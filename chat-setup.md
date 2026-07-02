# Setting Up in Chat

How to build and run a project using this workspace architecture in Claude Chat using the Desktop app with the Filesystem extension. You can read [workspace-architecture.md](workspace-architecture.md) for the principles and patterns behind the system. To migrate an existing Chat project to Claude Code, see [chat-to-code-migration.md](chat-to-code-migration.md).

---

## The Chat Project Structure

```
[Project]/
  WORKFLOW.txt              startup procedure, project
                            description, temporal awareness,
                            logging guidance, project context.
                            Only what earns its place in every
                            context window.
  Inbox/                    asynchronous interface, both
                            directions (see below)
  Workflow Files/           all project infrastructure
    HANDOFF.txt             current state,
                            priorities, reading pointers.
                            Overwritten with every log entry.
    PROJECT_INDEX.txt       file structure index.
                            Read at startup with HANDOFF.
    TASKS.txt               optional — active items only, no
                            DONE section. Read at startup for
                            projects that use one.
    Clock/timestamp.txt     temporal awareness
    Config/
      PROJECT_INSTRUCTIONS.txt  backup for portability, synced at startup
    Lessons/                optional — operational knowledge
      LESSONS_INDEX.txt     routing index
      [topic].txt           one file per topic
    Session Logs/           project-wide, on-demand
      Session_XXXX.txt      4-digit, one per session, sequential
  [Sub-Project A]/          functional area
    [SubProj]_STATUS.txt    orientation (current state)
    [SubProj]_REFERENCE.txt domain knowledge (on demand)
    [named domain files]    shaped by the work
    [domain folders]        shaped by the work
  [Sub-Project B]/          ...
```

The root shows: what the project does (sub-project folders), the entry point (WORKFLOW.txt), user-facing interaction (Inbox/), and infrastructure tucked away (Workflow Files/).

---

## Fresh Setup

### 1. Create the project directory

The minimum a Chat project needs: WORKFLOW.txt at the root, Workflow Files/ (with HANDOFF.txt, PROJECT_INDEX.txt, Clock/timestamp.txt, Config/PROJECT_INSTRUCTIONS.txt, Session Logs/), Inbox/, and at least one sub-project folder. Create Clock/timestamp.txt with any content (e.g., "tick") — the AI overwrites it at each clock check and reads the modification timestamp. The [mandated file templates](templates/mandated-files/) provide the starting content for each infrastructure file.

### 2. Set up project instructions

Paste these into your AI application's project settings field. The path is the only variable.

```
Workspace: All project files live on the filesystem at [path]. You have
Filesystem tools that give you full access to this directory and everything
inside it, including reading, writing, creating, editing, searching, and
moving files and directories. At session startup, use these tools to read
WORKFLOW.txt at the project path and follow its procedures.

When Filesystem tools are not available, let the user know and explain that
the session will operate from project memory and conversation context.
Capabilities will be limited. Remember any work that should be logged or
written to the filesystem per your workflow instructions, and do so when
these tools become available again.
```

The user pastes this once and never updates it. All evolution happens in filesystem files that the AI maintains directly.

A backup copy lives in the workspace at Config/PROJECT_INSTRUCTIONS.txt, synced automatically at startup (step 2). This makes the project fully portable: everything needed to recreate the project in a new account, on a different device, or for another person lives on the filesystem.

The instructions describe capabilities using verbs (reading, writing, creating, editing, searching, moving) rather than naming specific tools. This means tool updates don't require instruction changes. The first block asserts what the tools can do and commands an action: read WORKFLOW.txt. The fallback block handles sessions where the tools are absent (web, mobile).

### 3. Build WORKFLOW.txt

WORKFLOW.txt is the governing document — the only file read in every context window. Assemble it from the [workflow section templates](templates/workflow-sections/) in the order prescribed by the section registry below. Universal sections deploy verbatim; project-specific sections use the template structure with your project's content.

### 4. Set up user preferences

User preferences (interaction style, formatting rules, behavioral constraints) are injected automatically from the AI application's settings field. Content already in user preferences should not be duplicated in WORKFLOW.txt's Project Context section.

### 5. Verify

Start a real session. Confirm the AI reads WORKFLOW.txt, runs the startup procedure, checks the clock, reads the handoff and session log, and lists the inbox. Do real work in the first session to confirm continuity.

---

## The Startup Procedure

Startup reads seven things, in an order where each step builds on the context established by the previous ones:

1. **Confirm Filesystem tools loaded for essential operations** — these are the foundation for every step that follows. Tool discovery mechanisms may return narrow results for per-verb queries and miss sibling operations, so use broad queries covering the full set.
2. **Read Workflow Files/Config/PROJECT_INSTRUCTIONS.txt.** If it differs from the project instructions in context, update the file to match. This keeps the backup current for project portability and recreation.
3. **Check the clock and time since last logged interaction** (see Temporal Awareness) — establishes temporal frame before any project state loads
4. **Workflow Files/PROJECT_INDEX.txt and Workflow Files/HANDOFF.txt** — PROJECT_INDEX gives structural context (what exists, where), HANDOFF gives state context (what's happening, what to read next)
5. **Most recent session log in Workflow Files/Session Logs/**, plus any additional logs the handoff identifies.
6. **Project-level task queue**, if the project uses one. Fix any completed items on the spot. Sub-project or function-specific queues load at activation, not startup.
7. **Inbox/ listing** (filenames only) — last, because inbox items could be from any time and benefit from having all project state loaded first

The clock check comes early because temporal context informs how everything after it is read. Knowing whether the last logged interaction was an hour ago or three days ago changes how the handoff and session log land. The handoff gives the current state snapshot; the session log(s) give the narrative. Together they orient a fresh chat to continue the work with both the snapshot and the story. The inbox is listed last because having the full project state loaded first enables recognition of how inbox items connect to existing work.

When writing a handoff after structural or meta work, note which earlier session contains the last domain work. The startup log may be about structural changes, not the actual work.

For projects with multiple sub-projects, each area's section in the handoff should include a "last active" pointer: the session number where that area was last worked, and the sub-project reference file to read. This prevents sub-projects from becoming unresurfaceable when other areas dominate the work.

---

## The WORKFLOW Section Registry

WORKFLOW.txt sections should be standardized across all projects to maintain a consistent baseline. If you're running multiple projects, designate one as the owner of the canonical section list, ordering, and mechanical text.

Before adding a section to a WORKFLOW, check the registry. If the content fits an existing section, put it there. If no section fits and the content genuinely needs to be in every context window, evaluate it as a potential registry expansion.

A baseline registry with 12 sections in fixed order:

| # | Section | Status |
|---|---------|--------|
| 1 | Session Startup Procedure | Universal |
| 2 | Base Path | Project-specific |
| 3 | Tool Guides | Universal |
| 4 | What This Project Does | Project-specific |
| 5 | Sub-Project Activation | Universal pattern, project-specific pointers |
| 6 | Task Queue | Optional |
| 7 | Session Logs | Universal |
| 8 | Handoff | Universal |
| 9 | Temporal Awareness | Universal |
| 10 | Inbox | Universal |
| 11 | Shared Knowledge Base | Universal (if running multiple projects) |
| 12 | Project Context | Project-specific |

Universal sections carry identical mechanical text across all projects. Project-specific sections use the same heading and position but carry project-specific content. Optional sections are included only when needed. If you are an AI building this for a user, ask the user about each optional and project-specific section and explain what it does so they can make an informed decision.

For the actual deployable text of each section, see the [workflow section templates](templates/workflow-sections/).

### Section Descriptions

**Session Startup Procedure** — The seven-step startup sequence: confirm Filesystem tools loaded, sync config backup, check the clock and time since last logged interaction, read PROJECT_INDEX and HANDOFF, read the most recent session log plus any additional logs the handoff identifies, read task queue if present, list Inbox. Identical across all projects.

**Base Path** — The project's filesystem root. One line.

**Tool Guides** — Required guides to read before using specific tools, listed with hard preconditions (read the guide before loading or using the tool). Standard entries: Chrome browser, Filesystem tools, Cowork delegation. Projects adopt only the guides relevant to their work; entries for unused tools are omitted.

**What This Project Does** — Brief project description and current sub-project list with one-line descriptions. Updated when sub-projects are added or archived.

**Sub-Project Activation** — Three-step activation pattern: read reference file, read everything the handoff identifies for that sub-project, load additional files as needed. Loading depth varies by sub-project and is governed by the handoff's pointers. When reading a sub-project's status file, verify it is consistent with the handoff and fix discrepancies on the spot (see Fix on Contact in [workspace-architecture.md](workspace-architecture.md#fix-on-contact)). Universal pattern with project-specific reference file pointers. Also establishes the write direction: domain knowledge produced during work goes into files inside the sub-project directory, not PROJECT_INDEX.txt. Every sub-project listed must have a reference file; if the directory exists, a seeded file exists.

**Task Queue** — For projects that use a task queue. Standard location: Workflow Files/TASKS.txt. Active items only (no DONE section), read at startup, add immediately when items arise, remove on completion and note in session log. Include only in projects that maintain a task queue file.

**Session Logs** — Logging mechanics. One log per session, numbered to match the session number. Write when substantive work accumulates; never defer to end of session. Multiple distinct topics go in multiple entries within the same log. Paired writes with HANDOFF (including freshness lines). Structure changes trigger PROJECT_INDEX.txt verification. Fix on contact for stale information. Evolving state: log topics at current progress, not binary. Freshness line definitions and maintenance rules. Identical across all projects.

**Handoff** — The handoff is the orientation; session logs are the archive. Current state snapshot: where things stand, what to read for depth. Overwritten fresh with each paired write. Three sections: ACTIVE WORK (each item on its own line with current state), STANDING ITEMS (paused but ongoing work, one item per line), FOR DEPTH (which session logs to read). Scope is limited to what the next session needs to continue the work — rules, operating knowledge, and reference facts belong in governing documents; completed work belongs in the session log. Identical across all projects.

**Temporal Awareness** — Clock mechanism and two check points: at startup (current time + time since last interaction) and mid-chat (detect gaps when the human returns to a continuing chat after hours or days). Identical across all projects.

**Inbox** — Asynchronous interface between the user and the project, both directions. The user drops files for processing; the AI writes drafts, deletion flags, delegation notes, or anything needing the user's attention. Processing guidance: list the directory before any reference to inbox contents (startup, mid-session, handoff writing), read on demand, check existing project structure before assessing items. Identical across all projects.

**Shared Knowledge Base** — Path and one-line description. Identical across all projects. Include only when running multiple projects that share patterns and knowledge; a single-project setup omits this section.

**Project Context** — Project-specific material earning its place in every context window but not covered by account-wide user preferences. Domain context, operational conventions. Accumulates through use. A file deletion convention is always present as a seed entry (the AI cannot delete files in Chat — it moves items to Inbox/ with "DELETE ME" at the front). Content already in account-wide preferences should not be duplicated here. File structure documentation belongs in PROJECT_INDEX.txt, not here.

A routing flowchart for new content:

- Needed every session, project-specific context → **Project Context** section
- Needed every session, mechanical/procedural → check the registry for an existing section
- Applies to all projects, behavioral/personal → account-wide user preferences
- Needed only when working a specific sub-project → sub-project reference file
- File structure documentation → PROJECT_INDEX.txt
- Domain knowledge for a specific sub-project → a file inside the sub-project directory (PROJECT_INDEX.txt points to it, does not hold it)
- New section type not in the registry → evaluate for registry expansion

---

## Temporal Awareness

AI assistants have no internal clock and cannot estimate, infer, or guess the time. Temporal awareness is a continuous behavior with two components:

1. **What time is it now?**
2. **How long has it been since the last known time reference?**

The mechanism uses a persistent Clock file (Workflow Files/Clock/timestamp.txt) and filesystem metadata. Create this file with any content — the AI overwrites it each time it checks the clock, then reads the file's modification timestamp. The file is permanent and reusable. Never delete it. On macOS, only the "modified" field is reliable — the "created" field is the file's birth time and never updates.

The clock is checked at two points: at startup (step 3), and mid-chat before the first filesystem operation in each response. The startup check establishes the current time and calculates time since the last logged interaction. The mid-chat check detects gaps when the human leaves a continuing chat and returns hours or days later. Without the mid-chat check, the AI's only time reference is its startup reading, and it will fabricate timestamps when that reading goes stale.

Each project's WORKFLOW.txt carries the implementation steps. See the [temporal awareness workflow section template](templates/workflow-sections/temporal-awareness.md) for the deployable text.

For the design rationale behind this approach, see the [Temporal Awareness](patterns/temporal-awareness.md) pattern.

---

## Adopting for Existing Projects

If you have an existing unstructured project to migrate into this architecture:

1. Create a sub-project folder for the current work and move domain-specific files into it
2. Create Workflow Files/ and move Clock/, Config/, Session Logs/ into it
3. Create Workflow Files/HANDOFF.txt and PROJECT_INDEX.txt
4. Ensure Inbox/ stays at root
5. Rewrite WORKFLOW.txt: lean version with handoff-driven startup procedure
6. Add freshness lines (Last updated, Last reviewed) to all files created in steps 1-5. See [Freshness Tracking](workspace-architecture.md#freshness-tracking).
7. Simplify project instructions to match the template in Set up project instructions above
8. Update Config backup to match

---

## Known Limitations

**Filesystem extension required.** Requires the Claude Desktop app with the Filesystem extension (macOS and Windows). Web and mobile interfaces don't have filesystem access. When accessing a project chat in mobile or web, Claude will note what needs syncing when next opened in the Desktop app.

**Chat search is typically project-scoped.** Built-in chat search usually only sees conversations within the current project. It will never find anything from another project. The filesystem spans everything — when you need cross-project context, the AI reads the other project's files directly.

**File deletion.** The AI cannot delete files in Chat. It moves items to Inbox/ with "DELETE ME" at the front. The user handles the actual deletion.

---
*Part of [AI Project Architect](https://github.com/vbiroshak/ai-project-architect) — Version 4.6*
