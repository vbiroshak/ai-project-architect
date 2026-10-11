# Workspace Architecture for Sustained Knowledge Work with AI

Version 4.11

A workspace architecture designed for continuity across sessions.

Developed through iterative design and daily use across projects in different domains. For any project where an AI assistant serves one or more areas of ongoing work.

---

## The Problem

Default AI project tools are not built for sustained knowledge work: project files are static uploads, each conversation starts blank, and the AI has no way to maintain its own documentation, log sessions, or orient itself in ongoing work.

The workspace pattern moves project knowledge into files on your computer that the AI reads, writes, and maintains directly.

This document describes the architecture: the principles, patterns, and file roles that make the system work. It is platform-agnostic. For setup instructions:

- **Setup:** [Setting Up in Claude Code](claude-code-setup.md)
- **Migration:** [Migrating from Chat to Code](chat-to-code-migration.md)
- **Adaptation:** [Running on Another Platform](platform-adaptation.md)

---

## The Inbox

Inbox/ at the project root is the asynchronous interface between the user and the project, in both directions.

The user drops files here between sessions: emails saved as text, documents to process, screenshots, reference material, delegation briefs, anything the project needs to see. The AI checks the inbox at every startup, lists the files, and offers to process them.

The AI writes to the Inbox when it has something for the user: drafts for review, items flagged for deletion, cross-project delegation notes, or anything that needs the user's attention outside the current conversation.

The user saves something relevant to the project's inbox and moves on; the AI places a draft or a flagged file there for the user to find. The inbox holds work from when it arrives until the project is active, in either direction.

At startup the inbox is listed (filenames only), not read; the session processes items when directed or when the work calls for them.

Inbox contents can change at any time between messages.

An inbox item may be work not yet in the project's task list or session log, so a coordinator project's task review (see Knowledge Architecture below) includes inbox listings.

---

## Key Principles

### Portable by Design

The project is plain text files in a folder. Everything it knows and does, its instructions, state, history and procedures, is readable by any AI that can work in a folder on the user's computer, and by the user with a text editor. Nothing the project depends on lives inside one application.

AI applications offer features of their own: memory, plugins, code that runs inside the application, interface elements. Use them where they make the work easier, under one test: the project works the same with the feature turned off. A feature passes when it adds convenience on top of the files. It fails when it becomes the only place a procedure, a record, or a piece of the user's data exists. When a feature fails the test, put the mechanism in the files and let the feature, at most, present it.

The aim is that your work stays yours to do what you want with: move it, copy it, read it without the application, or hand it to a different AI. The project survives a change of application, account, model or vendor, or the loss of a service, because the next AI reads the folder and continues.

The session record is part of this. Every session's transcript belongs to the project's record, and the application keeps it in its own store, outside the folder, in its own format. The project copies each session's transcript into Project/Sessions/ at the start of the next session, named with the session number, with a readable rendering beside it. The next start is the reliable moment: sessions end without warning, and a copy taken at the end may never be taken. A project without this has its history inside one application.

### Instruction Composition: Actions, Not Conditions

Every instruction must be composed as explicit action sequences, not conditional triggers. AI assistants follow actions reliably. They do not reliably evaluate conditions before acting.

"When X, do Y" assumes the AI will check X first. It often won't. "Do A to check X. If X, do Y" works because the check is itself an action. Sometimes the check needs a method: "Check if A is available by doing B."

This applies at every level: project instructions, startup procedures, sub-project reference files, inbox checks, temporal awareness steps. Every conditional phrase ("when," "if," "once," "after") is a candidate for conversion into an explicit action step.

Conditional instructions read as clear to a human, which hides the failure. The bar is not clarity to a human reader but whether the instruction is an action the AI will execute rather than a condition it must evaluate first.

### Directory Design Is UX Design

The directory structure is a user interface: the hierarchy should show the project's organization without explanation. Sub-project folders say what the project does. Infrastructure is visually subordinate. Inbox is immediately accessible.

Naming: natural case (Inbox, not INBOX). ALLCAPS reads as system files in a file browser. Folder names should feel natural alongside the user's other directories.

### Handoff-Driven Orientation

Orientation and archive are separate functions and need separate files: session logs are the archive, HANDOFF.txt is the orientation. Loading the archive at startup wastes context on history that does not help the current session continue.

Handoff notes flag known fragilities, not just steps. A task with hidden complexity needs a caution line naming the risk and pointing to documentation.

### Lean Governing Document, Structural Index

The governing document keeps only what earns its place in every context window: project description, logging guidance, and project context. The startup procedure lives in a separate file, the one the platform loads at session start (CLAUDE.md in Claude Code), which imports or names the governing document (PROJECT_CONTEXT.md).

The project's file structure lives in PROJECT_INDEX.txt: a structural index of what exists and where. It holds no domain knowledge, procedures, or format specifications; those belong in the governing document (if they earn their place in every context window) or in sub-project reference files (if they are domain-specific). Both files read at startup with different roles: the governing document carries procedure and behavioral rules, PROJECT_INDEX the structural map.

### Concise Logging

Session logs capture every decision, state change, and rationale. They do not narrate the conversational process.

One log per session, numbered to match the session number, sequential across the project. The number comes from the user, in the opening message of each session, in whatever form they use; the suggested form is "This is [Project] N", because it works on every platform and the archiver reads it, and a platform's own way of naming a session may serve as well. The session log and the archived transcript carry the same number. A project's sessions are the ones run in its own folder. Work done on the project from a session outside its folder, such as a coordinator project building, migrating or converting it, takes no number here and is recorded in the project that session belongs to, if any; the project's own sequence continues with its next session.

Thoroughness applies to coverage (what is captured). Conciseness applies to expression (how it is written). These are not in tension.

Good: "Moved Q1 reports into Client A sub-project. Reduces root clutter, reports are client-specific. Summary spreadsheet absorbed (same data, different format)."

Unnecessary: "We discussed whether to keep the Q1 reports at root level. The user pointed out they're client-specific. We agreed moving them made more sense."

Reasoning IS worth capturing when a decision might be revisited: "Chose X over Y because Z." Process narration ("first we considered A, then B") is not, unless the alternatives themselves are important context.

Log without waiting to be asked. When substantive work has accumulated, write the session log and handoff. Logging is insurance against context loss, not a signal that work is finishing. After writing a log entry, continue working without shifting tone, offering to wrap up, or prompting for next steps.

### Inbox: Verify and Check Before Referencing

List the inbox directory before any reference to its contents: at startup, before mid-session processing, before mentioning inbox items to the user, and before writing inbox references into the handoff. The user adds and clears items at any time, so no earlier listing and no handoff text stands in for the current directory state.

Before assessing an inbox item, check the project's existing work structure (sub-projects, case folders, task queues, archives) for related items. A fresh session has no memory of past work; directory listings are how it recognizes a familiar item, and without this step it may treat one as new.

### Fix on Contact

When you encounter stale or incorrect information in a project file during normal work, fix it then and there before continuing with other work. Do not defer in any form — noting it for later, flagging it as pending, or adding it to a task list all count as deferring. If a completed task is still on the task queue, remove it. If a status file contradicts the handoff, update it. If a reference file lists a structure that has changed, correct it. Fixing on contact costs a few seconds; deferring costs a stale file that misleads the next session.

### Evolving State, Not Binary

Topics that develop across sessions must be logged at their current state of progress, not as binary open/closed. A design question progresses: not yet discussed → context gathered → options identified → partially decided → resolved. Binary logging ("open questions") forces the next session to restart from scratch on topics where significant work was done.

Each in-progress item should capture: what information was gathered, what options were considered, where the person's thinking landed, and what specifically remains. This protects the human from repeating themselves: their memory of conversational decisions fades between sessions just as the AI's context window ends.

See the companion pattern: [Evolving State in Handoffs](patterns/evolving-state.md).

### Act at the Moment of Decision

When a conversation produces a decision, execute it immediately rather than logging it for future action. A decision captured only as a to-do item requires the next handler — human or AI — to reconstruct the reasoning behind it. A decision executed immediately preserves the reasoning in the action itself.

### Session Logs Are Project-Wide

One sequence, tagged by functional area. This maintains the project narrative and avoids duplicating logging infrastructure.

### Project Context Accumulates

The governing document includes a section for project-specific material that earns its place in every context window but is not covered by account-wide user preferences. When the user corrects a project-specific behavior, the AI writes it here immediately. The project learns its operational context over time.

Account-wide preferences (formatting, communication style, interaction patterns) come from the application's user preference system and are not duplicated in the governing document.

---

## Factual Grounding

AI assistants tend to fill gaps with plausible content rather than admit uncertainty. Three techniques may reduce it:

1. **Permission to not know.** When unsure of a fact, say so and offer to find out (search, read a file, ask the user). Uncertainty plus initiative, not a dead end.

2. **Ground in source material first.** When working from documents or files, read and extract relevant content before acting on them. Do not infer what a document says from context or training data.

3. **Verify and cite.** When making factual claims, search to verify and cite the source. When a claim cannot be supported, say so rather than presenting it as fact.

Techniques 1 and 2 are general behavioral guidance, not installed by this architecture; place them wherever your setup puts behavioral rules: account-wide user preferences, an output style, or project-level instructions.

Technique 3 is installed per-project via the project context template. It scopes verification to the project's domain:

```
FACTUAL GROUNDING: For verifiable claims in this
project's domain (such as [examples from your
domain]), verify via search rather than relying
on training data or assumptions.
```

Replace the bracketed part with a few examples of the verifiable claims that come up in the work: types of facts, not specific files or procedures. Examples by domain:

- **Travel:** visa rules, fares, opening hours, transit schedules
- **Technical:** tools, versions, configurations, compatibility
- **Gardening:** plant names, hardiness zones, planting dates, pest treatments

If a project already has project context entries covering verification, data accuracy, or source-of-truth rules, consolidate them into the single FACTUAL GROUNDING entry.

If a project's work is primarily creative or advisory, it may not need the verification piece at all.

When project files and training data conflict on a matter of fact, the project files are authoritative.

---

## Freshness Tracking

Every architecture-prescribed file carries two freshness lines immediately after its title line:

```
Last updated: [Month DD, YYYY] (Session NNN)
Last reviewed: [Month DD, YYYY]
```

These lines say when the content was last changed and when it was last confirmed current, visible the moment the file is read. File metadata gives modification times, but at a tool call per file, and it does not distinguish content changes from formatting passes.

### Definitions

**"Last updated"** means the content was intentionally changed: information added, removed, revised, or restructured. Updating the freshness lines themselves does not count. Change content, update this line; only review the file, leave it.

**"Last reviewed"** means the file was read and its content confirmed accurate, or corrected on the spot. Update it whenever you read the file during substantive work, whether or not anything else changed. A review that finds and fixes errors is also an update: refresh both lines.

### Format

```
Last updated: Month DD, YYYY (Session NNN)
Last reviewed: Month DD, YYYY
```

The date comes first because temporal distance is the primary signal; the session number follows in parentheses for traceability. "Last reviewed" omits the session number: there is no log entry to trace to, and the date is what matters.

Both lines always present. If a file has never been reviewed separately from its last update, both lines carry the same date.

### Which Files

All architecture-prescribed files carry both freshness lines: PROJECT_CONTEXT.md, HANDOFF.txt, PROJECT_INDEX.txt, STATUS files, TASKS.txt, CHANGELOG.txt, INDEX.txt files, sub-project reference files, and LESSONS_INDEX.txt. The title line carries only the file's identity. Freshness lines occupy lines 2-3.

Session logs do not carry freshness lines (they are append-only historical records with timestamps in their entries).

Archived files keep the freshness lines they had when archived; do not maintain them afterwards. The closing write before archiving refreshes both lines (the closing note changes content and confirms the final state).

### New Files

A new file gets both freshness lines set to the creation date and session, never "Created:" or blank lines.

Domain files (working documents inside sub-projects, not prescribed by the architecture) also benefit: the more files carry freshness lines, the easier it is to judge any file's currency at a glance. Add the lines when creating or editing domain files.

### Maintenance

Freshness lines are maintained as part of existing workflow triggers, not as a separate procedure:

- **Paired writes:** When writing a log entry and overwriting the handoff, refresh the handoff's freshness lines, and a STATUS file's if the same write overwrites it. A file overwritten wholesale (HANDOFF, a STATUS file rewritten at a state change) carries the same date on both lines, because rewriting is both an update and a review.
- **Fix on Contact:** When correcting stale or incorrect information in any file, refresh both "Last updated" and "Last reviewed" (you changed the content and confirmed the rest).
- **Structure verification:** When verifying PROJECT_INDEX.txt after directory structure changes, refresh "Last updated" if content changed, and refresh "Last reviewed" regardless (you just confirmed it).
- **Task queue review:** When reading the task queue at startup and fixing completed items, refresh "Last reviewed" (you just confirmed the list is current). If you added or removed items, also refresh "Last updated."
- **Sub-project reference files:** When reading a sub-project reference file during substantive work, refresh "Last reviewed" before writing the session log. If you changed content, also refresh "Last updated."

### Governing Document Integration

The governing document's SESSION LOGS section carries a compressed version of these definitions and rules, so every session has them in context. This document is the full specification; the governing document carries the operating instructions:

```
FRESHNESS LINES: Every project file (except session logs)
carries two lines after its title:

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

A single growing file means the AI reads everything to find one item. A lessons file is fine at five entries; at fifty it costs thousands of tokens every time it is read, a meaningful share of the context window for one lookup.

The indexed pattern avoids this: read the index to know what is available, then pull only the file you need. The cost is about 1 KB for the index plus the one file, however large the collection grows; adding an entry costs about 1.5 KB (read the index, read one topic file, write the update), against reading and rewriting a monolithic file that grows without bound.

This pattern applies anywhere items accumulate and get looked up selectively: operational lessons, case evidence, research sources, reference materials, design decisions.

Standing rule: any folder whose contents a reader needs to discover and access selectively gets an INDEX.txt at creation, not later: domain folders, reference collections, case evidence, research materials, anywhere a reader would otherwise open every file to know what is there. Infrastructure folders whose files have defined roles do not need one.

Indexes serve more than the current session: future sessions (token-efficient retrieval), the user browsing the folder, other projects reading its files, and any new AI or account taking the project over from the folder. An index in every document folder is what makes that takeover practical without reading every file.

Indexes serve retrieval, not only growth: a static folder of five files benefits as much as a growing one. An index created empty or with a placeholder costs nothing; the failure is a session deciding a folder needs none because it will not grow.

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

**Sub-project reference files:** Domain-specific knowledge managed by each sub-project in whatever form serves the work: case files and communication logs for client management, analytical frameworks and source annotations for research, style guides and drafts for writing. Reference files are kept current.

Domain knowledge lives in sub-project files, never in PROJECT_INDEX.txt, which carries only a pointer to each file and a one-line scope description. When a sub-project accumulates context, write it into a file inside the sub-project directory.

**Project operational lessons:** Cross-cutting knowledge that any sub-project might need: what worked, what did not, patterns across cases, tool workarounds, procedures that apply across areas. Centralized in a Lessons/ directory with an index routing to topical files; a sub-project that discovers something operationally useful surfaces it here.

**Shared knowledge base (optional):** A folder outside the project directories that all projects have access to, holding cross-project knowledge as standalone entries: one project documents a technique and publishes it; others adopt, adapt, or ignore it. Only relevant with several projects.

The direction is always upward: sub-project reference files → project Lessons/ → shared knowledge base. Each level is a different formalization with a broader audience.

An application's session search usually sees only the current project's conversations; the filesystem spans everything, so for cross-project context the AI reads the other project's files directly.

### The Coordinator Project

With several projects, one project can be the coordinator that develops and maintains the system they share. It uses the same architecture as every other project; its domain work is the architecture itself.

The coordinator designs the workspace system, maintains the shared knowledge base, propagates structural changes, audits projects for consistency, tests improvements, and manages cross-project delegations. It is also the one place to ask what is pending across everything, to summarize task queues and prioritize between projects: every project can read every other project's files, and the coordinator reads handoffs, task queues, and inboxes across all of them, writes delegation notes, and verifies that changes have landed.

A coordinator is not required; one project or a few work without one. It earns its place when cross-cutting concerns appear: shared patterns to keep consistent, design changes that affect several projects, observations from one project that would help others.

Building a coordinator:

- Create it like any other project with the same workspace architecture.
- Its sub-project covers system-level work: architecture design, shared knowledge base maintenance, cross-project tracking, and any active design efforts.
- Its governing document describes the coordinator role and lists all the projects it manages.
- It maintains the shared knowledge base (a directory of standalone documents covering patterns and techniques that any project can consult).
- It uses the inbox mechanism in both directions: domain projects route cross-cutting observations to the coordinator's inbox, and the coordinator writes delegation notes to domain project inboxes.

The coordinator advises; it does not control. Domain projects are self-sufficient: they read the shared knowledge base, apply the architecture's principles, and use their own judgment. The coordinator lets you work on them without distracting them from their domain work.

---

## Sub-Projects

Each functional area gets its own directory at the project root, the home of all domain knowledge in that area: case data, research threads, tracking lists, analytical frameworks, procedural notes, everything the AI learns about the domain. PROJECT_INDEX.txt points to these files and never holds domain content.

Always create at least one sub-project folder, even for single-focus projects, to establish the pattern and avoid restructuring later.

### Sub-Project Internal Structure

A sub-project's internal structure mirrors the project level: an orientation file for current state, a reference file for accumulated domain knowledge, and domain folders shaped by the work.

Standard file roles:

- **[SubProject]_STATUS.txt** — Orientation. Current state, what's active, what's pending, known issues, and pointers to the sub-project's other files. Read at activation, overwritten as state changes: the sub-project's HANDOFF.txt. Required for any sub-project whose work spans sessions.
- **[SubProject]_REFERENCE.txt** — Domain knowledge: accumulated understanding, specifications, procedures, configurations consulted during work. Read on demand; when it grows large, apply the indexed collection pattern.
- **[named domain files]** — Working documents shaped by the domain. Case folders, design briefs, tracking lists, configuration files, research notes. Named for what they contain (e.g., voice_config.txt, not config.txt).
- **[domain folders]** — Cases/, Drafts/, Research/, etc. Shaped by the work.

**Naming rules:** Files inside sub-project directories carry the sub-project name or a domain identifier: RESEARCH_STATUS.txt, not STATUS.txt, which collides with every other status file once read into context. Exception: a sub-project with a single primary file may use a content-descriptive name (trust_analysis.txt). The test is whether the filename alone identifies the sub-project.

**Development trajectory:** A new sub-project starts with a status file and perhaps a reference file; named domain files and folders follow as work accumulates, and the indexed collection pattern as they grow. The AI builds this infrastructure as the need appears, following this document and the peer sub-projects.

Standing rule: seed every new sub-project directory with at least a status file at once. An empty directory gets skipped, and the AI writes domain content into PROJECT_INDEX.txt instead, because that file exists and has structure; a seeded status file gives the content a home from the start.

Sub-project structure depends on the shape of the work:

- Cases that open and close (client work, support tickets, disputes)
- Parallel ongoing projects (codebases, skill development)
- Sequential progression (chapters, assignments, phases)
- Themes or topics (research areas, product lines)
- Individuals (clients, correspondents, students)

Each shape implies different internal folders and reference file content.

### Archiving

A completed sub-project moves to Archive/ at the project root under a completion-date name ("Project Name - 2026-03"), with a closing note in its status file first. ARCHIVE_INDEX.txt inside Archive/ is the inventory. Active sub-projects live at root, never inside Archive/.

See the companion pattern: [Sub-Project Archive Pattern](patterns/archive-pattern.md).

---

## Project Complexity Tiers

The default setup is a baseline: state in HANDOFF.txt, reference files on demand, a lean startup procedure, and activation for every sub-project (its status file read before the first action on a request that belongs to it, then the files the status file points to, then what the handoff identifies). As a project or sub-project grows, give it more context.

At the project level: more files in the startup procedure, more session logs read by default, a governing document with more operating detail. At the sub-project level: a status file that grows into a full orientation file, with detailed state, open questions at their current stage, and pointers to its reference materials, and an activation sequence in the governing document naming the files to read, in order. Startup stays lean; a complex sub-project gets its full context when activated.

This is a matter of degree: more reads, longer documents, richer orientation. Concise logging, indexed collections, and on-demand loading still apply.

---

## Task Queues

Active items only. When a task is completed, remove it and note the completion in the session log, which is the archive. No DONE section and no archive file: either is a growing document read and rewritten at every completion, at a context cost that exceeds its value when the session logs already hold the record.

The project-level queue reads at startup: it is short, so the cost is low, and a queue loaded on demand goes stale because the demand never comes while the handoff carries enough context to proceed. Sub-project or function-specific queues read at activation.

Queues take the shape of the work: a priority queue lists what to work on next by urgency or category (active, follow-up, backlog); a living checklist tracks items worked through during a session, checked off as they complete. Projects use one, the other, or both.

A complex project may split its queue by function or sub-project, each small and focused; one combined queue grows beyond what any session needs and costs context on items irrelevant to the current work.

---

## Permissions

The project expects four things of the platform's permission system: the AI reads wherever the user allows; it writes inside the project folder; everything else prompts, every destructive shell command included; and the user chooses how much runs without asking. Each platform has its own mechanism for this, and the part is rebuilt for each platform rather than carried over. The Claude Code mechanism is in the [setup guide](claude-code-setup.md#5-configure-permissions).

---

## Known Limitations

**A local folder session required.** Requires an AI that can open the project folder, read and write it, and follow its instructions in every session, in an application that keeps session transcripts on disk. A session that cannot reach the folder cannot run the project.

**Built-in memory.** If your AI application has a memory feature of its own, this system works with it on or off. With it on, you may find duplication between memory and filesystem state; with it off, the filesystem is the sole source of continuity. Either way the files stay the record, as Portable by Design (Key Principles) requires.

---
*Part of [AI Project Architect](https://github.com/vbiroshak/ai-project-architect) — Version 4.11*
