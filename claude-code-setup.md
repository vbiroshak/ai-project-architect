# Setting Up in Claude Code

A guide for running this workspace architecture in Claude Code, whether starting fresh or migrating from Claude Desktop Chat. The architecture itself is platform-agnostic, but Code provides native filesystem access, event-driven hooks, and an auto-loaded project file that make the setup cleaner and more capable than the Chat-based approach.

Other AI development tools (Gemini CLI, GitHub Copilot Coding Agent, Cursor, Windsurf, OpenAI Codex CLI) have similar mechanisms — all support auto-loaded project instruction files, and several support hook systems and permission configurations. If you use one of those, point it at this repo and ask it to adapt the setup below to its own conventions. (Download the repo or provide the files directly rather than linking — some tools fetch cached content from the web that may be outdated.)

---

## What Code Provides

Claude Code gives the AI native filesystem access without a connector extension. It also provides:

- **CLAUDE.md** — a markdown file at the project root that loads automatically into every conversation. Replaces the project instructions text field and the Config/PROJECT_INSTRUCTIONS.txt backup.
- **Event hooks** — scripts that run on specific events (session start, each user message, and others). Replace manual mechanisms like the Clock file for temporal awareness.
- **settings.json** — project-level permissions controlling which files can be read or written, which shell commands are allowed without prompting, and which paths are denied.
- **Native shell access** — Bash commands run directly. No connector tools, no container paths, no copy-to-claude mechanics.

Claude Code also has native equivalents for several things this architecture handles with project files: [`.claude/rules/`](https://code.claude.com/docs/en/memory#organize-rules-with-claude/rules/) for project-specific instructions (comparable to PROJECT CONTEXT entries in WORKFLOW.txt), [output styles](https://code.claude.com/docs/en/output-styles) for per-project behavioral configuration, and [auto memory](https://code.claude.com/docs/en/memory#auto-memory) for cross-session knowledge. This guide describes both the architecture's approach and the Code-native alternatives. For non-coding projects especially, keeping operating instructions in visible project files rather than a `.claude/` directory can be preferable — but the choice is yours.

These replace several pieces of the Chat-based setup. The architecture's design principles, file roles, and workflow structure are unchanged.

---

## Fresh Setup

To build a new project in Code using this architecture:

### 1. Create the project directory

Build the standard structure: WORKFLOW.txt, Workflow Files/ (with HANDOFF.txt, PROJECT_INDEX.txt, Session Logs/), Inbox/, and at least one sub-project folder. Use the [templates](templates/) as your starting point, same as any other setup.

### 2. Create CLAUDE.md

CLAUDE.md is a markdown file at the project root that Claude Code loads automatically at the start of every session. It replaces both the project instructions text field and the Config/PROJECT_INSTRUCTIONS.txt backup. The Config/ directory is not needed. See the [CLAUDE.md documentation](https://code.claude.com/docs/en/memory) for the full specification.

There are two approaches, depending on how much of the architecture you want CLAUDE.md to carry:

**Minimal pointer.** CLAUDE.md directs the AI to read WORKFLOW.txt, which remains the governing document:

```
# [Project Name]

At session start, before responding to anything else, read `[full path]/WORKFLOW.txt`
in full and execute its startup procedure.
```

This keeps CLAUDE.md small and leaves the architecture's standard file structure intact. WORKFLOW.txt holds the startup procedure, section registry, and project context as described in the main architecture document.

**Startup procedure.** CLAUDE.md itself becomes the startup procedure, reading a single governing document that consolidates what would otherwise be split across WORKFLOW.txt and a separate operating context file:

```
# [Project Name]

## Session Startup Procedure

At session start, execute every step below in order before responding.

1. Orientation files:
   @Project/PROJECT_CONTEXT.md
   @Project/PROJECT_INDEX.txt
   @Project/HANDOFF.txt

2. [Additional project-specific startup steps]

3. Greet briefly, present orientation, ask how to begin.

If you are reading this after context compaction, re-read
Project/PROJECT_CONTEXT.md in full before continuing.
```

In this model, PROJECT_CONTEXT.md replaces WORKFLOW.txt as the single governing document — it holds the project description, working methods, logging guidance, temporal awareness, and project-specific rules in one file. The startup procedure lives in CLAUDE.md rather than inside the governing document. The compaction re-read line at the bottom ensures the AI reloads its operating context when the context window is compressed mid-session, without needing a hook.

Both approaches work. The minimal pointer preserves the standard architecture. The startup procedure approach is simpler for projects where the governing content fits naturally in a single file. The architecture's principles (handoff-driven orientation, session logs, sub-project activation, fix on contact) are the same either way.

### 3. Set up user preferences

In Claude Desktop (Chat) and the web interface, user preferences are injected automatically from a settings field. Claude Code does not receive these. The AI has no access to what you entered there unless you provide it through one of these mechanisms:

**PREFERENCES.md** (project-level file). Create a preferences file in the project directory, add it to the startup read list, and paste in your preferences from the Claude app's settings. See [templates/claude-code/PREFERENCES-template.md](templates/claude-code/PREFERENCES-template.md) for a starter structure. This is portable and versionable, and preferences can be tailored per project — a research project might carry different behavioral rules than a coding project.

**Global CLAUDE.md** (Code-native, cross-project). Claude Code supports a user-level CLAUDE.md at `~/.claude/CLAUDE.md` that loads automatically into every session across all projects. User preferences that apply everywhere (interaction style, formatting rules, things the AI should never do) go here. Project-specific preferences stay in the project. This eliminates the need for a per-project PREFERENCES.md for content that doesn't change between projects. See [CLAUDE.md scoping](https://code.claude.com/docs/en/memory#choose-where-to-put-claude-md-files) for the full hierarchy.

**Output styles** (Code-native, per-project behavior). Agent definition files in `.claude/agents/` can serve as per-project behavioral profiles. When a project specifies an output style, Claude receives project-specific instructions about tone, response format, and working patterns without those instructions living in the startup read. This separates user preferences (who you are, how you work) from project behavior (how the AI should operate in this specific project). See the [output styles documentation](https://code.claude.com/docs/en/output-styles) for setup and configuration.

These three mechanisms layer: global CLAUDE.md for user-level preferences, output styles for project-level behavior, and PREFERENCES.md available as a fallback or for projects where you prefer everything explicit in one file. Use as much or as little of Code's native structure as fits your workflow.

### 4. Adapt the startup procedure

The Chat-based startup has steps that Code doesn't need:

- **Remove:** the Filesystem tools loading step (Code has native access), the filesystem-tools guide read, and the manual clock-check step (replaced by the temporal hook).
- **Remove:** the Config/PROJECT_INSTRUCTIONS.txt sync step (CLAUDE.md replaces it).
- **Add:** PREFERENCES.md to the read list, if using a project-level preferences file (see step 3).
- **Simplify:** file reads become a single numbered step listing everything to read.

The startup procedure should describe actions, not tools. "Read these files" rather than "use Filesystem:read_file to read these files."

### 5. Set up hooks

Create `.claude/hooks/` in the project directory and register them in `.claude/settings.json`.

**Temporal awareness** (UserPromptSubmit): A script that injects the current local time into every turn. Replaces the Clock file mechanism entirely — no Clock/ directory needed, no mid-chat clock checks, no timestamp.txt. The AI receives the time automatically before processing each message.

**Transcript archiving** (SessionStart): A script that copies the previous session's transcript into the project's Sessions/ folder (Workflow Files/Sessions/) with a readable name derived from the session content. Maintains the project's conversation record automatically. A companion script renders each transcript as a readable Markdown file (collapsed view: messages in full, tool calls as one-line summaries).

To get readable filenames (e.g., `MyProject_42.jsonl` rather than a UUID), open each session with a declaration line like "This is MyProject 42." The archiver extracts the name and number from this line. Without it, transcripts are still archived but keep their UUID names. The declaration pattern is configurable in the script.

All three scripts (the two hooks plus the renderer) go into `.claude/hooks/`. The archiver imports the renderer automatically when it's present alongside it; if it's missing, archiving still works but without the Markdown companion files.

### 6. Configure permissions

`.claude/settings.json` controls what the AI can access and which hooks run. See [templates/claude-code/settings-template.json](templates/claude-code/settings-template.json) for the full deployable template. The structure has three sections:

- **permissions.deny** — paths that must never be modified (read-only sources, snapshots from other applications). Deny rules take precedence over allow rules.
- **permissions.allow** — read/write access to project files, read access to external resources, and Bash utilities that should run without prompting.
- **hooks** — event registrations pointing to the scripts in `.claude/hooks/`.

Key points:
- Deny rules use `//` (double slash) for absolute paths. A single leading slash is project-relative in Code.
- Deny every write-capable tool for protected paths (Edit, Write, MultiEdit, NotebookEdit) to fully seal a read-only source.
- Allow read-only Bash utilities by prefix pattern to reduce permission prompts during normal work. Keep prompts on destructive or write-capable commands.
- `additionalDirectories` grants access to folders outside the project root (external resources, sibling projects, shared libraries).
- Hook commands should use `${CLAUDE_PROJECT_DIR:-$PWD}` rather than bare relative paths, so they resolve correctly regardless of where Code is launched.

### 7. Remove Chat-only artifacts

These are no longer needed:
- `Workflow Files/Clock/` — replaced by the temporal hook
- `Workflow Files/Config/` — replaced by CLAUDE.md
- Filesystem tools guide — Code has native access
- Cowork delegation guide — Code does directly what Chat delegated to Cowork (multi-file reads, batch processing, parallel work via subagents)
- Any references to connector tool calls (`Filesystem:read_file`, `copy_file_user_to_claude`, `/mnt/` paths)

### 8. Update the WORKFLOW section registry

Two sections change:

- **Temporal Awareness** — replace the Clock file mechanism with a note that time is injected by the temporal hook each turn. The AI consults the injected time before any time-referential statement. No action steps needed; the hook is automatic.
- **Tool Guides** — remove entries for tools that no longer exist (Filesystem tools, Cowork delegation). Add entries for tools the project does use (e.g., Chrome browser if applicable). Tool guides are read before the work that uses them, not at startup.

The Session Startup Procedure section shrinks: fewer steps, no tool-loading preamble.

---

## Migrating from Chat

If you have an existing Chat-based project to migrate:

### Setting up the migration session

Don't migrate a project from inside itself. A half-rebuilt project has a half-working startup procedure, and the AI can't orient cleanly while its own instructions are mid-edit.

The practical method:

1. **Copy the project to a backup location.** This is both your safety net and the reference copy the migration session can consult.
2. **Open Claude Code in a different directory** (any directory that isn't the project being migrated).
3. **Point that session at the live project path** and have it rebuild in place. The live path stays the same, so nothing downstream (other projects that reference it, bookmarks, your habits) needs to change.

The backup copy is untouched throughout. If anything goes wrong, restore from it. Once the first real session in Code confirms everything works, the backup can be archived or deleted.

### Principles

1. **Surgical and minimal.** Change only what Code actually breaks or what you direct. Preserve existing text and meaning.
2. **No system-contrast commentary.** Files read as the system itself, not as a migration story. No "instead of Chat," "now in Code," "unlike the old system." State new mechanisms plainly.
3. **State the action, not the tool.** Strip instructions that prescribe specific connector tool calls. Leave the action and the discipline.
4. **One home, no duplication.** Each fact lives in exactly one file. CLAUDE.md replaces Config/PROJECT_INSTRUCTIONS.txt; don't keep both.
5. **Complete the reference chain.** Every move, deletion, or rename updates all references in the same pass. No deferred fixes.
6. **Freeze the historical record.** Session logs, archived transcripts, and dated changelog entries preserve old references as history. Never rewrite them.

### Process

1. **Back up the original.** Keep an untouched copy as a safety net before any edits.
2. **Place the new infrastructure.** Create `.claude/` with settings.json and hooks. Create CLAUDE.md at the project root. Set up user preferences using one of the approaches described in the fresh setup guide (project-level file, global CLAUDE.md, or output styles).
3. **Apply the fresh-setup changes above** — adapt the startup procedure, remove Chat-only artifacts, update the section registry. Work surgically on the specific lines that differ.
4. **Fix internal references.** Grep every active file for connector tool calls (`Filesystem:`, the connector verbs, `/mnt/`), Cowork-as-mechanism language, and dead paths. Fix each to state the action plainly or point to the correct current path.
5. **Repoint paths** if the project moved to a new directory. Exact-string replacement, scoped to self-references. External resource paths may also need reconciling.
6. **Add a HISTORY section** to an always-read file (e.g., a startup-read companion file or the WORKFLOW's PROJECT CONTEXT section). A short factual note: sessions 001–NNN ran in Chat on this architecture; from session NNN+1 it runs in Code. Name the two things a reader will encounter in the old record (the Filesystem connector mechanics; Cowork delegation) and what they were. Framed as context for a reader, not instruction.
7. **Verify.** Start a real session. Confirm CLAUDE.md auto-loads, the startup procedure runs, hooks fire (time appears, prior transcript archives), and the project works. Do real work in the first session to confirm continuity.

### What stays the same

The architecture's core is unchanged in Code, regardless of which file layout you choose:
- A governing document as the entry point (WORKFLOW.txt, PROJECT_CONTEXT.md, or equivalent)
- HANDOFF.txt overwritten with every log entry
- PROJECT_INDEX.txt as the structural map
- Session logs per unit of work, sequential numbering
- Inbox as the asynchronous interface
- Sub-project activation pattern
- Fix on contact, freshness lines, evolving state
- The indexed collection pattern
- All domain content and working files

---

## Code-Specific Features

### Working with Claude Code's auto memory

Claude Code has a built-in [auto memory](https://code.claude.com/docs/en/memory#auto-memory) system where it stores notes across sessions — build commands, debugging insights, user preferences, and patterns it discovers. For projects using this workspace architecture, the project files themselves are the primary memory (the handoff, session logs, status files, and project context carry everything a session needs). Auto memory serves a different purpose: it captures behavioral knowledge about how to work with you and with the project's tooling.

There are two reasonable approaches:

**Suppress auto memory.** If you want the project architecture to be the sole knowledge store, redirect or disable it. Add to CLAUDE.md or your project settings:

```json
{ "autoMemoryEnabled": false }
```

Or redirect it to a project-controlled directory in `.claude/settings.json`:

```json
{ "autoMemoryDirectory": "[full path]/Workflow Files/Claude Memory" }
```

Redirecting keeps auto memory active but puts the files where the project can see and manage them. The project files govern; a note that contradicts them is stale and deleted on contact.

**Use both layers.** Let auto memory handle what it's designed for (behavioral preferences, tool quirks, correction patterns) while the project architecture handles what it's designed for (work state, decisions, orientation). These are complementary: auto memory is a small notebook about how to work; the project files are the record of what work was done. If auto memory starts duplicating project document content, that signals the documents aren't functioning as behavioral instruction on first read — useful diagnostic information for improving your project files.

### Managing accumulated permissions

Claude Code maintains a `settings.local.json` that accumulates "always allow" grants as you approve actions during work. Over time this file can grow with grants you approved without fully understanding their scope (MCP tool allows are tool-wide, not per-action; Bash allows match by prefix). Periodically review it and clear grants that are too broad. The project `settings.json` is the deliberate policy; `settings.local.json` is the accumulated ad-hoc grants.

### On-demand reads and trigger maps

For projects with substantial domain reference material (style guides, process documents, reference files), loading everything at startup wastes context. Code's larger effective context makes it tempting to load more, but the principle holds: read what you need when you need it.

A trigger map in WORKFLOW.txt names the files, their recognition cues, and what they guard against. The model applies these by judgment — when it recognizes the work type, it loads the relevant files before proceeding. This keeps startup lean while ensuring domain knowledge is loaded before the work that needs it, not after.

---

## Capabilities Gained in Code

Beyond the cleaner setup, Code enables work that Chat delegated or couldn't do:

- **Multi-file operations in a single session** — read, compare, and edit across many files without context fragmentation or tool-call limits.
- **Subagents** — fan out parallel work (audits, batch reads, multi-file searches) within the same session, replacing external delegation.
- **Shell integration** — run scripts, process files with standard tools (grep, sed, python), interact with version control, all within the session.

These don't change the architecture. They change what's practical within it.

---
*Part of [AI Project Architect](https://github.com/vbiroshak/ai-project-architect) — Version 4.3*
