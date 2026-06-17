# Claude Code Templates

Resources for setting up or migrating to Claude Code. See [claude-code-setup.md](../../claude-code-setup.md) for the full guide.

## Files

| File | What it is |
|------|-----------|
| temporal-awareness.py | Hook script (UserPromptSubmit): injects the current local time into every turn. Replaces the Clock file mechanism. Drop into `.claude/hooks/` and register in settings.json. |
| archive-transcripts.py | Hook script (SessionStart): copies completed session transcripts into the project's Sessions/ folder with human-readable names. Customize `PROJECT_NAME` and the naming regex for your project. |
| transcript-to-md.py | Renderer: converts .jsonl transcripts into readable collapsed-view Markdown. Called automatically by the archiver if present alongside it in `.claude/hooks/`. Also usable standalone. |
| settings-template.json | Example `.claude/settings.json` showing the permission structure, deny rules, Bash allow patterns, and hook registration. Replace paths with your own. |
| PREFERENCES-template.md | Starter structure for the project preferences file. Section headings with guidance on what goes where. Paste your system preferences in and organize. |

## Setup

1. Copy all three scripts (temporal-awareness.py, archive-transcripts.py, and transcript-to-md.py) into your project's `.claude/hooks/` directory. The archiver imports the renderer from the same directory; if it's missing, archiving works but without the Markdown companion files.
2. Edit `archive-transcripts.py`: set `PROJECT_NAME` to your project's name and adjust `NUM_PATTERNS` if your session declarations use a different format. To get readable filenames, open each session with a line like "This is [Project] 42" — the archiver extracts the name and number from this declaration. Without it, transcripts keep their UUID names.
3. Copy `settings-template.json` to `.claude/settings.json` and replace the placeholder paths with your actual project and resource paths.
4. The temporal-awareness hook works without modification.

## Notes

- All scripts use only Python standard library (no dependencies to install).
- The archiver copies transcripts; it never deletes source files.
- Deny rules in settings.json use `//` (double slash) for absolute paths. A single leading slash is project-relative.
- `additionalDirectories` grants read access to folders outside your project root.
- Bash allow rules match by prefix. `Bash(grep *)` allows any grep command without prompting. Keep destructive commands (rm, mv, etc.) behind prompts.

---
*Part of [AI Project Architect](https://github.com/vbiroshak/ai-project-architect) — Version 4.3*
