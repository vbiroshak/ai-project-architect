# Workspace Architecture for Sustained Knowledge Work with AI

Version 4.5

A workspace architecture designed for continuity across sessions.

Developed through iterative design and daily use across multiple projects spanning different domains. Applicable to any project where an AI assistant serves one or more areas of ongoing work.

---

## The Problem

Default AI project tools aren't designed for sustained knowledge work. Project knowledge files are static uploads. There is no session continuity: each conversation starts blank. There is no mechanism for the AI to maintain its own documentation, log sessions, or orient itself in ongoing work.

The workspace pattern solves this by moving project knowledge to files on your filesystem that the AI reads, writes, and maintains directly.

This document describes the architecture: the principles, patterns, and file roles that make the system work. It is platform-agnostic. For setup instructions specific to your platform:

- **Chat:** [Setting Up in Chat](chat-setup.md)
- **Code:** [Setting Up in Claude Code](claude-code-setup.md)
- **Migration:** [Migrating from Chat to Code](chat-to-code-migration.md)

---

## The Inbox

Inbox/ at the project root is the asynchronous interface between the user and the project, in both directions.

The user drops files here between sessions: emails saved as text, documents to process, screenshots, reference material, delegation briefs, anything that a project needs to see. The AI checks the inbox at every startup, lists the files, and offers to process them.

The AI writes to the Inbox when it has something for the user: drafts for review, items flagged for deletion, cross-project delegation notes, or anything that needs the user's attention outside the current conversation.

This is a foundational workflow in both directions. The user encounters something relevant, saves it to the appropriate project's inbox, and moves on. The AI produces a draft or flags a file and places it in the inbox for the user to find. The inbox bridges the gap between when work arrives and when the project is active, regardless of which direction it flows.

Inbox items are listed (filenames only) at startup but not read. The listing surfaces what's waiting, and the session processes items when directed or when relevant to the work.

Inbox contents can change at any time between messages.

Inbox items may represent undocumented task entries, work that has arrived but hasn't been triaged into the project's task list or session log. If you use a coordinator project (see Knowledge Architecture below), its task review should include inbox listings for this reason.

---

## Key Principles

### Instruction Composition: Actions, Not Conditions

Every instruction must be composed as explicit action sequences, not conditional triggers. AI assistants follow actions reliably. They do not reliably evaluate conditions before acting.

"When X, do Y" assumes the AI will check X first. It often won't. "Do A to check X. If X, do Y" works because the check is itself an action. Sometimes the check needs a method: "Check if A is available by doing B."

This applies at every level: project instructions, startup procedures, sub-project reference files, inbox checks, temporal awareness steps. Every conditional phrase ("when," "if," "once," "after") is a candidate for conversion into an explicit action step.

The failure mode is subtle because conditional instructions read as clear to a human. Clarity to a human reader is not the bar. The bar is whether the instruction composes as an action the AI will execute, rather than a condition the AI is expected to evaluate before acting.

### Directory Design Is UX Design

The directory structure is a user interface. When someone opens the project folder, the visual hierarchy should communicate the project's organization without explanation. Sub-project folders tell you what the project does. Infrastructure is visually subordinate. Inbox is immediately accessible.

Naming: natural case (Inbox, not INBOX). ALLCAPS reads as system files in a file browser. Folder names should feel natural alongside the user's other directories.

### Handoff-Driven Orientation

Orientation and archive are separate functions that need separate files. Session logs are the archive. HANDOFF.txt is the orientation. Loading the archive at startup conflates the two and wastes context on historical content that doesn't help the current session continue the work.

Handoff notes flag known fragilities, not just steps. A task with hidden complexity needs a caution line naming the risk and pointing to documentation.

### Lean Governing Document, Structural Index

The governing document keeps only what earns its place in every context window: project description, logging guidance, and project context. In Chat, the governing document (WORKFLOW.txt) also contains the startup procedure directly. In Code, the startup procedure lives in a separate file (CLAUDE.md) that imports the governing document (PROJECT_CONTEXT.md).

The project's file structure lives in PROJECT_INDEX.txt: a pure structural index listing what exists and where. It is not a container for domain knowledge, procedures, or format specifications — those belong in the governing document (if they earn their place in every context window) or in sub-project reference files (if they're domain-specific). Both files read at startup, but they serve different roles: the governing document carries procedure and behavioral rules, PROJECT_INDEX carries the structural map.

### Concise Logging

Session logs capture every decision, state change, and rationale. They do not narrate the conversational process.

One log per session, numbered to match the session number. Numbering is sequential across the project.

Thoroughness applies to coverage (what is captured). Conciseness applies to expression (how it is written). These are not in tension.

Good: "Moved Q1 reports into Client A sub-project. Reduces root clutter, reports are client-specific. Summary spreadsheet absorbed (same data, different format)."

Unnecessary: "We discussed whether to keep the Q1 reports at root level. The user pointed out they're client-specific. We agreed moving them made more sense."

Reasoning IS worth capturing when a decision might be revisited: "Chose X over Y because Z." Process narration ("first we considered A, then B") is not, unless the alternatives themselves are important context.

Log without waiting to be asked. When substantive work has accumulated, write the session log and handoff. Logging is insurance against context loss, not a signal that work is finishing. After writing a log entry, continue working without shifting tone, offering to wrap up, or prompting for next steps.

### Inbox: Verify and Check Before Referencing

List the inbox directory before any reference to its contents. This applies at startup, before mid-session processing, before mentioning inbox items to the user, and before writing inbox references into the handoff. Inbox contents change between messages. The user adds and clears items at any time. No earlier listing, and no handoff text, is a reliable substitute for the current directory state.

Before assessing an inbox item, check the project's existing work structure (sub-projects, case folders, task queues, archives) for related items. A fresh session has no memory of past work. Directory listings are the recognition mechanism. Without this step, a session may treat a familiar item as new, failing to connect it to work the project has already done.

### Fix on Contact

When you encounter stale or incorrect information in a project file during normal work, fix it then and there before continuing with other work. Do not defer in any form — noting it for later, flagging it as pending, or adding it to a task list all count as deferring. If a completed task is still on the task queue, remove it. If a status file contradicts the handoff, update it. If a reference file lists a structure that has changed, correct it. The cost of fixing on contact is a few seconds. The cost of deferring is a stale file that misleads the next session.

### Evolving State, Not Binary

Topics that develop across sessions must be logged at their current state of progress, not as binary open/closed. A design question progresses: not yet discussed → context gathered → options identified → partially decided → resolved. Binary logging ("open questions") forces the next session to restart from scratch on topics where significant work was done.

Each in-progress item should capture: what information was gathered, what options were considered, where the person's thinking landed, and what specifically remains. This protects the human from repeating themselves. Their memory of conversational decisions fades between sessions just as the AI's context window ends.

See the companion pattern: [Evolving State in Handoffs](patterns/evolving-state.md).

### Act at the Moment of Decision

When a conversation produces a decision, execute it immediately rather than logging it for future action. A decision captured only as a to-do item requires the next handler — human or AI — to reconstruct the reasoning behind it. A decision executed immediately preserves the reasoning in the action itself.

### Session Logs Are Project-Wide

One sequence, tagged by functional area. This maintains the project narrative and avoids duplicating logging infrastructure.

### Project Context Accumulates

The governing document includes a section for project-specific material that earns its place in every context window but is not covered by account-wide user preferences. When the user corrects a project-specific behavior, the AI writes it here immediately. The project learns its operational context over time.

Account-wide preferences (formatting, communication style, interaction patterns) are already delivered via the AI application's user preference system and should not be duplicated in the governing document.

---

## Factual Grounding

AI assistants tend to fill information gaps with plausible-sounding content rather than acknowledging uncertainty. Three techniques may reduce it:

1. **Permission to not know.** When unsure of a fact, say so and offer to find out (search, read a file, ask the user). Uncertainty plus initiative, not a dead end.

2. **Ground in source material first.** When working from documents or files, read and extract relevant content before acting on them. Do not infer what a document says from context or training data.

3. **Verify and cite.** When making factual claims, search to verify and cite the source. When a claim cannot be supported, say so rather than presenting it as fact.

Techniques 1 and 2 are general behavioral guidance — they apply broadly but are not installed by this architecture. Place them in account-wide user preferences, an output style, or project-level instructions, wherever your setup places behavioral rules.

Technique 3 is installed per-project via the project context template. It scopes verification to the project's domain:

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

All architecture-prescribed files carry both freshness lines: WORKFLOW.txt (Chat) or PROJECT_CONTEXT.md (Code), HANDOFF.txt, PROJECT_INDEX.txt, STATUS files, TASKS.txt, INDEX.txt files, sub-project reference files, and LESSONS_INDEX.txt. The title line carries only the file's identity. Freshness lines occupy lines 2-3.

Session logs do not carry freshness lines (they are append-only historical records with timestamps in their entries). In Chat projects, the Clock file (used for temporal awareness) is also excluded — it is a mechanism file, not a content document.

Archived files retain whatever freshness lines they had at the time of archiving. Do not maintain freshness lines on files after they are archived. During the archiving process itself, refresh both freshness lines as part of the closing write (the closing note changes content and confirms final state).

Documents in a shared knowledge base folder that carry version numbers (Version X.X — Month YYYY) keep them instead of freshness lines. Version numbers serve a different purpose: they identify which version of a pattern has been adopted. All other shared files (README, INDEX files, templates, examples) use standard freshness lines.

### New Files

When creating a new file, set both freshness lines to the creation date and session. Do not use "Created:" or leave the lines blank. Every file starts with both lines populated from the moment it exists.

Domain files (working documents inside sub-projects that are not architecture-prescribed) also benefit from adopting the freshness standard. The more files that carry freshness lines, the easier it is to assess the currency of any file at a glance. When creating or editing domain files, add the standard freshness lines.

### Maintenance

Freshness lines are maintained as part of existing workflow triggers, not as a separate procedure:

- **Paired writes:** When writing a log entry and overwriting the handoff, refresh the handoff's freshness lines. When overwriting a STATUS file as part of the same paired write, refresh its freshness lines. For files that are overwritten wholesale (HANDOFF, STATUS files rewritten during state changes), both lines carry the same date because rewriting is both an update and a review.
- **Fix on Contact:** When correcting stale or incorrect information in any file, refresh both "Last updated" and "Last reviewed" (you changed the content and confirmed the rest).
- **Structure verification:** When verifying PROJECT_INDEX.txt after directory structure changes, refresh "Last updated" if content changed, and refresh "Last reviewed" regardless (you just confirmed it).
- **Task queue review:** When reading the task queue at startup and fixing completed items, refresh "Last reviewed" (you just confirmed the list is current). If you added or removed items, also refresh "Last updated."
- **Sub-project reference files:** When reading a sub-project reference file during substantive work, refresh "Last reviewed" before writing the session log. If you changed content, also refresh "Last updated."

### Governing Document Integration

The governing document's SESSION LOGS section carries a compressed version of the definitions and maintenance rules so that every session has them in context. The full specification lives in this document; the governing document carries the operational instructions:

```
FRESHNESS LINES: Every project file (except session logs;
in Chat projects, also the Clock file) carries two lines
after its title:

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

A single file that keeps growing means the AI reads everything just to find one item. A lessons file or reference document is fine when it has five entries. At fifty entries it costs thousands of tokens every time it's read. Files that grow by accretion will eventually consume a meaningful share of the context window just to look up one item.

The indexed pattern avoids this. Like a card catalog in a library, read the index to know what's available, then pull only the file you need. Cost is ~1 KB for the index read plus the one file you actually need, regardless of how large the collection grows. Adding a new entry costs ~1.5 KB of context (read index, read one topic file, write the update). Compare to reading and rewriting a monolithic file that grows without bound.

This pattern applies anywhere items accumulate and get looked up selectively: operational lessons, case evidence, research sources, reference materials, design decisions.

Standing rule: any folder where a reader needs to discover and selectively access its contents gets an INDEX.txt at creation time, not retroactively. This includes domain folders, reference collections, case evidence, research materials — anywhere a reader would otherwise need to open every file to know what's there. It does not include infrastructure folders with architecturally defined contents where the files have known roles.

The reader is not just the current session. Indexes serve future sessions (token-efficient retrieval), the user browsing the folder (directory design as UX extends into folder contents), other projects reading cross-project files, and any new AI account or system absorbing the project from the filesystem (portability). The project filesystem is designed to be portable — a new account with the project files can pick up the work. An index in every document folder is what makes that practical without brute-force reading.

Indexes serve retrieval, not just growth. A static folder with five files benefits from an index just as much as a growing one. Creating an index empty or with a placeholder costs nothing and ensures the pattern is never missed. The failure mode is a session judging that a folder doesn't need an index because it won't grow.

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

**Sub-project reference files:** Domain-specific knowledge managed by each sub-project in whatever form serves the work. A client management sub-project has case files and communication logs. A research sub-project has analytical frameworks and source annotations. A media sub-project has taste profiles and tracking lists. Reference files are kept updated to reflect the current state of the sub-project.

Domain knowledge always lives in sub-project files, not in the project-level PROJECT_INDEX.txt. When a sub-project accumulates context, write that content into a file inside the sub-project directory. The project-level PROJECT_INDEX.txt carries a pointer to the sub-project file and a one-line scope description — never a summary or duplication of the content itself.

**Project operational lessons:** Cross-cutting knowledge that any sub-project might need. What worked, what didn't, patterns observed across cases, tool workarounds, and procedures that apply across areas. Centralized in a Lessons/ directory with an index routing to topical files. When a sub-project discovers something operationally useful, it surfaces here.

**Shared knowledge base (optional):** A folder, separate from your project directories, that all your projects have access to. Cross-project knowledge published as standalone entries. One project discovers a technique, documents it portably, publishes it. Other projects encounter it and adopt, adapt, or ignore it. This is how projects teach each other. Only relevant if you're running multiple projects.

The direction is always upward: sub-project reference files → project Lessons/ → shared knowledge base. Each level is a different formalization with a broader audience.

Session search is typically project-scoped — built-in session search usually only sees conversations within the current project. But the filesystem spans everything. When you need cross-project context, the AI reads the other project's files directly.

### Cross-Project Routing via Coordinator Inbox

When a project discovers something cross-cutting during its own domain work, it doesn't need to know the shared knowledge base structure or make the routing decision itself. The pattern: the project packages the observation as a concise note (what was noticed, why it matters, where it might belong), and routes it to the coordinator project's inbox. The coordinator reads the note, decides where it belongs, places it, and clears the inbox.

Not every cross-cutting observation warrants a new shared document. Many are feedback on existing infrastructure: a note that improves an existing doc, a line item for a project's lessons file, or a correction to a shared template. The routing mechanism is the same regardless of destination. The coordinator has the cross-project view to decide.

The note should include: the observation itself, the source (which project and session), and a suggestion for where it might land. The suggestion is advisory. The coordinator may route it differently based on its view across all projects.

### The Coordinator Project

When you run multiple projects, you can create one project as a meta-project coordinator to develop and maintain the system they all share. It uses the same workspace architecture as every other project. Its domain work is the architecture itself.

The coordinator is where you can do design work on the workspace system, maintain the shared knowledge base, propagate structural changes, audit projects for consistency, test improvements, and manage cross-project delegations. It can also serve as a gateway for cross-project visibility: summarizing task queues across all projects, helping prioritize between competing demands in different projects, and giving you a single place to ask "what's pending across everything?" Every project can read every other project's files. The coordinator uses this to read handoffs, task queues, and inboxes across all projects, write delegation notes, and verify that changes have been applied.

A coordinator project is not required. A single project or a few projects work fine without one. The coordinator becomes valuable when you have enough projects that cross-cutting concerns emerge: shared patterns that need to stay consistent, design changes that affect multiple projects, observations from one project that would benefit others.

Building a coordinator:

- Create it like any other project with the same workspace architecture.
- Its sub-project covers system-level work: architecture design, shared knowledge base maintenance, cross-project tracking, and any active design efforts.
- Its governing document describes the coordinator role and lists all the projects it manages.
- It maintains the shared knowledge base (a directory of standalone documents covering patterns and techniques that any project can consult).
- It uses the inbox mechanism in both directions: domain projects route cross-cutting observations to the coordinator's inbox, and the coordinator writes delegation notes to domain project inboxes.

The coordinator's relationship to domain projects is consultative, not controlling. Domain projects are self-sufficient. They read the shared knowledge base, apply the architecture's principles, and use their own judgment. A coordinator project allows you to work on the other projects without distracting them from their domain work.

---

## Sub-Projects

Each functional area gets its own directory at the project root. This directory is the authoritative home for all domain knowledge in that area. Everything the AI learns about the domain — case data, research threads, tracking lists, analytical frameworks, procedural notes — is written into files inside the sub-project directory. The project-level PROJECT_INDEX.txt points to these files but never holds domain content itself.

Always create at least one sub-project folder, even for single-focus projects, to establish the pattern and avoid restructuring later.

### Sub-Project Internal Structure

A sub-project's internal structure mirrors the project level: an orientation file for current state, a reference file for accumulated domain knowledge, and domain folders shaped by the work.

Standard file roles:

- **[SubProject]_STATUS.txt** — Orientation. Current state, what's active, what's pending, known issues. Read at activation. Overwritten as state changes. This is the sub-project analog of HANDOFF.txt at the project level. Required for any sub-project with ongoing work spanning multiple sessions.
- **[SubProject]_REFERENCE.txt** — Domain knowledge. Accumulated understanding, specifications, procedures, configurations consulted during work. Read on demand. Grows over time. When it grows large, apply the indexed collection pattern.
- **[named domain files]** — Working documents shaped by the domain. Case folders, design briefs, tracking lists, configuration files, research notes. Named for what they contain (e.g., voice_config.txt, not config.txt).
- **[domain folders]** — Cases/, Testing Reports/, Research/, etc. Shaped by the work.

**Naming rules:** Files inside sub-project directories must include the sub-project name or a domain-specific identifier. No generic names like STATUS.txt or REFERENCE.txt — these collide with each other when read into context. A session reading RESEARCH_STATUS.txt or TRACKING_REFERENCE.txt knows immediately what sub-project it belongs to. Exception: a sub-project with a single primary file may use a content-descriptive name instead (e.g., trust_analysis.txt). The test is whether the filename alone identifies the sub-project.

**Development trajectory:** A new sub-project starts with a status file and possibly a reference file. As work accumulates, named domain files and folders emerge. As domain files grow, the indexed collection pattern applies. The AI should recognize when infrastructure needs to develop and build it, following the patterns in this document and looking at how peer sub-projects have organized their work.

Standing rule: when a sub-project directory is created, seed it with at least a status file immediately. An empty sub-project directory gets skipped — the AI will write domain content into PROJECT_INDEX.txt instead, because that file already exists and has structure. A seeded status file gives the AI somewhere to put sub-project content from the start.

Sub-project structure depends on the shape of the work:

- Cases that open and close (client work, support tickets, disputes)
- Parallel ongoing projects (codebases, skill development)
- Sequential progression (chapters, assignments, phases)
- Themes or topics (research areas, product lines)
- Individuals (clients, correspondents, students)

Each shape implies different internal folders and reference file content.

### Migration

When a sub-project outgrows its parent project, it can be split into its own project. Build the new project's structure from inside the old project, move the directory, create the new AI project, move relevant session history, migrate session logs with provenance headers, update the old project. Migration is also an opportunity to add structure the work has grown into.

### Archiving

When a sub-project completes, it moves to Archive/ at the project root with a completion-date name (e.g., "Project Name - 2026-03"). The sub-project's status file gets a closing note before archiving. An ARCHIVE_INDEX.txt inside the Archive/ directory maintains an inventory of archived sub-projects for discoverability. Active sub-projects always live at root, never inside Archive/.

See the companion pattern: [Sub-Project Archive Pattern](patterns/archive-pattern.md).

---

## Project Complexity Tiers

The default setup gives you a baseline: state summarized in HANDOFF.txt, reference files loaded on demand, a lean startup procedure. As a project or sub-project grows in complexity, you can expand this baseline to give it more context at startup.

At the project level, this means adding more files to the startup procedure, reading more session logs by default, or growing the governing document to cover more operational detail. At the sub-project level, you can give a sub-project its own orientation file (named to clearly identify the area it covers) with detailed state, open questions at their current stage of thinking, and reading pointers to its own reference materials.

This is just a matter of degree — adding more reads, longer documents, richer orientation. Concise logging, indexed collections, and on-demand loading can all still apply.

### Separating Startup and Activation

For sub-projects with their own orientation files, you can separate startup and activation into distinct loading steps:

**Startup** (at session open): Follow the standard startup sequence. HANDOFF.txt carries the project's current state and pointers to orientation files for sub-projects that have them.

**Activation** (when work begins on a sub-project): Read the sub-project's orientation file. Read the session log referenced in its "last active" pointer, if different from the session log already loaded at startup. Report sub-project state to the user and wait for direction.

To set this up, include an explicit activation sequence for each sub-project in the governing document, specifying the files to read and their order. This keeps startup lean while giving complex sub-projects the full context load they need when activated.

---

## Task Queues

Active items only. When a task is completed, remove it from the queue and note completion in the session log. The session log is the archive. No DONE section, no archive file. A DONE section or archive creates a growing document that must be read and rewritten every time a task is completed. The context cost of maintaining an archive exceeds its value, since the session logs already contain the completion record.

The project-level task queue reads at startup. Task queues are short (active items only, no DONE section) and the cost of reading them is low. The alternative — on-demand loading — can lead to stale queues because the demand never comes when the handoff carries enough context to proceed. Sub-project or function-specific queues read at sub-project activation rather than startup.

Task queues take different shapes depending on the work. A priority queue lists what to work on next, organized by urgency or category (active, follow-up, backlog). A living checklist tracks items being worked through during a session, with items checked off as they're completed. Both are valid. Some projects use one, some the other, some both for different purposes.

Complex projects may need multiple task queues split by function or sub-project. Each queue stays focused on its domain and stays small. The alternative (one large combined queue) creates a file that grows beyond what any single session needs, costing context to read items irrelevant to the current work.

---

## Tool Guides

Tool guides are operational reference for using a specific capability well. They answer "how do I use this tool efficiently and correctly?" — front-loading the working approach so the AI doesn't have to rediscover it mid-session.

Tool guides live per-project in a Tool Guides/ directory, loaded on demand when work that uses the tool begins. They are not loaded at startup. Each guide is self-contained operational reference for one tool.

The repo carries tool guides as a collection ([tool-guides/](tool-guides/)) from which projects adopt what they need. A project that doesn't use Chrome doesn't need the Chrome guide.

Scope: tool guides cover universal tool behavior. Task-specific operational detail (how to fill out a particular form on a particular site, for example) belongs in domain files inside the relevant sub-project, not in the tool guide. The tool guide is the reusable layer; the domain file is the work-specific layer.

---

## Known Limitations

**Filesystem required for full functionality.** Requires an AI application with filesystem read/write access. Web and mobile interfaces don't have filesystem access. When accessing a project without filesystem access, the AI will note what needs syncing when filesystem access is next available.

**Project memory.** This system works with your AI application's project memory turned on or off. With memory on, you may find duplication between memory and filesystem state; with memory off, the filesystem is the sole source of continuity. Experiment with both to see what works for your use case.

---
*Part of [AI Project Architect](https://github.com/vbiroshak/ai-project-architect) — Version 4.5*
