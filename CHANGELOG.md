# Changelog

This file records major content, lab, template, and automation changes for the
System Design Decision Cookbook. Use it to explain what changed, why it matters
to learners, and which release phase it supports.

Release phases follow the [Roadmap](ROADMAP.md):

- **MVP:** M0-M3 tickets marked `mvp = TRUE`.
- **v1:** M4 production-depth material after the MVP learning path works.
- **v2 and long-term:** M5 expansion, polish, automation, and contribution
  quality improvements.

## How To Update This File

Update the changelog when a pull request changes learner-facing content,
runnable labs, reusable templates, public contribution workflow, or release
automation.

For each entry, include:

- the ticket ID or issue reference;
- the changed area, such as docs, labs, templates, or automation;
- the learner or contributor impact;
- any known compatibility, navigation, or follow-up note.

Small typo fixes do not need a changelog entry unless they correct misleading
technical guidance.

## Unreleased

Use this section until the first tagged release.

### Added

- Initial changelog and release notes process.
- `SDC-E15-T09` added a manual contribution quality dashboard so contributors
  can review epic coverage, diagram coverage, lab completeness, stale-page
  signals, and walkthrough completeness before releases.

### Changed

- Nothing yet.

### Fixed

- Nothing yet.

### Known Gaps

- No tagged release has been cut yet.

## Release Notes Format

Copy the relevant format when preparing a release.

### MVP Release Notes

Use this for the first public cut of the cookbook.

```text
## MVP - <date>

### Learning Path

- <What a new reader can now do from start to finish.>

### Included Scope

- <M0-M3 milestone areas completed for the MVP cut.>
- <Key docs, walkthroughs, labs, templates, and review aids.>

### Checks

- <Docs, link, lab, and automation checks run before release.>

### Known Gaps

- <Intentional omissions, rough edges, or follow-up tickets.>

### Upgrade Notes

- <Navigation, template, or lab behavior changes contributors should know.>
```

### v1 Release Notes

Use this after the MVP learning path works and production-depth material is
ready.

```text
## v1 - <date>

### Production Depth Added

- <M4 areas completed: data, communication, scalability, reliability, security,
  operations, or cost.>

### Improved Guidance

- <Decision trees, walkthroughs, labs, or rubrics that became more complete.>

### Contributor Impact

- <Template, workflow, review, or automation changes that affect pull requests.>

### Checks

- <Docs, link, lab, and automation checks run before release.>

### Known Gaps

- <Advanced topics or labs intentionally left for v2.>
```

### v2 And Long-Term Release Notes

Use this for expansion, polish, and sustained contribution releases.

```text
## v2 - <date>

### New Examples And Practice

- <Additional walkthroughs, prompts, flashcards, templates, or challenge paths.>

### New Labs Or Simulators

- <Runnable additions and what behavior they demonstrate.>

### Automation And Maintenance

- <Checks, validators, release tooling, dashboards, or repo quality changes.>

### Breaking Or Notable Changes

- <Renamed pages, moved labs, changed templates, or contribution workflow
  changes.>

### Known Gaps

- <Remaining quality, coverage, or automation gaps.>
```

## Entry Checklist

Before adding a release entry, confirm:

- the entry describes learner or contributor impact, not just file movement;
- the release phase matches the roadmap;
- known gaps are explicit;
- links point to stable repository files;
- the wording is original and does not summarize external material.
