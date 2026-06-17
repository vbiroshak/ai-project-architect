#!/usr/bin/env python3
"""UserPromptSubmit hook — injects the current local time into every turn.

Replaces the Clock file mechanism from the Chat-based setup. The AI receives
the current time automatically before processing each user message, so there
is no Clock/ directory, no manual check step, and no stale timestamps.

Register in .claude/settings.json under hooks > UserPromptSubmit.

How it works: Claude Code hooks can return additionalContext via a JSON object
printed to stdout. This context appears as a system reminder attached to the
user's message. The temporal-awareness hook prints the formatted local time
so the AI always knows what time it is without a tool call or file read.
"""
import json
import sys
from datetime import datetime

now = datetime.now().astimezone()

# Format the timestamp in a human-readable way.
# Avoids %-d and %-I (GNU-only, not cross-platform). Strips leading zeros manually.
stamp = now.strftime("%A, %B {day}, %Y, {hour}:%M %p %Z").format(
    day=now.day, hour=((now.hour - 1) % 12) + 1
)

context = (
    "=== Current local time (injected each turn) ===\n"
    f"{stamp}\n"
    "Consult this before any time-referential statement — greetings, \"today\"/\"this "
    "morning\", elapsed-time remarks. It refreshes every turn; the harness 'currentDate' "
    "field is date-only, so this is the authoritative time of day."
)

print(json.dumps({"hookSpecificOutput": {
    "hookEventName": "UserPromptSubmit",
    "additionalContext": context,
}}))
sys.exit(0)
