# CLAUDE.md Template

Startup procedure for a Code project. Place at the project root as `CLAUDE.md`. Claude Code loads this automatically at the start of every session.

## Template Text

```
# [Project Name]

## Session Startup Procedure

At session start, execute every step below in order before responding. Every step is required regardless of the user's first message.

1. Orientation files:
   @Project/PROJECT_CONTEXT.md
   @Project/PROJECT_INDEX.txt
   @Project/HANDOFF.txt
   @Project/TASKS.txt              [if using a task queue file]

2. Find and read the most recent session log:
   ls "Project/Session Logs/" | tail -5
   Read the most recent, plus any additional logs the handoff identifies.

3. List Inbox contents (filenames only, don't read):
   ls Inbox/

4. Greet briefly. Then present a brief orientation: where work left off, what's pending, any Inbox items. One item per line, not education on what each item is about. Ask how the user would like to begin.

If you are reading this after context compaction, re-read
Project/PROJECT_CONTEXT.md in full before continuing.
```

## Notes

The `@` syntax imports files into context at load time. See [CLAUDE.md imports](https://code.claude.com/docs/en/memory#import-additional-files).

The compaction re-read line ensures the AI reloads its governing document when the context window is compressed mid-session.

Add project-specific startup steps as additional numbered steps. Keep CLAUDE.md under 200 lines.

---
*Part of [AI Project Architect](https://github.com/vbiroshak/ai-project-architect) — Version 4.7*
