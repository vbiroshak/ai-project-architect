# Temporal Awareness

WORKFLOW section — universal, identical across all projects. See the [temporal awareness pattern](../../patterns/temporal-awareness.md) for the full mechanism, setup instructions, and implementation details.

## Template Text

```
---
TEMPORAL AWARENESS

The AI has no internal clock. Do not estimate, infer, or guess the time. Use the clock mechanism below.

CLOCK FILE — Workflow Files/Clock/timestamp.txt

Only the modification timestamp matters, do not read the file's content.

To check the current time:

  1. Write "tick" to the file (overwrite)
  2. Get the file's info — the "modified" field is the current time

If the modified date is earlier than the system prompt date, repeat both steps once. Never delete the Clock file.

WHEN TO CHECK THE CLOCK:

AT STARTUP (step 3): Tick the clock. Get the most recent session log's file info and compare its modified timestamp to the Clock reading. Consider what both imply: day of week, business hours, calendar deadlines, how much may have changed since last contact.

MID-CHAT: Before the first filesystem operation in each response, get the Clock file's info (do NOT tick it yet — just read the metadata). If the last clock check was on a different calendar date than the system prompt date, or more than two hours ago: tick the clock, calculate the gap, acknowledge it briefly to the user, and record it at the next log write. If the last clock check was today and less than two hours ago, continue normally.
```

---
*Part of [AI Project Architect](https://github.com/vbiroshak/ai-project-architect) — Version 4.4*
