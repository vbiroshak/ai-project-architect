# Claude Code Templates

Resources for setting up or migrating to Claude Code. See [claude-code-setup.md](../../claude-code-setup.md) for the full setup guide and [chat-to-code-migration.md](../../chat-to-code-migration.md) for the migration guide.

## Files

### Hooks and session infrastructure

| File | What it is |
|------|-----------|
| temporal-awareness.py | Hook script (UserPromptSubmit): injects the current local time into every turn. Drop into `.claude/hooks/` and register in settings.json. |
| archive-transcripts.py | Hook script (SessionStart): copies completed session transcripts into the project's Sessions/ folder with human-readable names. Set `PROJECT_NAME` at the top of the script to the project's name. Touches only transcripts in Claude Code's format; another platform's archives in the same folder are left alone. |
| transcript_to_md.py | Renderer: converts .jsonl transcripts into readable collapsed-view Markdown. Called automatically by the archiver if present alongside it in `.claude/hooks/`. Also usable standalone. |

### Project templates

| File | What it is |
|------|-----------|
| CLAUDE-template.md | Startup procedure template for CLAUDE.md. Place at the project root. |
| PROJECT-CONTEXT-template.md | Governing document template for PROJECT_CONTEXT.md. All standard sections with Code-specific paths and mechanics. Place at Project/PROJECT_CONTEXT.md. |
| PROJECT-INDEX-template.md | File structure index template for PROJECT_INDEX.txt with the Code directory layout. Place at Project/PROJECT_INDEX.txt. |

### Skills

| File | What it is |
|------|-----------|
| skills/handoff/SKILL.md | The `/handoff` command: tells Claude the session is closing and to follow SESSION CLOSE in PROJECT_CONTEXT.md. Copy the folder to `.claude/skills/`; the folder name is the command name. |

### Configuration

| File | What it is |
|------|-----------|
| settings-template.json | Example `.claude/settings.json` showing the permission structure (allow rules, a deny rule, additional directories) and hook registration. Replace the placeholder paths with the project's own. |

### Transcript processing (for migration)

| File | What it is |
|------|-----------|
| split_export.py | Splits a Claude.ai bulk data export (conversations.json) into individual per-project .json files. Edit the KNOWN_PROJECTS list with the user's project names before running. See [chat-to-code-migration.md](../../chat-to-code-migration.md) for the full pipeline. |
| chat_export_to_md.py | Converts individual Chat .json transcripts into readable collapsed-view .md files. Reads the structured content blocks (not the flattened text field which loses all tool calls). |

## Setup

1. Copy all three scripts (temporal-awareness.py, archive-transcripts.py, and transcript_to_md.py) into the project's `.claude/hooks/` directory. Copy the files exactly (with `cp`, for example), not retyped or regenerated: a rewritten copy can silently diverge from the tested source. The archiver imports the renderer from the same directory; without it, archiving works but no Markdown companions are written.
2. Edit `archive-transcripts.py`: set `PROJECT_NAME` at the top to the project's name. The archiver names transcripts using four tiers: `/rename` with a name and number (e.g. "MyProject 42") is checked first, then a "This is MyProject 42" declaration in the opening message, then a free-form `/rename` title (used as the filename as-is), then UUID as fallback. Number-named sessions are formatted as `MyProject_0042.jsonl`. The name may contain spaces and accented letters.
3. Copy `settings-template.json` to `.claude/settings.json` and replace the placeholder paths with the project's own paths and the resource paths the user named.
4. The temporal-awareness hook works without modification.

## Notes

- All scripts use only Python standard library (no dependencies to install).
- The archiver copies transcripts; it never deletes source files.
- Absolute paths in settings.json rules use `//` (double slash). A single leading slash is project-relative.
- File rules use `Read(...)` and `Edit(...)`. An `Edit` rule covers every tool that changes files.
- `permissions.additionalDirectories` adds folders outside the project root as working directories: readable without prompts, with edits following the current permission mode.
- The template pre-approves no shell commands. Bash allow rules, if the user adds any, match by prefix: `Bash(grep *)` allows any grep command without prompting. Keep destructive commands (rm, mv, etc.) behind prompts.

---
*Part of [AI Project Architect](https://github.com/vbiroshak/ai-project-architect) — Version 4.11*
