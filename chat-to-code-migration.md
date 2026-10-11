# Migrating from Chat to Code

This guide is written for the AI that migrates the project; the person who owns the project reads the [README](README.md). It covers only the migration-specific work: how to get a project from Claude Chat into Claude Code. The target state, what a Code project looks like, is in [claude-code-setup.md](claude-code-setup.md).

---

## Starting a Migration

The migration runs in a Claude Code session; where that session runs, and what follows from it, is in [Setting Up the Migration Session](#setting-up-the-migration-session). The user says they are moving a Chat project and where its files are. Ask if they have not said. The path depends on the project's files.

**The project has a folder on the user's computer with a WORKFLOW.txt in it.** It was built with this system. Convert the project in place, following this guide from [Setting Up the Migration Session](#setting-up-the-migration-session) onward.

**The project has a folder on the user's computer with no WORKFLOW.txt.** The files stay in that folder and the project structure is built around them. Follow [Adopting for existing projects](claude-code-setup.md#adopting-for-existing-projects) in the setup guide.

**The project has no folder on the user's computer.** Its instructions and files are in the user's Claude account. Ask the user where the project's folder should be, and build a new project there, following [claude-code-setup.md](claude-code-setup.md).

On every path, parts of the project are still in the user's Claude account. A data export brings them to the computer (see [The data export](#the-data-export)); ask the user for it, and incorporate:

- **Conversations.** See [Transcript Processing](#transcript-processing).
- **Instructions, documents, and memory.** See [Project Data in the Export](#project-data-in-the-export). If the user has the original files of documents added to the Chat project, ask for them in the project's Inbox/ folder.
- **User preferences.** These are not in the project. See [Move user preferences](#6-move-user-preferences).

---

## What a Chat Project Built with This System Contains

The layout this guide converts:

```
[Project]/
  WORKFLOW.txt              governing document: startup procedure,
                            project description, logging guidance,
                            project context
  Inbox/
  Workflow Files/           project infrastructure
    HANDOFF.txt
    PROJECT_INDEX.txt
    TASKS.txt               (if the project uses a task queue)
    Clock/timestamp.txt     time source
    Config/
      PROJECT_INSTRUCTIONS.txt
    Lessons/                (if used)
    Tool Guides/            (if used)
    Session Logs/           one log file per session
  [Sub-Project A]/
    [SubProj]_STATUS.txt
```

WORKFLOW.txt is the governing document and carries the startup procedure. The instructions in the Chat project's settings tell the AI to read it at the start of every session; Config/PROJECT_INSTRUCTIONS.txt is a backup copy of those instructions. The Clock file is the time source: the AI writes to it and reads its modification time.

---

## Setting Up the Migration Session

A project's sessions are the ones run in its own folder (see [Concise Logging](workspace-architecture.md#concise-logging)). The README tells the user to run the migration from a session outside the project's folder: a session in any other folder, or a session of another Code project, such as a coordinator project. That session is not one of the project's sessions, so the project's next Code session is the next number in its sequence and continues where Chat left off. The steps below are written for this case: the migration leaves the project's handoff alone and leaves no transcript in the project. The repo's files can be anywhere the session can read them, the project's own folder included.

A session running in the project's own folder can also do the migration. Tell the user why a session outside the folder is better before going on. If the user goes on, the session is one of the project's sessions: it takes the next number in the project's sequence, writes that session's log and the handoff as any session does (principle 11 and the handoff line in step 9 do not apply), and its transcript is archived at the next session's start. The Verification section at the end of this guide says what each case changes.

Point the session at the live project path and rebuild in place. Back up the project directory first as a safety net. Once the project's next session confirms everything works, the backup can be archived or deleted.

---

## Principles

Hold all of them.

1. **Surgical and minimal.** Change only what the Code harness actually breaks, or what the user directs. Preserve existing text and meaning; never reword or translate prose while fixing a problem.
2. **No system-contrast commentary.** Files read as the system itself, not as a migration story. No "instead of," "unlike Chat," "now in Code." State any new mechanism plainly, as if the file always said it.
3. **State the action, not the tool.** Strip instructions that prescribe specific connector tool calls (e.g., "use Filesystem:list_directory"); leave the action and the discipline.
4. **One home, no duplication.** Each fact lives in exactly one file. CLAUDE.md replaces Config/PROJECT_INSTRUCTIONS.txt; don't keep both.
5. **Capability preserved, mechanism adapted.** The system still does everything it did; only the mechanism changes where Code differs from Chat. A Chat project with temporal awareness through a Clock file gets it through a hook.
6. **Complete the reference chain.** Every move, deletion, or rename updates all references in the same pass. No deferred fixes.
7. **Functional vs. cosmetic.** Fix what would break or misdirect operation: a path that doesn't resolve, a reference to something deleted, a tool call Code lacks. Ignore cosmetic drift such as a count off by one: normal sessions correct it, and the migration is not a general cleanup.
8. **Freeze the historical record.** Session logs, archived transcripts, the Archive folder, and dated CHANGELOG entries preserve old references as history. Never rewrite them.
9. **No propagating artifacts.** Don't introduce a non-standard section or pattern (e.g., a "Migration Notes" section in the handoff) that a future session would replicate forever. Put facts into the body of existing sections.
10. **Copy, then edit.** When setting up hooks, copy the scripts from [templates/claude-code/](templates/claude-code/) and change only the project name. Don't rewrite from memory.
11. **Don't edit the migrated project's handoff.** A migration run from a session outside the project's folder is not one of the project's sessions; the project's next session writes its own handoff. (A migration run in the project's own folder is one of its sessions and writes the handoff as any session does; see [Setting Up the Migration Session](#setting-up-the-migration-session).)

---

## Transcript Processing

If the project has Chat session history worth preserving, process the transcripts before the structural changes; a project with little history can skip to the structural migration.

Before starting, verify the transcript count matches the project's known Chat session count. Mismatches (gaps, duplicates, unnamed conversations) are easier to resolve before alignment than after.

### The data export

The user requests the export from the Claude app's settings; see Anthropic's [Export your Claude data](https://support.claude.com/en/articles/9450526-export-your-claude-data). The download is either a single archive or a small manifest file that lists several archives (conversations, projects, memories, and others), each with its own link. If it is a manifest, every archive it lists must be downloaded promptly, because the links expire. Ask the user to unzip everything into one folder.

The folder holds `conversations.json`, which bundles all conversations across all projects into a single file; an entry for each project, with its name, instructions, and documents; and the saved memory, including each project's memory under the project's ID. Projects do not reference their conversations, and conversations do not carry a project identifier. The most reliable way to associate a conversation with its project is by the conversation's `name` field.

The export also holds account-wide memory that belongs to no project, and account files (`users.json`, `login_history.json`) with contact details and IP addresses. No project needs the account files; leave them in the export.

Conversations deleted in Chat may still appear in the export as empty shells (no text, tool calls, or attachments); ignore them.

### Splitting by project

`split_export.py` (in [templates/claude-code/](templates/claude-code/)) reads `conversations.json`, identifies each conversation's project from its `name` field (pattern: "ProjectName N"), and writes individual `.json` files named with the 4-digit convention (`ProjectName_0042.json`) into a staging directory organized by project. It reports per-project counts, gaps, and duplicates.

Before running, edit the `KNOWN_PROJECTS` list at the top of the script with the user's project names — the script matches conversation names only against that list, so run as shipped it matches nothing.

Usage: `python3 split_export.py <batch-dir> <output-dir> [--project ProjectName] [--dry-run]` (on Windows, invoke with `python` or `py -3` instead of `python3` — here and in the commands below)

The script matches integer-named conversations ("MyProject 42" → `MyProject_0042.json`) and decimal-named ones ("MyProject 1.4" → `MyProject_1.4.json`, the form the archive hook gives such sessions in Code). Unnamed conversations are counted but not written unless `--include-unnamed` is passed. Conversations whose number collides with one already written are quarantined into `_duplicates/` for manual resolution.

### Converting to readable Markdown

`chat_export_to_md.py` (in [templates/claude-code/](templates/claude-code/)) converts each individual `.json` into a collapsed-view `.md` — the readable companion. Human messages render as `## User`, assistant messages as `## Claude`. Tool calls render as `→ name` lines. Tool results, token_budget blocks, and whitespace-only text blocks are omitted. Thinking renders as blockquoted reasoning.

The script reads each message's structured `content` blocks, not the flattened `text` field, which can hold "This block is not supported on your current device yet" placeholders where tool calls should be.

Usage: `python3 chat_export_to_md.py <directory>` converts every `.json` in the directory.

### Verification

After conversion, verify:
- Zero "This block is not supported" strings in any `.md`
- `→ ` lines present (tool calls survived)
- `## User` / `## Claude` headers (not a personal name)
- No `tool_result` content leaked through

### Naming, numbering, and alignment

Session logs are the canonical navigation system. Logs keep their original sequential numbers, padded to four digits; a log is never renamed so that its filename no longer matches the session number inside it and in cross-references, because that breaks every reference to the session.

Transcripts are named to match their primary log number: the first log a chat wrote determines the transcript's number. To find which log each chat wrote, extract the write events from the transcripts mechanically (look for calls to the file-writing tool that target Session Logs/; its name ends in `write_file`, and the prefix in front of it varies). The filename in a write event is the log's name at the time it was written; if the project has renumbered its logs since, match the event to the current log by the log's title line and entry dates, not by filename.

**Write out the full alignment plan before executing.** Map every transcript to its destination number. Verify the plan at sample points before renaming anything. Renaming without a plan leads to cascading corrections.

**Use a temp directory for renames** to avoid collisions when old and new numbers overlap (e.g., transcript 5 needs to become 3, but transcript 3 hasn't moved yet). Copy to temp, then from temp to final names.

**Never delete transcripts without reading them.** A session with a proper opener is a real session even if it didn't write a log. Only empty transcripts (no content at all) are excluded. If a rename script also deletes, run the deletes on the original filenames before the renames, or newly renamed files at the same numbers get caught.

The naming conventions:

- **1:1 sessions** — transcript gets the log number.
- **Multi-log sessions** (one chat wrote multiple logs) — the transcript gets the first log number. Each secondary log gets a pointer line at the bottom: "Session transcript: Project/Sessions/ProjectName_NNNN" linking to the transcript for that chat. Only needed where the log number differs from the transcript number.
- **Pre-log transcripts** (sessions before the project had logging) — name them ProjectName_0000a through ProjectName_0000x. These sort before 0001 and letters give sequence.
- **No-log sessions** (sessions that didn't write a log) — name the transcript by position in the log timeline: the last log number before them + letter suffix (e.g., between logs 010 and 011 → ProjectName_0010b).

### Placing transcripts

Create Project/Sessions/ (or Workflow Files/Sessions/ if placing before the directory rename). Copy both the `.json` and `.md` files. The `.json` is the canonical record; the `.md` is the readable companion.

Going forward in Code, the archive hook names transcripts from `/rename` (checked first) or the "This is ProjectName NNN" session opener (fallback). Number-named sessions are formatted as `ProjectName_NNNN.jsonl`. The project's next session number = last log number + 1; the user types that number in the opener, so tell the user the exact opener when the migration is done. A migration run from a session outside the project's folder leaves no transcript in the project; one run in the project's own folder is archived at the next session's start like any session.

---

## Project Data in the Export

Besides the conversations, the export holds data that belongs to the project: its instructions, the documents added to it, and what Claude's memory saved for it. Find the project's entry in the export by the project's name and note its ID; the memory is filed under that ID. Incorporate all three; nothing the project needs stays only in the export.

**Instructions.** In a project built with this system, the instructions only point to WORKFLOW.txt; CLAUDE.md replaces them and nothing is carried over. In any other project they are the project's real instructions. What describes the work goes into PROJECT_CONTEXT.md (WHAT THIS PROJECT DOES and the PROJECT CONTEXT entries). How the AI should behave goes into the output style. Ask the user where an instruction's place is unclear.

**Documents.** Write each document into the sub-project it belongs to, under its original filename, and list it in that sub-project's status file. Where the project folder already holds the document, keep the project's copy.

**Memory.** A memory entry is not evidence that its claim is true or still current. The export can hold the same memory twice, as one older block of text and as newer separate files; treat the newer as current. Work through the project's memory one item at a time; an entry that holds several facts or rules is several items. For each item:

- If a file the project loads already states it, write nothing.
- If it is knowledge about the work, write it into the sub-project file where it belongs.
- If it is the state of some piece of work, compare it with the handoff, status files, and latest session log. Where they are newer, they govern and the item is dropped.
- If it is a rule for the whole project, write it into the PROJECT CONTEXT entries.
- If it describes how the Chat setup worked (tool names, the clock file, working without file access), drop it.
- If it is incidental, or cannot be confirmed against the project's own record, drop it.

A memory file that is itself a session log (some Chat projects kept their logs in memory) is not an item: it becomes a file in Session Logs/, numbered to match the chat that wrote it, body kept verbatim.

Keep a short record of where each item went, and keep the project's own entries from the export's memory file in the project's Archive/ as the original; the file holds every project's memory.

---

## The Structural Migration

The target state for each file is described in [claude-code-setup.md](claude-code-setup.md). This section covers how to get there from the Chat layout.

### 1. Read the whole project first

Understand its full scope before proposing any changes: WORKFLOW.txt, HANDOFF, PROJECT_INDEX, TASKS, CHANGELOG, all sub-project status/reference files, lessons, tool guides. Each project is an independent implementation and may have adapted the architecture in ways that are meaningful. Note any library or tool the lessons and tool guides assume: the Chat environment had some preinstalled (Python packages, for example) that the user's machine may not have.

### 2. Create CLAUDE.md

Create CLAUDE.md at the project root from the [CLAUDE.md template](templates/claude-code/CLAUDE-template.md), which holds the startup procedure and the compaction re-read line.

### 3. Create PROJECT_CONTEXT.md from WORKFLOW.txt

Copy WORKFLOW.txt to Project/PROJECT_CONTEXT.md, then make surgical edits (do not rewrite from memory):

- Change the title line to "[PROJECTNAME] — PROJECT CONTEXT" with a fresh date and the next session number.
- **Remove** the SESSION STARTUP PROCEDURE section (now in CLAUDE.md).
- **Remove** the BASE PATH section.
- **Remove** the FILESYSTEM TOOLS and COWORK DELEGATION entries from TOOL GUIDES. Keep entries for guides the project still uses, updating their path from Workflow Files/ to Project/; remove the section if none remain.
- **Update** all "Workflow Files/" references to "Project/" throughout the file.
- **Update** the SESSION LOGS naming line: "One log per session, numbered to match the session number." Change "multiple log files" to "multiple entries within the same log." Remove the KEEP LOGS CONCISE paragraph if present.
- **Remove** "and Clock" from the FRESHNESS LINES exception list.
- **Replace** the TEMPORAL AWARENESS section with the Code version (see the [PROJECT_CONTEXT template](templates/claude-code/PROJECT-CONTEXT-template.md)).
- **Add** the SESSION NUMBER entry after the Naming line in SESSION LOGS, from the template, with the session-naming form the user chose (README question 9).
- **Add** the SESSION CLOSE section after HANDOFF, from the template.
- In PROJECT CONTEXT entries: remove FILE DELETION (Chat limitation), FILESYSTEM SCOPE (Chat limitation), and any entry about Chat's memory feature (Code's memory is a different feature; instructions written for Chat's do not transfer). Keep all domain-specific entries.
- Remove the preamble text from the PROJECT CONTEXT section ("Project-specific context and preferences not covered by...").

Remove WORKFLOW.txt after its content has been placed.

### 4. Rename Workflow Files/ to Project/

All internal references update in the same pass.

### 5. Create .claude/ configuration

See the [Fresh Setup](claude-code-setup.md#5-configure-permissions) section for the settings.json structure.

- Copy hooks from [templates/claude-code/](templates/claude-code/) (see its [README](templates/claude-code/README.md) for setup). Set the `PROJECT_NAME` constant at the top of the archiver to the project's name. Register them in settings.json.
- Create the output style file in `.claude/output-styles/` and select it in `.claude/settings.local.json`. See [output style setup](claude-code-setup.md#6-set-up-output-style-and-preferences) for the file format and frontmatter.
- If the user chose the session close skill (README question 6), copy [templates/claude-code/skills/handoff/](templates/claude-code/skills/handoff/) to `.claude/skills/handoff/`.

### 6. Move user preferences

In Chat, user preferences live in the app's user preferences settings field. In Code, they go in `~/.claude/CLAUDE.md`, which loads into every session across all projects. Ask the user for the text of that field and write it there. See [CLAUDE.md scoping](https://code.claude.com/docs/en/memory#choose-where-to-put-claude-md-files) for the full hierarchy.

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
- Do NOT edit HANDOFF.txt from a session outside the project's folder — the project's next session writes its own (principle 11).

### 10. Repoint paths if the project moved

If the project directory changed location during migration, repoint self-referential absolute paths to the new root. Exact-string replace, scoped to self-references only. Leave genuinely external paths (other projects, shared resources) unchanged — reconcile those with the user.

### 11. Fix stale references

Grep all active files (excluding Session Logs/, Sessions/, Archive/, CHANGELOG) for: "Workflow Files", "Filesystem", "write_file", "copy_file_user_to_claude", "/mnt/", "container", "remote-devices", "Cowork", "Clock/".

For each hit: determine if it's a functional reference (needs fixing) or historical/factual context (leave it). Fix functional references. Intentional references to leave alone: HISTORY section in PROJECT_CONTEXT, Archive entries in PROJECT_INDEX, historical descriptions in reference files, lesson files describing Chat-era behavior.

### 12. Audit

Dispatch independent read-only passes across file clusters — governing docs (CLAUDE.md, PROJECT_CONTEXT, PROJECT_INDEX, HANDOFF, TASKS), sub-project status/reference files, and lessons/tool guides — to report functional issues: broken paths, stale references to removed artifacts. Verify each finding before acting on it: audit agents report false positives, especially when they cannot check whether a file exists.

---

## Verification

The checks run in the project's own sessions, which the migration session is not when it runs outside the project's folder; give the checks to the user together with the opener for the project's next session.

1. **The project's next session**, the next number in its sequence: Confirm CLAUDE.md auto-loads, the startup procedure runs, hooks fire (time injected, prior transcript archives on next session), and the project orients correctly. Do real work to confirm continuity.
2. **The session after it:** Confirm the archive hook captured the previous session's transcript into Sessions/ with the correct name and the readable .md companion was generated.

When the migration ran in the project's own folder, it was one of the project's sessions, and the next session checks both items: its start archives the migration session.

---

## Post-Migration Refinement

Some adaptations emerge only after several Code sessions: trigger maps for on-demand loading, domain-specific hooks, output style refinement, restructuring that live use reveals. The migration gets the project running; the first Code sessions show what to fine-tune.

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
*Part of [AI Project Architect](https://github.com/vbiroshak/ai-project-architect) — Version 4.11*
