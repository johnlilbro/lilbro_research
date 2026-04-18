# NOTIFICATIONS

Each successful `lilbro_research` cycle writes a notification-ready markdown file into `notifications/`.

## Purpose

This provides a durable handoff point for later user-facing alerts.

## File pattern

- `notifications/research_cycle_complete_<timestamp>.md`

## Included details

- timestamp
- chosen topic
- created branch
- generated files
- cycle count

## Future extension

Later, this can be connected to an OpenClaw-driven alert so Mr. John gets a direct message when a cycle finishes.
