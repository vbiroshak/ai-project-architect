# Migrating from Chat to Code

A guide for migrating an existing Chat-based project to Claude Code. For the target state (what a Code project looks like), see [claude-code-setup.md](claude-code-setup.md). This document covers only the migration-specific work: how to get from Chat to Code.

---

## Setting Up the Migration Session

Don't migrate a project from inside itself. A half-rebuilt project has a half-working startup procedure, and the AI can't orient cleanly while its own instructions are mid-edit.

Migrate from a separate Claude Code session: a coordinator project, a different project with read access, or any directory that isn't the project being migrated. Point the session at the live project path and rebuild in place. Back up the project directory first as a safety net. Once the first real Code session confirms everything works, the backup can be archived or deleted.

---

## Principles

Hold all of them.

1. **Surgical and minimal.** Change only what the Code harness actually breaks, or what you direct. Preserve existing text and meaning; never reword or translate prose while fixing a problem.
2. **No system-contrast commentary.** Files read as the system itself, not as a migration story. No "instead of," "unlike Chat," "now in Code." State any new mechanism plainly, as if the file always said it.
3. **State the action, not the tool.** Strip instructions that prescribe specific connector tool calls (e.g., "use Filesystem:list_directory"); leave the action and the discipline.
4. **One home, no duplication.** Each fact lives in exactly one file. CLAUDE.md replaces Config/PROJECT_INSTRUCTIONS.txt; don't keep both.
5. **Capability preserved, mechanism adapted.** The system must still do everything it did. Only the mechanism changes where Code differs from Chat. If a Chat project had temporal awareness via a Clock file, the Code project has temporal awareness via a hook. The capability doesn't disappear — the mechanism changes.
6. **Complete the reference chain.** Every move, deletion, or rename updates all references in the same pass. No deferred fixes.
7. **Functional vs. cosmetic.** Fix what would break or misdirect operation: a path that doesn't resolve, a reference to something deleted, a tool call Code lacks. Ignore cosmetic drift like a count off by one. Normal sessions self-correct cosmetic issues; the migration should not scope-creep into a general cleanup.
8. **Freeze the historical record.** Session logs, archived transcripts, the Archive folder, and dated CHANGELOG entries preserve old references as history. Never rewrite them.
9. **No propagating artifacts.** Don't introduce a non-standard section or pattern (e.g., a "Migration Notes" section in the handoff) that a future session would replicate forever. Put facts into the body of existing sections.
10. **Copy, then edit.** When setting up hooks, copy working scripts from an existing Code project and surgically edit the project name. Don't rewrite from memory.
11. **Don't edit the migrated project's handoff.** The migration runs from a separate session; the project's first Code session writes its own handoff.

---

## Transcript Processing

If you have Chat session history worth preserving, process the transcripts before making structural changes. This is optional for projects with minimal history — you can skip straight to the structural migration.

Before starting, verify the transcript count matches the project's known Chat session count. Mismatches (gaps, duplicates, unnamed conversations) are easier to resolve before alignment than after.

### The data export

Anthropic's data export bundles all conversations across all projects into a single `conversations.json` file. Projects are listed separately in the export but do not reference their conversations, and conversations do not carry a project identifier. The most reliable way to associate a conversation with its project is by the conversation's `name` field.

Some conversations that were deleted in the Chat UI may still appear in the export with empty content — message shells with no text, no tool calls, no attachments. These can be identified and ignored.

### Splitting by project

`split_export.py` (in [templates/claude-code/](templates/claude-code/)) reads `conversations.json`, identifies each conversation's project from its `name` field (pattern: "ProjectName N"), and writes individual `.json` files named with the 4-digit convention (`ProjectName_0042.json`) into a staging directory organized by project. It reports per-project counts, gaps, and duplicates.

Before running, edit the `KNOWN_PROJECTS` list at the top of the script with your project names — the script matches conversation names only against that list, so run as shipped it matches nothing.

Usage: `python3 split_export.py <batch-dir> <output-dir> [--project ProjectName] [--dry-run]` (on Windows, invoke with `python` or `py -3` instead of `python3` — here and in the commands below)

The script matches only integer-named conversations (e.g., "MyProject 42"). Unnamed conversations are counted but not written unless `--include-unnamed` is passed. Conversations whose number collides with one already written are quarantined into `_duplicates/` for manual resolution.

### Converting to readable Markdown

`chat_export_to_md.py` (in [templates/claude-code/](templates/claude-code/)) converts each individual `.json` into a collapsed-view `.md` — the readable companion. Human messages render as `## User`, assistant messages as `## Claude`. Tool calls render as `→ name` lines. Tool results, token_budget blocks, and whitespace-only text blocks are omitted. Thinking renders as blockquoted reasoning.

The script reads the structured `content` blocks in each message, not the flattened `text` field. The `text` field can contain "This block is not supported on your current device yet" placeholders where tool calls should be. The `content` blocks have the actual data.

Usage: `python3 chat_export_to_md.py <directory>` converts every `.json` in the directory.

### Verification

After conversion, verify:
- Zero "This block is not supported" strings in any `.md`
- `→ ` lines present (tool calls survived)
- `## User` / `## Claude` headers (not a personal name)
- No `tool_result` content leaked through

### Naming, numbering, and alignment

Session logs are the canonical navigation system. Logs keep their original sequential numbers with 4-digit padding — they are never renamed in a way that changes the session number the AI uses inside the file and in cross-references. A renamed log whose filename no longer matches its internal session number breaks every reference to that session.

Transcripts are named to match their primary log number: the first log a chat wrote determines the transcript's number. To find which log each chat wrote, extract the write events from the transcripts mechanically (look for Filesystem:write_file calls targeting Session Logs/).

**Write out the full alignment plan before executing.** Map every transcript to its destination number. Verify the plan at sample points before renaming anything. Renaming without a plan leads to cascading corrections.

**Use a temp directory for renames** to avoid collisions when old and new numbers overlap (e.g., transcript 5 needs to become 3, but transcript 3 hasn't moved yet). Copy to temp, then from temp to final names.

**Never delete transcripts without reading them.** A session with a proper opener is a real session even if it didn't write a log. Only truly empty transcripts (no content at all) should be excluded. If a rename script also deletes, ensure deletes run on original filenames before renames — otherwise newly renamed files at the same numbers get caught.

The naming conventions:

- **1:1 sessions** — transcript gets the log number.
- **Multi-log sessions** (one chat wrote multiple logs) — the transcript gets the first log number. Each secondary log gets a pointer line at the bottom: "Session transcript: Project/Sessions/ProjectName_NNNN" linking to the transcript for that chat. Only needed where the log number differs from the transcript number.
- **Pre-log transcripts** (sessions before the project had logging) — name them ProjectName_0000a through ProjectName_0000x. These sort before 0001 and letters give sequence.
- **No-log sessions** (sessions that didn't write a log) — name the transcript by position in the log timeline: the last log number before them + letter suffix (e.g., between logs 010 and 011 → ProjectName_0010b).

### Placing transcripts

Create Project/Sessions/ (or Workflow Files/Sessions/ if placing before the directory rename). Copy both the `.json` and `.md` files. The `.json` is the canonical record; the `.md` is the readable companion.

Going forward in Code, the archive hook names transcripts from `/rename` (checked first) or the "This is ProjectName NNN" session opener (fallback). Number-named sessions are formatted as `ProjectName_NNNN.jsonl`. The first Code session number = last log number + 1.

---

## The Structural Migration

The target state for each file is described in [claude-code-setup.md](claude-code-setup.md). This section covers how to get there from the Chat layout.

### 1. Read the whole project first

Understand its full scope before proposing any changes: WORKFLOW.txt, HANDOFF, PROJECT_INDEX, TASKS, CHANGELOG, all sub-project status/reference files, lessons, tool guides. Each project is an independent implementation and may have adapted the architecture in ways that are meaningful.

### 2. Create CLAUDE.md

Create CLAUDE.md at the project root with the startup procedure. See the [Fresh Setup](claude-code-setup.md#2-create-claudemd) section for the template. Add a compaction re-read line at the end.

### 3. Create PROJECT_CONTEXT.md from WORKFLOW.txt

Copy WORKFLOW.txt to Project/PROJECT_CONTEXT.md, then make surgical edits (do not rewrite from memory):

- Change the title line to "[PROJECTNAME] — PROJECT CONTEXT" with a fresh date and the next session number.
- **Remove** the SESSION STARTUP PROCEDURE section (now in CLAUDE.md).
- **Remove** the BASE PATH section.
- **Remove** FILESYSTEM TOOLS and COWORK DELEGATION entries from TOOL GUIDES (keep CHROME BROWSER if applicable; update its path from Workflow Files/ to Project/).
- **Update** all "Workflow Files/" references to "Project/" throughout the file.
- **Update** the SESSION LOGS naming line: "One log per session, numbered to match the session number." Change "multiple log files" to "multiple entries within the same log." Remove the KEEP LOGS CONCISE paragraph if present.
- **Remove** "and Clock" from the FRESHNESS LINES exception list.
- **Replace** the TEMPORAL AWARENESS section with the Code version (see the [PROJECT_CONTEXT template](templates/claude-code/PROJECT-CONTEXT-template.md)).
- In PROJECT CONTEXT entries: remove FILE DELETION (Chat limitation) and FILESYSTEM SCOPE (Chat limitation). Keep all domain-specific entries.
- Remove the preamble text from the PROJECT CONTEXT section ("Project-specific context and preferences not covered by...").

Remove WORKFLOW.txt after its content has been placed.

### 4. Rename Workflow Files/ to Project/

All internal references update in the same pass.

### 5. Create .claude/ configuration

See the [Fresh Setup](claude-code-setup.md#5-configure-permissions) section for the settings.json structure.

- Copy hooks from [templates/claude-code/](templates/claude-code/) (see its [README](templates/claude-code/README.md) for setup). Set the `PROJECT_NAME` constant at the top of the archiver to your project's name. Register them in settings.json.
- Create the output style file in `.claude/output-styles/` and select it in `.claude/settings.local.json`. See [output style setup](claude-code-setup.md#6-set-up-output-style-and-preferences) for the file format and frontmatter.
- Create Project/Claude Memory/ if redirecting auto memory.

### 6. Move user preferences

In Chat, user preferences live in the app's user preferences settings field. In Code, they go in `~/.claude/CLAUDE.md`, which loads into every session across all projects. Copy your preferences there. See [CLAUDE.md scoping](https://code.claude.com/docs/en/memory#choose-where-to-put-claude-md-files) for the full hierarchy.

### 7. Remove Chat-only artifacts

- Clock/ directory (replaced by temporal hook)
- Config/ directory (replaced by CLAUDE.md)
- Filesystem tools guide (Code has native access)
- Cowork delegation guide (Code does directly what Chat delegated to Cowork)
- Move Cowork directories to Archive/ if they exist

### 8. Renumber session logs to 4-digit

Session_001.txt → Session_0001.txt, etc.

### 9. Update project files

- **PROJECT_INDEX.txt** — replace WORKFLOW.txt entry with CLAUDE.md, replace Workflow Files/ tree with Project/ tree, add .claude/ directory, remove removed artifacts. Update session log naming to 4-digit.
- **CHANGELOG.txt** — add a migration entry recording the transition from Chat to Code: which sessions ran in Chat, what mechanics a reader will encounter in the old record (Filesystem connector tool calls, Cowork delegation), and what replaced them.
- Do NOT edit HANDOFF.txt — the project's first Code session writes its own.

### 10. Repoint paths if the project moved

If the project directory changed location during migration, repoint self-referential absolute paths to the new root. Exact-string replace, scoped to self-references only. Leave genuinely external paths (other projects, shared resources) unchanged — reconcile those with the user.

### 11. Fix stale references

Grep all active files (excluding Session Logs/, Sessions/, Archive/, CHANGELOG) for: "Workflow Files", "Filesystem:", "copy_file_user_to_claude", "/mnt/", "Cowork", "Clock/".

For each hit: determine if it's a functional reference (needs fixing) or historical/factual context (leave it). Fix functional references. Intentional references to leave alone: HISTORY section in PROJECT_CONTEXT, Archive entries in PROJECT_INDEX, historical descriptions in reference files, lesson files describing Chat-era behavior.

### 12. Audit

Dispatch independent read-only passes across file clusters — governing docs (CLAUDE.md, PROJECT_CONTEXT, PROJECT_INDEX, HANDOFF, TASKS), sub-project status/reference files, and lessons/tool guides — to report functional issues: broken paths, stale references to removed artifacts. Adversarially verify each finding before acting on it. Audit agents may report false positives, especially when they lack the ability to verify whether a file exists.

---

## Verification

Two-session verification:

1. **First Code session:** Confirm CLAUDE.md auto-loads, the startup procedure runs, hooks fire (time injected, prior transcript archives on next session), and the project orients correctly. Do real work to confirm continuity.
2. **Second Code session:** Confirm the archive hook captured the first session's transcript into Sessions/ with the correct name and the readable .md companion was generated.

---

## Post-Migration Refinement

Some adaptations only emerge after a project has run in Code for several sessions: trigger maps for on-demand file loading, domain-specific hooks, output style refinement, restructuring that requires live-use experience to identify. The migration gets the project running; the first few Code sessions reveal what needs fine-tuning.

---

## What Stays the Same

The architecture's core is unchanged in Code:
- A governing document as the entry point (PROJECT_CONTEXT.md in Code, WORKFLOW.txt in Chat)
- HANDOFF.txt overwritten with every log entry
- PROJECT_INDEX.txt as the structural map
- Session logs per session, sequential numbering
- Inbox as the asynchronous interface
- Sub-project activation pattern
- Fix on contact, freshness lines, evolving state
- The indexed collection pattern
- All domain content and working files

---
*Part of [AI Project Architect](https://github.com/vbiroshak/ai-project-architect) — Version 4.7*
