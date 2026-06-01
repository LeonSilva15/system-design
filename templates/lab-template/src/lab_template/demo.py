"""Minimal demo entry point for new labs."""


def run_demo() -> list[str]:
    """Return observable output for the template smoke test.

    Replace this with lab-specific behavior when copying the template.
    """
    return [
        "scenario=baseline",
        "step=1 result=accepted",
        "step=2 result=observed",
        "summary=replace this with lab-specific evidence",
    ]


def main() -> None:
    for line in run_demo():
        print(line)


if __name__ == "__main__":
    main()
