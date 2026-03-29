# Workspace Architecture for Sustained Knowledge Work with AI

Version 4.0

A workspace architecture optimized for context cost and continuity.

Developed through iterative design and daily use across multiple projects spanning different domains. Applicable to any project where an AI assistant serves one or more areas of ongoing work.

---

## The Problem

Default AI project tools aren't designed for sustained knowledge work. Project knowledge files are static uploads. There is no session continuity: each conversation starts blank. There is no mechanism for the AI to maintain its own documentation, log sessions, or orient itself in ongoing work.

The workspace pattern solves this by moving project knowledge to a living filesystem that the AI reads, writes, and maintains directly. But the workspace itself must be designed to work within context window constraints. Every file read at startup stays in context for the entire conversation and is retokenized every turn. A 50 KB startup across 20 turns means the startup content is processed roughly 20 times.

This document describes a workspace architecture that balances orientation quality against context cost.

---

## The Structure

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
    REFERENCE.txt           file structure, format specs,
                            procedures, sub-project pointers.
                            Read at startup with HANDOFF.
                            Not a container for domain knowledge.
    TASKS.txt               optional — active items only, no
                            DONE section. Read at startup for
                            projects that use one.
    Clock/timestamp.txt     temporal awareness
    Config/
      PROJECT_INSTRUCTIONS.txt  backup for portability, synced at startup
    Lessons/                operational knowledge
      LESSONS_INDEX.txt     routing index
      [topic].txt           one file per topic
    Session Logs/           project-wide, on-demand
      Session_XXX.txt       per unit of work, sequential
  [Sub-Project A]/          functional area
    [SubProj]_STATUS.txt    orientation (current state)
    [SubProj]_REFERENCE.txt domain knowledge (on demand)
    [named domain files]    shaped by the work
    [domain folders]        shaped by the work
  [Sub-Project B]/          ...
```

The root shows: what the project does (sub-project folders), the entry point (WORKFLOW.txt), user-facing interaction (Inbox/), and infrastructure tucked away (Workflow Files/). That's it.

---

## The Inbox

Inbox/ at the project root is the asynchronous interface between the user and the project, in both directions.

The user drops files here between sessions: emails saved as text, documents to process, screenshots, reference material, delegation briefs, anything that a project needs to see. The project notices them at startup and asks about them.

The AI writes to the Inbox when it has something for the user: drafts for review, items flagged for deletion, cross-project delegation notes, or anything that needs the user's attention outside the current conversation.

This is a foundational workflow in both directions. The user encounters something relevant, saves it to the appropriate project's inbox, and moves on. The AI produces a draft or flags a file and places it in the inbox for the user to find. The inbox bridges the gap between when work arrives and when the project is active, regardless of which direction it flows.

Inbox items are listed (filenames only) at startup as step 7. They are not read at startup. The listing surfaces what's waiting, and the chat processes items when directed or when relevant to the session's work.

Inbox contents can change at any time between messages. See Inbox: Verify and Check Before Referencing in Key Principles for the verification procedure.

Inbox items may represent undocumented task entries, work that has arrived but hasn't been triaged into the project's task list or session log. If you use a coordinator project (see Knowledge Architecture below), its task review should include inbox listings for this reason.

---

## Startup

Startup reads seven things, in an order where each step builds on the context established by the previous ones:

1. **WORKFLOW.txt**
2. **Read Workflow Files/Config/PROJECT_INSTRUCTIONS.txt.** If it differs from the project instructions in context, update the file to match. This keeps the backup current for project portability and recreation.
3. **Check the clock and time since last logged interaction** (see Temporal Awareness) — establishes temporal frame before any project state loads
4. **Workflow Files/REFERENCE.txt and Workflow Files/HANDOFF.txt** — REFERENCE gives structural context (what exists, where), HANDOFF gives state context (what's happening, what to read next)
5. **Most recent session log in Workflow Files/Session Logs/**, plus any additional logs the handoff identifies.
6. **Project-level task queue**, if the project uses one. Fix any completed items on the spot. Sub-project or function-specific queues load at activation, not startup.
7. **Inbox/ listing** (filenames only) — last, because inbox items could be from any time and benefit from having all project state loaded first

The clock check comes early because temporal context informs how everything after it is read. Knowing whether the last logged interaction was an hour ago or three days ago changes how the handoff and session log land. The handoff gives the current state snapshot: where things stand per functional area, priorities, what to read for depth. The session log(s) give the narrative: how things got to the current state, what was tried, what was decided and why. Together they orient a fresh chat to continue the work with both the snapshot and the story. The inbox is listed last because its items may be old or new, and having the full project state loaded first enables recognition of how inbox items connect to existing work.

The session log was added back after testing showed that handoff-only startup lost narrative continuity. A chat reading only the handoff knew what the current state was but not how it got there, causing it to fall back on stale memory and past chat search. One session log restores the narrative thread at modest cost while significantly reducing context load compared to reading multiple logs at startup.

When writing a handoff after structural or meta work (like project optimization or file reorganization), note which earlier session contains the last domain work. The startup log may be about structural changes, not the actual work. The handoff pointer lets the chat load the domain narrative.

For projects with multiple sub-projects or functional areas, each area's section in the handoff should include a "last active" pointer: the session number where that area was last worked, and the sub-project reference file to read for full state. This prevents sub-projects from becoming unresurfaceable when other areas dominate the work for extended periods. The FOR DEPTH section at the bottom of the handoff naturally scrolls past older sessions, but the sub-project pointer persists as long as the section exists.

Example:

```
RESEARCH — LITERATURE REVIEW
Next: finish annotating the second batch of sources.
Last active: Session 012. For full state, read
  Research/RESEARCH_STATUS.txt.
```

Once oriented, the chat loads additional session logs, sub-project reference files, lessons, and task queues on demand.

The user already knows their project. They need orientation (where we left off, what's pending), not education (what each item is about).

---

## WORKFLOW Section Registry

WORKFLOW.txt is the only file read in every context window. Its sections should be standardized across all projects to maintain a consistent baseline. If you're running multiple projects, designate one as the owner of the canonical section list, ordering, and mechanical text.

Before adding a section to a WORKFLOW, check the registry. If the content fits an existing section, put it there. If no section fits and the content genuinely needs to be in every context window, evaluate it as a potential registry expansion. Don't invent WORKFLOW sections ad hoc within individual projects.

A baseline registry with 10 sections in fixed order:

| # | Section | Status |
|---|---------|--------|
| 1 | Session Startup Procedure | Universal |
| 2 | Base Path | Project-specific |
| 3 | What This Project Does | Project-specific |
| 4 | Sub-Project Activation | Universal pattern, project-specific pointers |
| 5 | Task Queue | Optional |
| 6 | Session Logs | Universal |
| 7 | Temporal Awareness | Universal |
| 8 | Inbox | Universal |
| 9 | Shared Knowledge Base | Universal |
| 10 | Project Context | Project-specific |

Universal sections carry identical mechanical text across all projects. Project-specific sections use the same heading and position but carry project-specific content. Optional sections are included only when needed.

For the actual deployable text of each section, see the [workflow section templates](templates/workflow-sections/).

### Section Descriptions

**Session Startup Procedure** — The seven-step startup sequence: read WORKFLOW, sync config backup, check the clock and time since last logged interaction, read REFERENCE and HANDOFF, read the most recent session log plus any additional logs the handoff identifies, read task queue if present, list Inbox. Identical across all projects.

**Base Path** — The project's filesystem root. One line.

**What This Project Does** — Brief project description and current sub-project list with one-line descriptions. Updated when sub-projects are added or archived.

**Sub-Project Activation** — Three-step activation pattern: read reference file, read everything the handoff identifies for that sub-project, load additional files as needed. Loading depth varies by sub-project and is governed by the handoff's pointers. When reading a sub-project's status file, verify it is consistent with the handoff and fix discrepancies on the spot (see Fix on Contact). Universal pattern with project-specific reference file pointers. Also establishes the write direction: domain knowledge produced during work goes into files inside the sub-project directory, not REFERENCE.txt. Every sub-project listed must have a reference file; if the directory exists, a seeded file exists.

**Task Queue** — For projects that use a task queue. Standard location: Workflow Files/TASKS.txt. Active items only (no DONE section), read at startup, add immediately when items arise, remove on completion and note in session log. Include only in projects that maintain a task queue file.

**Session Logs** — Logging mechanics. Per unit of work, not per chat. Sequential numbering. Write when substantive work accumulates; never defer to end of session. Keep logs concise; a growing log signals writing more often. Paired writes with HANDOFF (including freshness lines). Structure changes trigger REFERENCE.txt verification. Fix on contact for stale information. Evolving state: log topics at current progress, not binary. Handoff pointers scaled to complexity. Freshness line definitions and maintenance rules. Identical across all projects.

**Temporal Awareness** — Clock mechanism (write to file, get file info, read modified field, stale-reading retry) and time since last logged interaction. Identical across all projects.

**Inbox** — Asynchronous interface between the user and the project, both directions. The user drops files for processing; the AI writes drafts, deletion flags, delegation notes, or anything needing the user's attention. Processing guidance: list the directory before any reference to inbox contents (startup, mid-session, handoff writing), read on demand, check existing project structure before assessing items. Identical across all projects.

**Shared Knowledge Base** — Path and one-line description. Identical across all projects.

**Project Context** — Project-specific material earning its place in every context window but not covered by account-wide user preferences. Domain context, operational conventions. Accumulates through use. A file deletion convention is always present as a seed entry. Content already in account-wide preferences should not be duplicated here. Detailed procedures and file structure documentation belong in REFERENCE.txt, not here.

Additional sections may be prescribed by shared patterns (e.g., an Archive section prescribed by the archive pattern, sitting after Sub-Project Activation). These are governed by their pattern documentation, not the base registry.

A routing flowchart for new content:

- Needed every session, project-specific context → **Project Context** section
- Needed every session, mechanical/procedural → check the registry for an existing section
- Applies to all projects, behavioral/personal → account-wide user preferences
- Needed only when working a specific sub-project → sub-project reference file
- Reference material, procedures, file structure → REFERENCE.txt
- Domain knowledge for a specific sub-project → a file inside the sub-project directory (REFERENCE.txt points to it, does not hold it)
- New section type not in the registry → evaluate for registry expansion

---

## Project Instructions

These go into your AI application's project settings. The path is the only variable. Identical for every project.

The example below uses Claude Desktop's Filesystem extension. Adapt for other AI platforms with filesystem access.

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

A backup copy lives in the workspace at Config/PROJECT_INSTRUCTIONS.txt, synced automatically at startup (step 2). This makes the project fully portable: everything needed to recreate the project in a new account, on a different device, or for another person lives on the filesystem. It also serves as the source text when guiding project creation: the AI reads the file and presents its contents in conversation rather than directing the user to dig through Workflow Files.

The instructions describe capabilities using verbs (reading, writing, creating, editing, searching, moving) rather than naming specific tools. This means tool updates don't require instruction changes. "Filesystem tools" maps to the prefix the AI sees on every tool in its context. The first block asserts what the tools can do and commands an action: read WORKFLOW.txt. There is no evaluation step where the AI decides whether it has access. The fallback block handles sessions where the tools are absent (web, mobile) and instructs the AI to catch up on logging when the tools return. See INSTRUCTION COMPOSITION below.

---

## Key Principles

### Instruction Composition: Actions, Not Conditions

Every instruction must be composed as explicit action sequences, not conditional triggers. AI assistants follow actions reliably. They do not reliably evaluate conditions before acting.

"When X, do Y" assumes the AI will check X first. It often won't. "Do A to check X. If X, do Y" works because the check is itself an action. Sometimes the check needs a method: "Check if A is available by doing B."

This applies at every level: project instructions, startup procedures, sub-project reference files, inbox checks, temporal awareness steps. Every conditional phrase ("when," "if," "once," "after") is a candidate for conversion into an explicit action step.

Discovered through multiple iterations of the project instructions template. Each version was clear to a human reader. The problem was never clarity. It was the assumption that the AI processes instructions the way humans read them.

### Directory Design Is UX Design

The directory structure is a user interface. When someone opens the project folder, the visual hierarchy should communicate the project's organization without explanation. Sub-project folders tell you what the project does. Infrastructure is visually subordinate. Inbox is immediately accessible. WORKFLOW.txt is visible as the entry point.

Naming: natural case (Inbox, not INBOX). ALLCAPS reads as system files in a file browser. Folder names should feel natural alongside the user's other directories.

### Handoff-Driven Orientation

Orientation and archive are separate functions that need separate files. Session logs are the archive. HANDOFF.txt is the orientation. Loading the archive at startup conflates the two and wastes context on historical content that doesn't help the current chat continue the work.

Handoff notes flag known fragilities, not just steps. A task with hidden complexity needs a caution line naming the risk and pointing to documentation.

### Lean Workflow, Structural Reference

WORKFLOW.txt keeps only what earns its place in every context window: startup procedure, project description, temporal awareness, logging guidance, project context.

Everything else (file structure listings, detailed format specs, procedural notes, sub-project pointers) lives in Workflow Files/REFERENCE.txt. REFERENCE.txt is infrastructure: it describes the project's file structure, points to sub-project files, and holds procedural notes. It is not a container for domain knowledge. Domain content belongs in sub-project files; REFERENCE.txt points to those files. Both files read at startup, but they serve different roles: WORKFLOW carries procedure and behavioral rules, REFERENCE carries structural context.

### Concise Logging

Session logs capture every decision, state change, and rationale. They do not narrate the conversational process.

Logs are per unit of work, not per chat. A single chat may produce multiple log files; a brief chat may produce one small one. Numbering is sequential across the project.

Thoroughness applies to coverage (what is captured). Conciseness applies to expression (how it is written). These are not in tension.

Good: "Moved Q1 reports into Client A sub-project. Reduces root clutter, reports are client-specific. Summary spreadsheet absorbed (same data, different format)."

Unnecessary: "We discussed whether to keep the Q1 reports at root level. The user pointed out they're client-specific. We agreed moving them made more sense."

Reasoning IS worth capturing when a decision might be revisited: "Chose X over Y because Z." Process narration ("first we considered A, then B") is not, unless the alternatives themselves are important context.

Log without waiting to be asked. When substantive work has accumulated, write the session log and handoff. Logging is insurance against context loss, not a signal that work is finishing. After writing a log entry, continue working without shifting tone, offering to wrap up, or prompting for next steps.

For the mechanical rules that implement these principles in every WORKFLOW (paired writes, entry format, structure verification, fix on contact, evolving state), see the [session logs template](templates/workflow-sections/session-logs.md).

### Inbox: Verify and Check Before Referencing

List the inbox directory before any reference to its contents. This applies at startup, before mid-session processing, before mentioning inbox items to the user, and before writing inbox references into the handoff. Inbox contents change between messages. The user adds and clears items at any time. No earlier listing, and no handoff text, is a reliable substitute for the current directory state.

Before assessing an inbox item, check the project's existing work structure (sub-projects, case folders, task queues, archives) for related items. A fresh chat has no memory of past work. Directory listings are the recognition mechanism. Without this step, a chat may treat a familiar item as new, failing to connect it to work the project has already done.

### Fix on Contact

When you encounter stale or incorrect information in a workflow, handoff, reference, status, task queue, or index file during normal work, fix it then and there before continuing with other work. Do not defer in any form — noting it for later, flagging it as pending, or adding it to a task list all count as deferring. If a completed task is still on the task queue, remove it. If a status file contradicts the handoff, update it. If a reference file lists a structure that has changed, correct it. The cost of fixing on contact is a few seconds. The cost of deferring is a stale file that misleads the next session.

### Evolving State, Not Binary

Topics that develop across sessions must be logged at their current state of progress, not as binary open/closed. A design question progresses: not yet discussed → context gathered → options identified → partially decided → resolved. Binary logging ("open questions") forces the next chat to restart from scratch on topics where significant work was done.

Each in-progress item should capture: what information was gathered, what options were considered, where the person's thinking landed, and what specifically remains. This protects the human from repeating themselves. Their memory of conversational decisions fades between sessions just as the AI's context window ends.

See the companion pattern: [Evolving State in Handoffs](patterns/evolving-state.md).

### Act at the Moment of Decision

When a conversation produces a decision, execute it immediately rather than logging it for future action. A decision captured only as a to-do item requires the next handler — human or AI — to reconstruct the reasoning behind it. A decision executed immediately preserves the reasoning in the action itself.

### Session Logs Are Project-Wide

One sequence, tagged by functional area. This maintains the project narrative and avoids duplicating logging infrastructure. Location: Workflow Files/Session Logs/.

### Project Context Accumulates

WORKFLOW.txt includes a PROJECT CONTEXT section for project-specific material that earns its place in every context window but is not covered by account-wide user preferences. When the user corrects a project-specific behavior, the AI writes it here immediately. The project learns its operational context over time.

Account-wide preferences (formatting, communication style, interaction patterns) are already delivered via the AI application's user preference system and should not be duplicated in the WORKFLOW.

---

## Factual Grounding

AI assistants tend to fill information gaps with plausible-sounding content rather than acknowledging uncertainty. This is a known model behavior (see Anthropic's "Reduce Hallucinations" documentation for one treatment). Three techniques reduce it:

1. **Permission to not know.** When unsure of a fact, say so and offer to find out (search, read a file, ask the user). Uncertainty plus initiative, not a dead end.

2. **Ground in source material first.** When working from documents or files, read and extract relevant content before acting on them. Do not infer what a document says from context or training data.

3. **Verify and cite.** When making factual claims, search to verify and cite the source. When a claim cannot be supported, say so rather than presenting it as fact.

Techniques 1 and 2 apply broadly with minimal tradeoff. Technique 3 improves accuracy for work involving verifiable facts but constrains work that is creative, subjective, or advisory.

Techniques 1 and 2 are universal and belong in account-wide user preferences, not in project files. They apply to every interaction regardless of project or interface.

Technique 3 is project-specific. PROJECT CONTEXT entries scope it to the project's domain. Template:

```
FACTUAL GROUNDING: For verifiable claims in this
project's domain (such as [examples from your
domain]), verify via search rather than relying
on training data or assumptions.
```

Replace the bracketed part with a few examples of the kinds of verifiable claims that come up in the work. Keep it general — name the types of facts, not specific files or procedures. Examples of how different domains have scoped it:

- **Financial:** tickers, companies, funds, financial terms, market data
- **Technical:** tools, versions, configurations, compatibility
- **Legal/tax:** rules, thresholds, form requirements, filing deadlines

If a project already has PROJECT CONTEXT entries covering verification, data accuracy, or source-of-truth rules, consolidate them into the single FACTUAL GROUNDING entry. One consistent entry, not scattered entries layered on top of each other.

If a project's work is primarily creative or advisory, it may not need the verification piece at all.

When project files and training data conflict on a matter of fact, the project files are authoritative.

---

## Freshness Tracking

Every architecture-prescribed file carries two freshness lines immediately after its title line:

```
Last updated: [Month DD, YYYY] (Session NNN)
Last reviewed: [Month DD, YYYY]
```

These lines tell any reader when the file's content was last changed and when it was last confirmed current. File metadata can provide modification timestamps, but that costs a tool call per file and doesn't distinguish between content changes and formatting passes. The freshness lines are visible the moment the file is read.

### Definitions

**"Last updated"** means the file's content was intentionally changed: information added, removed, revised, or restructured. Routine freshness line maintenance (updating the date on these lines themselves) does not count as an update. When you change content, update this line. When you only review the file, leave this line unchanged.

**"Last reviewed"** means the file was read and its content confirmed to still be accurate, or corrected on the spot. Update this line whenever you read the file during substantive work, whether or not you changed anything else. A review that finds and fixes errors counts as both a review and an update: refresh both lines.

### Format

```
Last updated: Month DD, YYYY (Session NNN)
Last reviewed: Month DD, YYYY
```

Date comes first because temporal distance is the primary signal. Session number follows in parentheses for traceability within the project. "Last reviewed" omits the session number because there is no corresponding log entry to trace back to; the date is the only information that matters.

Both lines always present. If a file has never been reviewed separately from its last update, both lines carry the same date.

### Which Files

All architecture-prescribed files carry both freshness lines: WORKFLOW.txt, HANDOFF.txt, REFERENCE.txt, STATUS files, TASKS.txt, INDEX.txt files, sub-project reference files, and LESSONS_INDEX.txt. The title line carries only the file's identity. Freshness lines occupy lines 2-3.

Session logs do not carry freshness lines (they are append-only historical records with timestamps in their entries). Clock files and Config backups do not carry them.

Archived files retain whatever freshness lines they had at the time of archiving. Do not maintain freshness lines on files after they are archived. During the archiving process itself, refresh both freshness lines as part of the closing write (the closing note changes content and confirms final state).

Shared knowledge base documents that carry version numbers (Version X.X — Month YYYY) keep them instead of freshness lines. Version numbers serve a different purpose: they identify which version of a pattern has been adopted. All other shared files (README, INDEX files, templates, examples) use standard freshness lines.

### New Files

When creating a new file, set both freshness lines to the creation date and session. Do not use "Created:" or leave the lines blank. Every file starts with both lines populated from the moment it exists.

Domain files (working documents inside sub-projects that are not architecture-prescribed) also benefit from adopting the freshness standard. The more files that carry freshness lines, the easier it is to assess the currency of any file at a glance. When creating or editing domain files, add the standard freshness lines.

### Maintenance

Freshness lines are maintained as part of existing workflow triggers, not as a separate procedure:

- **Paired writes:** When writing a log entry and overwriting the handoff, refresh the handoff's freshness lines. When overwriting a STATUS file as part of the same paired write, refresh its freshness lines. For files that are overwritten wholesale (HANDOFF, STATUS files rewritten during state changes), both lines carry the same date because rewriting is both an update and a review.
- **Fix on Contact:** When correcting stale or incorrect information in any file, refresh both "Last updated" and "Last reviewed" (you changed the content and confirmed the rest).
- **Structure verification:** When verifying REFERENCE.txt after directory structure changes, refresh "Last updated" if content changed, and refresh "Last reviewed" regardless (you just confirmed it).
- **Task queue review:** When reading the task queue at startup and fixing completed items, refresh "Last reviewed" (you just confirmed the list is current). If you added or removed items, also refresh "Last updated."
- **Sub-project reference files:** When reading a sub-project reference file during substantive work, refresh "Last reviewed" before writing the session log. If you changed content, also refresh "Last updated."

### WORKFLOW Integration

The WORKFLOW SESSION LOGS section carries a compressed version of the definitions and maintenance rules so that every session has them in context. The full specification lives in this document; the WORKFLOW carries the operational instructions (~150-200 tokens):

```
FRESHNESS LINES: Every project file (except session logs
and Clock) carries two lines after its title:

  Last updated: [Month DD, YYYY] (Session NNN)
  Last reviewed: [Month DD, YYYY]

"Last updated" means content was intentionally changed —
adding, removing, revising, or restructuring. Updating
only the freshness lines themselves does not count.
"Last reviewed" means content was read and confirmed
accurate during substantive work, whether or not anything
changed. A correction refreshes both.

For files overwritten wholesale (HANDOFF, STATUS) or
newly created, both lines carry the same date and session.
```

---

## The Indexed Collection Pattern

A general strategy for any content that accumulates and is consulted selectively: an index file that describes what's available, plus a collection of small files each covering one item or topic.

Monolithic files are a context cost time bomb. A single lessons file or reference document is fine when it has five entries. At fifty entries it costs thousands of tokens every time it's read, and every read stays in context for the entire conversation. Files that grow by accretion will eventually consume a meaningful share of the context window just to look up one item.

The indexed pattern avoids this. Like a card catalog in a library, read the index to know what's available, then pull only the file you need. Cost is ~1 KB for the index read plus the one file you actually need, regardless of how large the collection grows. Adding a new entry costs ~1.5 KB of context (read index, read one topic file, write the update). Compare to reading and rewriting a monolithic file that grows without bound.

This pattern applies anywhere items accumulate and get looked up selectively: operational lessons, case evidence, research sources, reference materials, design decisions.

Standing rule: any folder where a reader needs to discover and selectively access its contents gets an INDEX.txt at creation time, not retroactively. This includes domain folders, reference collections, case evidence, research materials — anywhere a reader would otherwise need to open every file to know what's there. It does not include infrastructure folders with architecturally defined contents (Workflow Files/, Session Logs/, Config/) where the files have known roles.

The reader is not just the current chat. Indexes serve future chats (token-efficient retrieval), the user browsing the folder (directory design as UX extends into folder contents), other projects reading cross-project files, and any new AI account or system absorbing the project from the filesystem (portability). The project filesystem is designed to be portable — a new account with the project instructions and the filesystem can pick up the work. An index in every document folder is what makes that practical without brute-force reading.

Indexes serve retrieval, not just growth. A static folder with five files benefits from an index just as much as a growing one. Creating an index empty or with a placeholder costs nothing and ensures the pattern is never missed. The failure mode is a chat judging that a folder doesn't need an index because it won't grow.

The structure:

```
[Collection Folder]/
  INDEX.txt (or LESSONS_INDEX.txt, etc.)
  [item_1].txt
  [item_2].txt
  ...
```

Naming follows the domain. A case folder has Resources/ with INDEX.txt. Project-level operational knowledge has Lessons/ with LESSONS_INDEX.txt. A research project might have Sources/ with INDEX.txt. The pattern is the same; the naming adapts.

---

## Knowledge Architecture

Knowledge flows upward through three levels:

**Sub-project reference files:** Domain-specific knowledge managed by each sub-project in whatever form serves the work. A client management sub-project has case files and communication logs. A research sub-project has analytical frameworks and source annotations. A media sub-project has taste profiles and tracking lists. These are living documents that capture the current state of the sub-project's thinking.

Domain knowledge always lives in sub-project files, not in the project-level REFERENCE.txt. When a sub-project accumulates context, write that content into a file inside the sub-project directory. The project-level REFERENCE.txt carries a pointer to the sub-project file and a one-line scope description — never a summary or duplication of the content itself.

**Project operational lessons:** Cross-cutting knowledge that any sub-project might need. Tool quirks, workarounds, migration procedures, context cost behavior. Centralized in Workflow Files/Lessons/ with an index routing to topical files. When a sub-project discovers something operationally useful, it surfaces here.

**Shared knowledge base (optional):** Cross-project knowledge published as standalone entries. One project discovers a technique, documents it portably, publishes it. Other projects encounter it and adopt, adapt, or ignore it. This is how projects teach each other. Only relevant if you're running multiple projects.

The direction is always upward: sub-project reference files → project Lessons/ → shared knowledge base. Each level is a different formalization with a broader audience.

### Cross-Project Routing via Coordinator Inbox

When a project chat discovers something cross-cutting during its own domain work, it doesn't need to know the shared knowledge base structure or make the routing decision itself. The pattern: the project chat packages the observation as a concise note (what was noticed, why it matters, where it might belong), and routes it to the coordinator project's inbox. The coordinator reads the note, decides where it belongs, places it, and clears the inbox.

Not every cross-cutting observation warrants a new shared document. Many are feedback on existing infrastructure: a note that improves an existing doc, a line item for a project's lessons file, or a correction to a shared template. The routing mechanism is the same regardless of destination. The coordinator has the cross-project view to decide.

The note should include: the observation itself, the source (which project and session), and a suggestion for where it might land. The suggestion is advisory. The coordinator may route it differently based on its view across all projects.

### The Coordinator Project

When you run multiple projects, you can create one project as a meta-project coordinator to develop and maintain the system they all share. It uses the same workspace architecture as every other project. Its domain work is the architecture itself.

The coordinator is where you do design work on the workspace system, maintain the shared knowledge base, propagate structural changes, audit projects for consistency, and manage cross-project delegations. It also serves as a gateway for cross-project visibility: summarizing task queues across all projects, helping prioritize between competing demands in different projects, and giving you a single place to ask "what's pending across everything?" Since all project directories live under the same root (a requirement of the Filesystem extension's permissions model), every project can read every other project's files. The coordinator uses this to read handoffs, task queues, and inboxes across all projects, write delegation notes, and verify that changes have been applied.

A coordinator project is not required. A single project or a few projects work fine without one. The coordinator becomes valuable when you have enough projects that cross-cutting concerns emerge: shared patterns that need to stay consistent, design changes that affect multiple projects, observations from one project that would benefit others.

Building a coordinator:

- Create it like any other project with the same workspace architecture.
- Its sub-project covers system-level work: architecture design, shared knowledge base maintenance, cross-project tracking, and any active design efforts.
- Its WORKFLOW describes the coordinator role and lists all the projects it manages.
- It maintains the shared knowledge base (a directory of standalone documents covering patterns and techniques that any project can consult).
- It uses the inbox mechanism in both directions: domain projects route cross-cutting observations to the coordinator's inbox, and the coordinator writes delegation notes to domain project inboxes.

The coordinator's relationship to domain projects is consultative, not controlling. Domain projects are self-sufficient. They read the shared knowledge base, apply the architecture's principles, and use their own judgment. The coordinator improves the design and makes it available. It does not babysit individual projects.

---

## Sub-Projects

Each functional area gets its own directory at the project root. This directory is the authoritative home for all domain knowledge in that area. Everything the AI learns about the domain — case data, research threads, tracking lists, analytical frameworks, procedural notes — is written into files inside the sub-project directory. The project-level REFERENCE.txt points to these files but never holds domain content itself.

Always create at least one sub-project folder, even for single-focus projects, to establish the pattern and avoid restructuring later.

### Sub-Project Internal Structure

A sub-project's internal structure mirrors the project level: an orientation file for current state, a reference file for accumulated domain knowledge, and domain folders shaped by the work. The same architectural logic that separates WORKFLOW.txt from REFERENCE.txt at the project level applies inside each sub-project.

Standard file roles:

- **[SubProject]_STATUS.txt** — Orientation. Current state, what's active, what's pending, known issues. Read at activation. Overwritten as state changes. This is the sub-project analog of HANDOFF.txt at the project level. Required for any sub-project with ongoing work spanning multiple sessions.
- **[SubProject]_REFERENCE.txt** — Domain knowledge. Accumulated understanding, specifications, procedures, configurations consulted during work. Read on demand. Grows over time. When it grows large, apply the indexed collection pattern.
- **[named domain files]** — Working documents shaped by the domain. Case folders, design briefs, tracking lists, configuration files, research notes. Named for what they contain (e.g., voice_config.txt, not config.txt).
- **[domain folders]** — Cases/, Testing Reports/, Research/, etc. Shaped by the work.

**Naming rules:** Files inside sub-project directories must include the sub-project name or a domain-specific identifier. No generic names like REFERENCE.txt or STATUS.txt — these collide with the project-level files and with each other when read into context. A chat reading VOICEMODE_STATUS.txt or SUPPLEMENTS_REFERENCE.txt knows immediately what sub-project it belongs to. Exception: a sub-project with a single primary file may use a content-descriptive name instead (e.g., trust_analysis.txt). The test is whether the filename alone identifies the sub-project.

**Development trajectory:** A new sub-project starts with a status file and possibly a reference file. As work accumulates, named domain files and folders emerge. As domain files grow, the indexed collection pattern applies. The AI should recognize when infrastructure needs to develop and build it, following the patterns in this document and looking at how peer sub-projects have organized their work.

Standing rule: when a sub-project directory is created, seed it with at least a status file immediately. An empty sub-project directory has no gravity — domain knowledge will flow to the project-level REFERENCE.txt instead, because that file already exists and has structure. A seeded file reverses that pull.

Sub-project structure depends on the shape of the work:

- Cases that open and close (client work, support tickets, disputes)
- Parallel ongoing projects (codebases, skill development)
- Sequential progression (chapters, assignments, phases)
- Themes or topics (research areas, product lines)
- Individuals (clients, correspondents, students)

Each shape implies different internal folders and reference file content.

### Migration

When a sub-project outgrows its parent project, it can be split into its own project. Build the new project's structure from inside the old project, move the directory, create the new AI project with the instructions template, move relevant chats, migrate session logs with provenance headers, update the old project. Migration is also an opportunity to add structure the work has grown into.

### Archiving

When a sub-project completes, it moves to Archive/ at the project root with a completion-date name (e.g., "Project Name - 2026-03"). The sub-project's status file gets a closing note before archiving. An ARCHIVE_INDEX.txt at the project root maintains an inventory of archived sub-projects for discoverability. Active sub-projects always live at root, never inside Archive/.

See the companion pattern: [Sub-Project Archive Pattern](patterns/archive-pattern.md).

### Sub-Project Complexity Tiers

Sub-projects operate at one of two context tiers:

**Standard:** The default. The sub-project's state is summarized in the project-level HANDOFF.txt. Its reference files load on demand when work begins. No additional orientation file needed.

**Extended:** For sub-projects whose domain complexity requires richer orientation than a handoff summary can provide. The sub-project maintains its own orientation file (named distinctively, never HANDOFF.txt) with detailed state, open questions at their current stage of thinking, and reading pointers to its own reference materials.

A sub-project starts at Standard by default. It can be designated Extended at creation if the scope is known, or promoted later when complexity emerges.

Extended tier means permission for: longer orientation files, bigger session log entries for that area, more reference material. It does not mean abandoning the optimization principles. Concise logging, indexed collections, and on-demand loading all still apply. The ceiling is raised, not removed.

### Loading Sequence for Extended Sub-Projects

Startup and activation are separate loading steps.

**Startup** (at session open): Follow the standard startup sequence (see Startup). The project-level HANDOFF.txt carries a brief summary of each sub-project's state and a pointer to its orientation file.

**Activation** (when user directs work to the sub-project): Read the sub-project's orientation file. Read the session log referenced in its "last active" pointer, if different from the session log already loaded at startup. Report sub-project state to the user and wait for direction.

The WORKFLOW.txt must include an explicit activation sequence for each Extended sub-project, specifying the files to read and their order. Example:

```
When the user indicates work on [Sub-Project]:
1. Read [Sub-Project]/[STATUS_FILE].txt
2. Read the session log named in its "last active" pointer
   (unless already loaded at startup)
3. Report sub-project state and wait for direction
```

This keeps startup lean while giving Extended sub-projects the full context load they need when activated. The orientation file must have a distinctive name that cannot be confused with the project-level HANDOFF.txt. Use a name that reflects the sub-project's domain. The name should make the file's scope obvious from a directory listing.

---

## Task Queues

Active items only. When a task is completed, remove it from the queue and note completion in the session log. The session log is the archive. No DONE section, no archive file. A DONE section or archive creates a growing document that must be read and rewritten every time a task is completed. The context cost of maintaining an archive exceeds its value, since the session logs already contain the completion record.

The project-level task queue reads at startup. Task queues are short (active items only, no DONE section) and the cost of reading them is low. The alternative — on-demand loading — demonstrably leads to stale queues because the demand never comes when the handoff carries enough context to proceed. Sub-project or function-specific queues read at sub-project activation rather than startup.

Task queues take different shapes depending on the work. A priority queue lists what to work on next, organized by urgency or category (active, follow-up, backlog). A living checklist tracks items being worked through during a session, with items checked off as they're completed. Both are valid. Some projects use one, some the other, some both for different purposes.

Complex projects may need multiple task queues split by function or sub-project. Each queue stays focused on its domain and stays small. The alternative (one large combined queue) creates a file that grows beyond what any single session needs, costing context to read items irrelevant to the current work.

---

## Temporal Awareness

AI assistants have no internal clock. Temporal awareness has two components, both baseline startup behaviors:

1. **What time is it now?**
2. **How long has it been since the last logged interaction?**

The first gives the current moment. The second gives context: is this a return after three days or a continuation from an hour ago? Both inform orientation. Temporal awareness is not just knowing the time but reasoning about what it means for the work: day of week, business hours, calendar deadlines, how much may have changed.

The mechanism uses a persistent Clock file (Workflow Files/Clock/timestamp.txt) and filesystem metadata. Each project's WORKFLOW.txt carries the implementation steps.

See the companion pattern: [Temporal Awareness](patterns/temporal-awareness.md).

---

## Adopting This Structure

### For New Projects

Start with this structure even for single-function projects. Create one sub-project folder to establish the pattern. This avoids restructuring when the project expands.

The [templates](templates/) directory contains deployable text for every WORKFLOW section and structural templates for every mandated file. Use them as your starting point.

### For Existing Projects

The existing structure works well for its scope. Migrate when the project grows or when starting fresh is worthwhile:

1. Create a sub-project folder for the current work and move domain-specific files into it
2. Create Workflow Files/ and move Clock/, Config/, Session Logs/ into it
3. Create Workflow Files/HANDOFF.txt and REFERENCE.txt
4. Ensure Inbox/ stays at root
5. Rewrite WORKFLOW.txt: lean version with handoff-driven startup procedure
6. Add freshness lines (Last updated, Last reviewed) to all files created in steps 1-5. See Freshness Tracking.
7. Simplify project instructions to match the template in Project Instructions above
8. Update Config backup to match

---

## Known Limitations

**Filesystem required for full functionality.** Currently requires an AI application with filesystem read/write access. In the Claude ecosystem, this means the Desktop app with the Filesystem extension (macOS and Windows). Web and mobile interfaces don't have filesystem access. The workspace degrades gracefully: chats note what needs syncing when desktop access is restored.

**Chat search is typically project-scoped.** Built-in chat search usually only sees conversations within the current project. It will never find anything from another project. But the filesystem spans everything. When you need cross-project context, the AI reads the other project's files directly.

**Domain file design is domain-specific.** This architecture prescribes standard file roles inside sub-projects (STATUS for orientation, REFERENCE for domain knowledge) and naming conventions, but the specific content and additional domain files depend on the nature of the work.

**Project memory.** This system works with your AI application's project memory turned on or off. With memory on, you may find duplication between memory and filesystem state. With memory off, you may find less long-term usefulness on mobile or web where the filesystem is unavailable. Experiment with both to see what works for your use case.
