#!/usr/bin/env python3
"""UserPromptSubmit hook — injects the current local time into every turn.

The harness currentDate field is date-only with no time of day and does not
refresh mid-session. This hook provides time-of-day precision, refreshed
every turn.

Register in .claude/settings.json under hooks > UserPromptSubmit.

CONTRACT (platform-neutral; a port to another platform meets the same terms):
  Input: the platform's per-message event; stdin is not read.
  Must: print the machine's current local time with the day of the week, the
  date, the time of day and the timezone, so the model has an accurate time
  reference before processing every user message.
  Output: JSON on stdout, hookSpecificOutput.additionalContext carrying
  "Local time: <stamp>".
"""
import json
import sys
from datetime import datetime

now = datetime.now().astimezone()

# Avoids %-d (GNU-only, not cross-platform). Strips leading zero manually.
stamp = now.strftime("%A, %B {day}, %Y, %H:%M %Z").format(day=now.day)

context = f"Local time: {stamp}"

print(json.dumps({"hookSpecificOutput": {
    "hookEventName": "UserPromptSubmit",
    "additionalContext": context,
}}))
sys.exit(0)

# Version 4.11
