"""Deterministic retry and idempotency model for the lab."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Reservation:
    id: str
    member_id: str
    workshop_id: str


@dataclass(frozen=True)
class EmailSend:
    id: str
    reservation_id: str
    recipient: str
    template: str
    dedupe_key: str


@dataclass(frozen=True)
class IdempotencyRecord:
    key: str
    fingerprint: tuple[str, str]
    reservation_id: str


@dataclass(frozen=True)
class CommandResult:
    status: str
    reservation_id: str | None
    duplicate: bool
    email_sent: bool


@dataclass(frozen=True)
class EventResult:
    status: str
    duplicate: bool
    email_sent: bool


class ReservationSystem:
    """Small in-memory system that makes duplicate work visible."""

    def __init__(self) -> None:
        self.reservations: list[Reservation] = []
        self.emails: list[EmailSend] = []
        self.idempotency_records: dict[str, IdempotencyRecord] = {}
        self.processed_event_ids: set[str] = set()
        self.sent_side_effect_keys: set[str] = set()
        self.key_conflicts = 0
        self.duplicate_requests = 0
        self.duplicate_events = 0

    def reserve_without_idempotency(
        self,
        member_id: str,
        workshop_id: str,
    ) -> CommandResult:
        reservation = self._create_reservation(member_id, workshop_id)
        self._send_email(
            reservation_id=reservation.id,
            recipient=member_id,
            template="reservation_confirmation",
            dedupe_key=f"unsafe:{reservation.id}:confirmation",
        )
        return CommandResult(
            status="created",
            reservation_id=reservation.id,
            duplicate=False,
            email_sent=True,
        )

    def reserve_with_idempotency(
        self,
        member_id: str,
        workshop_id: str,
        idempotency_key: str,
    ) -> CommandResult:
        if not idempotency_key:
            raise ValueError("idempotency_key must not be empty")

        fingerprint = (member_id, workshop_id)
        existing = self.idempotency_records.get(idempotency_key)
        if existing:
            if existing.fingerprint != fingerprint:
                self.key_conflicts += 1
                return CommandResult(
                    status="conflict",
                    reservation_id=existing.reservation_id,
                    duplicate=True,
                    email_sent=False,
                )
            self.duplicate_requests += 1
            return CommandResult(
                status="duplicate",
                reservation_id=existing.reservation_id,
                duplicate=True,
                email_sent=False,
            )

        reservation = self._create_reservation(member_id, workshop_id)
        self.idempotency_records[idempotency_key] = IdempotencyRecord(
            key=idempotency_key,
            fingerprint=fingerprint,
            reservation_id=reservation.id,
        )
        email_sent = self._send_email_once(
            reservation_id=reservation.id,
            recipient=member_id,
            template="reservation_confirmation",
            side_effect_key=f"reservation:{reservation.id}:confirmation",
        )
        return CommandResult(
            status="created",
            reservation_id=reservation.id,
            duplicate=False,
            email_sent=email_sent,
        )

    def handle_event_without_dedupe(
        self,
        event_id: str,
        reservation_id: str,
        recipient: str,
    ) -> EventResult:
        self._send_email(
            reservation_id=reservation_id,
            recipient=recipient,
            template="reservation_receipt",
            dedupe_key=f"unsafe-event:{event_id}",
        )
        return EventResult(status="sent", duplicate=False, email_sent=True)

    def handle_event_with_dedupe(
        self,
        event_id: str,
        reservation_id: str,
        recipient: str,
    ) -> EventResult:
        if event_id in self.processed_event_ids:
            self.duplicate_events += 1
            return EventResult(
                status="duplicate_event",
                duplicate=True,
                email_sent=False,
            )

        self.processed_event_ids.add(event_id)
        side_effect_key = f"reservation:{reservation_id}:receipt:{recipient}"
        email_sent = self._send_email_once(
            reservation_id=reservation_id,
            recipient=recipient,
            template="reservation_receipt",
            side_effect_key=side_effect_key,
        )
        if not email_sent:
            return EventResult(
                status="duplicate_side_effect",
                duplicate=True,
                email_sent=False,
            )
        return EventResult(status="sent", duplicate=False, email_sent=True)

    def _create_reservation(self, member_id: str, workshop_id: str) -> Reservation:
        reservation = Reservation(
            id=f"res-{len(self.reservations) + 1:03d}",
            member_id=member_id,
            workshop_id=workshop_id,
        )
        self.reservations.append(reservation)
        return reservation

    def _send_email_once(
        self,
        reservation_id: str,
        recipient: str,
        template: str,
        side_effect_key: str,
    ) -> bool:
        if side_effect_key in self.sent_side_effect_keys:
            return False
        self.sent_side_effect_keys.add(side_effect_key)
        self._send_email(
            reservation_id=reservation_id,
            recipient=recipient,
            template=template,
            dedupe_key=side_effect_key,
        )
        return True

    def _send_email(
        self,
        reservation_id: str,
        recipient: str,
        template: str,
        dedupe_key: str,
    ) -> EmailSend:
        email = EmailSend(
            id=f"email-{len(self.emails) + 1:03d}",
            reservation_id=reservation_id,
            recipient=recipient,
            template=template,
            dedupe_key=dedupe_key,
        )
        self.emails.append(email)
        return email


def run_duplicate_request_attempts(
    system: ReservationSystem,
    attempts: int,
    member_id: str,
    workshop_id: str,
    idempotency_key: str | None = None,
) -> list[CommandResult]:
    """Run repeated client attempts against safe or unsafe command handling."""
    if attempts < 0:
        raise ValueError("attempts must be zero or greater")

    results: list[CommandResult] = []
    for _index in range(attempts):
        if idempotency_key is None:
            results.append(
                system.reserve_without_idempotency(
                    member_id=member_id,
                    workshop_id=workshop_id,
                )
            )
        else:
            results.append(
                system.reserve_with_idempotency(
                    member_id=member_id,
                    workshop_id=workshop_id,
                    idempotency_key=idempotency_key,
                )
            )
    return results


def run_duplicate_event_deliveries(
    system: ReservationSystem,
    deliveries: int,
    reservation_id: str,
    recipient: str,
    safe: bool = True,
) -> list[EventResult]:
    """Run repeated event deliveries against safe or unsafe event handling."""
    if deliveries < 0:
        raise ValueError("deliveries must be zero or greater")

    event_id = f"reservation.confirmed:{reservation_id}"
    results: list[EventResult] = []
    for _index in range(deliveries):
        if safe:
            results.append(
                system.handle_event_with_dedupe(
                    event_id=event_id,
                    reservation_id=reservation_id,
                    recipient=recipient,
                )
            )
        else:
            results.append(
                system.handle_event_without_dedupe(
                    event_id=event_id,
                    reservation_id=reservation_id,
                    recipient=recipient,
                )
            )
    return results
