#!/usr/bin/env python3
"""UserPromptSubmit hook — injects the current local time into every turn.

The harness currentDate field is date-only with no time of day and does not
refresh mid-session. This hook provides time-of-day precision, refreshed
every turn.

Register in .claude/settings.json under hooks > UserPromptSubmit.
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

# Version 4.6
