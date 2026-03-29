# Temporal Awareness

WORKFLOW section — universal, identical across all projects. See the [temporal awareness pattern](../../patterns/temporal-awareness.md) for the full mechanism, setup instructions, and implementation details.

## Template Text

```
---
TEMPORAL AWARENESS

The AI has no internal clock.

CURRENT TIME — Workflow Files/Clock/timestamp.txt

Only the modification timestamp matters, not the file's content.

  1. Write "tick" to the file (overwrite)
  2. Get the file's info — the "modified" field is the current time

If the modified date is earlier than the system prompt date, repeat both steps once. Never delete the Clock file.

TIME SINCE LAST LOGGED INTERACTION — Get the most recent session log's file info and compare its modified timestamp to the Clock reading.

Consider what both imply: day of week, business hours, calendar deadlines, how much may have changed since last contact.
```
