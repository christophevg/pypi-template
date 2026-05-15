# TODO

## Inbox Input (2026-04-20)

*Unstructured input from inbox processing session. To be refined and integrated.*

- pypi-template: template based project management tool
- Decision: stop using it and deprecate in favor of agentic project management
- TODO: identify all projects that use pypi-template and plan migration
- TODO: keep in mind that this must be removed

## Backlog

_Empty - deprecation complete_

## Completed Deprecation Tasks

- [x] **deprecate-pypi-template** (2026-05-15)
  - Added deprecation banner to README.md and docs/index.md
  - Created MIGRATION.md with step-by-step migration guide
  - Updated pyproject.toml with deprecation notice
  - Project marked as deprecated, ready for archival

- [x] **stop-using-pypi-template** (2026-04-29)
  - Decision made to deprecate pypi-template
  - Replaced by modern pyproject.toml + hatchling setup
  - See c3/skills/python-project/SKILL.md for new standard