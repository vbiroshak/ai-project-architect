# Claude Code Templates

Resources for setting up or migrating to Claude Code. See [claude-code-setup.md](../../claude-code-setup.md) for the full setup guide and [chat-to-code-migration.md](../../chat-to-code-migration.md) for the migration guide.

## Files

### Hooks and session infrastructure

| File | What it is |
|------|-----------|
| temporal-awareness.py | Hook script (UserPromptSubmit): injects the current local time into every turn. Replaces the Clock file mechanism. Drop into `.claude/hooks/` and register in settings.json. |
| archive-transcripts.py | Hook script (SessionStart): copies completed session transcripts into the project's Sessions/ folder with human-readable names. Set `PROJECT_NAME` at the top of the script to your project's name. |
| transcript_to_md.py | Renderer: converts .jsonl transcripts into readable collapsed-view Markdown. Called automatically by the archiver if present alongside it in `.claude/hooks/`. Also usable standalone. |

### Project templates

| File | What it is |
|------|-----------|
| CLAUDE-template.md | Startup procedure template for CLAUDE.md. Place at the project root. |
| PROJECT-CONTEXT-template.md | Governing document template for PROJECT_CONTEXT.md. All standard sections with Code-specific paths and mechanics. Place at Project/PROJECT_CONTEXT.md. |
| PROJECT-INDEX-template.md | File structure index template for PROJECT_INDEX.txt with the Code directory layout. Place at Project/PROJECT_INDEX.txt. |

### Configuration

| File | What it is |
|------|-----------|
| settings-template.json | Example `.claude/settings.json` showing the permission structure, deny rules, Bash allow patterns, hook registration, and auto memory redirect. Replace paths with your own. |

### Transcript processing (for migration)

| File | What it is |
|------|-----------|
| split_export.py | Splits a Claude.ai bulk data export (conversations.json) into individual per-project .json files. Edit the KNOWN_PROJECTS list with your project names before running. See [chat-to-code-migration.md](../../chat-to-code-migration.md) for the full pipeline. |
| chat_export_to_md.py | Converts individual Chat .json transcripts into readable collapsed-view .md files. Reads the structured content blocks (not the flattened text field which loses all tool calls). |

## Setup

1. Copy all three scripts (temporal-awareness.py, archive-transcripts.py, and transcript_to_md.py) into your project's `.claude/hooks/` directory. The archiver imports the renderer from the same directory; if it's missing, archiving works but without the Markdown companion files.
2. Edit `archive-transcripts.py`: set `PROJECT_NAME` at the top to your project's name. The archiver names transcripts using three tiers: `/rename` with a name and number (e.g. "MyProject 42") is checked first, then a "This is MyProject 42" declaration in the opening message, then UUID as fallback. Named sessions are formatted as `MyProject_0042.jsonl`.
3. Copy `settings-template.json` to `.claude/settings.json` and replace the placeholder paths with your actual project and resource paths.
4. The temporal-awareness hook works without modification.

## Notes

- All scripts use only Python standard library (no dependencies to install).
- The archiver copies transcripts; it never deletes source files.
- Deny rules in settings.json use `//` (double slash) for absolute paths. A single leading slash is project-relative.
- `additionalDirectories` grants read access to folders outside your project root.
- Bash allow rules match by prefix. `Bash(grep *)` allows any grep command without prompting. Keep destructive commands (rm, mv, etc.) behind prompts.

---
*Part of [AI Project Architect](https://github.com/vbiroshak/ai-project-architect) — Version 4.5*
