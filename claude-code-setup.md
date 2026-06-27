# Setting Up in Claude Code

How to build and run a project using this workspace architecture in Claude Code. You can read [workspace-architecture.md](workspace-architecture.md) for the principles and patterns behind the system. To set up in Chat instead, see [chat-setup.md](chat-setup.md). To migrate an existing Chat project, see [chat-to-code-migration.md](chat-to-code-migration.md).

---

## What Code Provides

Claude Code gives the AI native filesystem access and several features this architecture uses:

- **[CLAUDE.md](https://code.claude.com/docs/en/memory)** — a markdown file at the project root that loads automatically into every session. Carries the startup procedure.
- **[Event hooks](https://code.claude.com/docs/en/hooks)** — scripts that run on specific events (session start, each user message, and others). Used for temporal awareness and transcript archiving.
- **[Settings](https://code.claude.com/docs/en/settings)** — project-level permissions controlling which files can be read or written, which shell commands are allowed without prompting, and which paths are denied.
- **[Output styles](https://code.claude.com/docs/en/output-styles)** — per-project behavioral profiles that modify the system prompt. Set role, tone, and output format without repeating instructions every turn.
- **[Auto memory](https://code.claude.com/docs/en/memory#auto-memory)** — notes Claude writes across sessions: build commands, debugging insights, preferences it discovers. Complements the project's own file-based memory.
- **[Skills](https://code.claude.com/docs/en/skills)** — reusable prompts invoked by name (`/skill-name`) or automatically when Claude recognizes a matching task. Each skill is a folder with a SKILL.md file plus supporting files.
- **[Subagents](https://code.claude.com/docs/en/sub-agents)** — specialized agents with their own context window, system prompt, and tool access. Run parallel work or isolated tasks without cluttering the main session.
- **[Rules](https://code.claude.com/docs/en/memory#organize-rules-with-claude/rules/)** — topic-scoped instructions in `.claude/rules/` that can be gated by file path, loading only when Claude works with matching files.
- **Native shell access** — Bash commands run directly on the local filesystem.

---

## The Code Project Structure

CLAUDE.md at the project root is the entry point (auto-loaded every session). PROJECT_CONTEXT.md is the governing document. Project infrastructure lives in a Project/ directory.

```
[Project]/
  CLAUDE.md                   auto-loaded startup procedure
  .claude/                    Code configuration
    settings.json             permissions, hooks, memory redirect
    settings.local.json       output style, personal overrides (gitignored)
    hooks/                    event scripts (optional but recommended)
    output-styles/            behavioral profiles (optional)
    skills/                   reusable prompts (optional)
    agents/                   specialized subagents (optional)
    rules/                    path-scoped instructions (optional)
  Inbox/
  Project/                    project infrastructure
    PROJECT_CONTEXT.md        governing document
    HANDOFF.txt
    PROJECT_INDEX.txt
    TASKS.txt                 (optional — Code has built-in task tools)
    CHANGELOG.txt             (optional)
    Claude Memory/            (optional — auto memory redirect)
    Lessons/                  (optional — auto memory can cover this)
    Tool Guides/              (optional — project-specific guides only)
    Session Logs/
      Session_XXXX.txt        4-digit, one per session
    Sessions/                 (created by archive hook if set up)
  [Sub-Project A]/
  Archive/
```

The core that every Code project needs: CLAUDE.md, PROJECT_CONTEXT.md (or equivalent governing document), HANDOFF.txt, PROJECT_INDEX.txt, Session Logs/, at least one sub-project directory. Everything else is optional and depends on what serves the work.

**What's optional and why:**

- **TASKS.txt** — Code has a built-in task system that tracks items within a session. A file-based task queue is useful for cross-session visibility that doesn't depend on Code's task tools, but either approach works. If used: active items only, no DONE section. When a task completes, remove it from the queue and note completion in the session log.
- **Claude Memory/** — Code's [auto memory](https://code.claude.com/docs/en/memory#auto-memory) works fine in its default location (`~/.claude/projects/`). Redirecting it into the project via `autoMemoryDirectory` in settings.json puts the memory files where the project can see and manage them, but it's a preference, not a requirement.
- **Lessons/** — auto memory captures behavioral lessons automatically. A separate Lessons/ directory with an index is more structured and portable, but for many projects auto memory covers it.
- **Tool Guides/** — Code has built-in knowledge of its own tools. Project-specific tool guides (like Chrome usage patterns for a project that uses the Chrome extension) still add value.
- **Sessions/** — created automatically by the transcript archiving hook (see Hooks below). Not needed if you don't set up the hook.
- **CHANGELOG.txt** — useful for projects with infrastructure changes to track; optional for simpler projects.

---

## Architecture Essentials

The principles and patterns needed to operate a Code project. The full architecture is documented in [workspace-architecture.md](workspace-architecture.md).

### The Inbox

Inbox/ at the project root is the asynchronous interface between the user and the project, in both directions. The user drops files for processing between sessions; the AI writes drafts, deletion flags, or anything needing the user's attention outside the current conversation. Contents are listed (filenames only) at startup but not read — items are processed when directed or relevant. Contents can change at any time. List the directory before any reference to its contents: at startup, before mid-session processing, and before writing inbox references into the handoff.

### Sub-Projects

Each functional area gets its own directory at the project root. Standard file roles inside a sub-project:

- **[SubProject]_STATUS.txt** — orientation. Current state, what's active, what's pending. Read at activation.
- **[SubProject]_REFERENCE.txt** — domain knowledge. Accumulated understanding consulted during work. Read on demand.
- **Domain files and folders** — shaped by the work.

Sub-project names must be in the filename (RESEARCH_STATUS.txt, not STATUS.txt) so the file identifies itself when read into context. Every sub-project directory gets at least a status file at creation.

Activation: read the status file, read everything the handoff identifies for that sub-project, load additional files as needed. Domain knowledge produced during work goes into files inside the sub-project directory, not into PROJECT_INDEX.txt.

When a sub-project completes, move it to Archive/ at the project root with a completion-date name (e.g., "Project Name - 2026-03"). Add a closing note to the status file before archiving. ARCHIVE_INDEX.txt inside Archive/ tracks inventory.

For sub-projects whose complexity outgrows a handoff summary, see [Sub-Project Complexity Tiers](workspace-architecture.md#sub-project-complexity-tiers) in the architecture doc — the Extended tier provides richer orientation with its own status file and activation sequence.

### Operating Principles

**Fix on contact.** When you encounter stale or incorrect information in any project file during normal work, fix it then and there. Do not defer — noting it for later, flagging it as pending, or adding it to a task list all count as deferring.

**Evolving state.** Log topics at their current state of progress, not as binary open/closed. Capture what was gathered, what was considered, where thinking landed, and what remains. Each in-progress item should let the next session continue where this one stopped.

**Act at the moment of decision.** When a conversation produces a decision, execute it immediately rather than logging it for future action.

**Concise logging.** Session logs capture every decision, state change, and rationale. They do not narrate the conversational process. One log per session, numbered to match the session number. Each entry starts with a header: `[Date, ~Time Timezone] TOPIC`. Write when work accumulates; never defer to end of session.

**Paired writes.** Every log entry is paired with a HANDOFF.txt overwrite — both happen together, every time. When the entry covers sub-project work, verify the sub-project's status file reflects the current state. When file operations change directory structure, verify PROJECT_INDEX.txt.

**Handoff-driven orientation.** Session logs are the archive; HANDOFF.txt is the orientation. The handoff gives the current state snapshot. It is overwritten fresh (not appended). Three sections: ACTIVE WORK, STANDING ITEMS, FOR DEPTH.

**Instruction composition.** Write instructions as explicit action sequences, not conditional triggers. "Do A to check X. If X, do Y" works reliably. "When X, do Y" assumes the AI will check X first — it often won't.

### Freshness Tracking

Every project file (except session logs) carries two lines after its title:

```
Last updated: [Month DD, YYYY] (Session NNN)
Last reviewed: [Month DD, YYYY]
```

"Last updated" means content was intentionally changed. "Last reviewed" means content was read and confirmed accurate during substantive work. A correction refreshes both. For files overwritten wholesale (HANDOFF, STATUS) or newly created, both lines carry the same date and session. See [workspace-architecture.md](workspace-architecture.md#freshness-tracking) for the full specification.

### The Indexed Collection Pattern

Any content that accumulates and is consulted selectively gets an index file plus a collection of small files: one per topic. Read the index to find what's available, pull only the file you need. This avoids monolithic files that grow without bound and cost thousands of tokens every time they're read. Applies to lessons, research sources, reference materials, case evidence. Every folder where a reader needs to discover its contents gets an INDEX.txt at creation time.

### Factual Grounding

When unsure of a fact, say so and offer to find out. When working from documents or files, read and extract relevant content before acting on them. For verifiable claims in the project's domain, verify via search rather than relying on training data.

### Temporal Awareness

AI assistants have no internal clock and cannot estimate, infer, or guess the time. The temporal-awareness hook (see [step 4](#4-set-up-hooks)) solves this by injecting the current local time into every turn. The AI receives an accurate time reference automatically before processing each user message, with no tool call or file read required. The PROJECT_CONTEXT.md template includes a Temporal Awareness section that tells the AI how to use the injected time — consult it before greetings, "today"/"this morning" references, and elapsed-time remarks.

For the design rationale behind this approach, see the [Temporal Awareness](patterns/temporal-awareness.md) pattern.

### Knowledge Architecture

Knowledge flows upward through three levels: sub-project reference files (domain-specific), project-level Lessons/ (cross-cutting operational knowledge), and an optional shared knowledge base (cross-project). Each level is a different formalization with a broader audience. When running multiple projects, a coordinator project can maintain the shared knowledge base and handle cross-project visibility.

---

## Fresh Setup

To build a new project in Code using this architecture:

### 1. Create the project directory

Create the project directory with this structure:
- CLAUDE.md at the root (step 2)
- Project/ containing HANDOFF.txt, PROJECT_INDEX.txt, and Session Logs/
- Inbox/ for asynchronous items between you and the AI
- At least one sub-project folder for the project's domain work

The following components are optional. If you are an AI building this for a user, ask the user about each one and explain what it does so they can make an informed decision:

| Component | What it does | Where it goes |
|-----------|-------------|---------------|
| Task queue | File-based cross-session task tracking | Project/TASKS.txt + section in PROJECT_CONTEXT.md + `@` import in CLAUDE.md |
| Auto memory redirect | Makes auto memory files visible inside the project | `autoMemoryDirectory` in settings.json + Project/Claude Memory/ |
| Additional directories | Read access to folders outside the project | `additionalDirectories` in settings.json |
| Tool guides | Pre-read reference for specific tools | Section in PROJECT_CONTEXT.md + Project/Tool Guides/ |
| Shared knowledge base | Cross-project shared resources | Section in PROJECT_CONTEXT.md |
| Output style | Role, tone, and behavioral profile | .claude/output-styles/ + `outputStyle` in settings.local.json (step 6) |
| Lessons directory | Structured operational knowledge | Project/Lessons/ with index |
| Changelog | Record of structural/infrastructure changes | Project/CHANGELOG.txt |

See the directory tree in [The Code Project Structure](#the-code-project-structure) above for the full layout. The [Code templates](templates/claude-code/) provide starting content for [CLAUDE.md](templates/claude-code/CLAUDE-template.md), [PROJECT_CONTEXT.md](templates/claude-code/PROJECT-CONTEXT-template.md), [PROJECT_INDEX.txt](templates/claude-code/PROJECT-INDEX-template.md), and [settings.json](templates/claude-code/settings-template.json). For HANDOFF.txt format, see the [handoff template](templates/mandated-files/handoff.md).

### 2. Create CLAUDE.md

[CLAUDE.md](https://code.claude.com/docs/en/memory) loads automatically at the start of every session. It carries the startup procedure: the sequence of files to read for orientation.

```
# [Project Name]

## Session Startup Procedure

At session start, execute every step below in order before responding. Every step is required regardless of the user's first message.

1. Orientation files:
   @Project/PROJECT_CONTEXT.md
   @Project/PROJECT_INDEX.txt
   @Project/HANDOFF.txt
   @Project/TASKS.txt              [if using a task queue file]

2. Find and read the most recent session log:
   ls "Project/Session Logs/" | tail -5
   Read the most recent, plus any additional logs the handoff identifies.

3. List Inbox contents (filenames only, don't read):
   ls Inbox/

4. Greet briefly. Then present a brief orientation: where work left off, what's pending, any Inbox items. One item per line, not education on what each item is about. Ask how the user would like to begin.

If you are reading this after context compaction, re-read
Project/PROJECT_CONTEXT.md in full before continuing.
```

The `@` syntax imports files into context at load time — see [CLAUDE.md imports](https://code.claude.com/docs/en/memory#import-additional-files). The compaction re-read line ensures the AI reloads its governing document when the [context window is compressed](https://code.claude.com/docs/en/context-window) mid-session.

Add project-specific startup steps (sub-project activation, task queue reads, domain-specific loads) as additional numbered steps. Keep CLAUDE.md under 200 lines — instructions beyond that length reduce adherence.

### 3. Create PROJECT_CONTEXT.md

PROJECT_CONTEXT.md is the governing document: the substantive operating knowledge every session needs from the first message. The startup procedure lives in CLAUDE.md; everything else lives here.

The [PROJECT_CONTEXT template](templates/claude-code/PROJECT-CONTEXT-template.md) provides the full deployable text with all standard sections: What This Project Does, Sub-Project Activation, Session Logs, Handoff, Inbox, Temporal Awareness, and Project Context, plus optional sections for Tool Guides, Task Queue, and Shared Knowledge Base.

### 4. Set up hooks

Create `.claude/hooks/` in the project directory and register them in `.claude/settings.json`. Three hooks provide the core session infrastructure:

**Temporal awareness** (UserPromptSubmit): Injects the current local time into every turn. The AI receives the time automatically before processing each message.

**Transcript archiving** (SessionStart): Copies the previous session's transcript into the project's Sessions/ directory with a readable name derived from the session content. To get readable filenames (e.g., `MyProject_0042.jsonl` rather than a UUID), open each session with a declaration line like "This is MyProject 42." The archiver extracts the name and number from this line.

**Transcript renderer** (companion script): Renders each archived transcript as a readable Markdown file (collapsed view: messages in full, tool calls as one-line summaries). The archiver imports the renderer automatically when it's alongside it.

Hooks communicate context back to the session by printing a JSON object to stdout with an `additionalContext` field inside `hookSpecificOutput`. This context appears as a system reminder attached to the user's message. The temporal-awareness hook uses this to inject the formatted local time so the AI receives it automatically before processing each turn.

All three scripts go into `.claude/hooks/`. See [templates/claude-code/](templates/claude-code/) for deployable versions. If you have a working project, copy its hooks and surgically edit the project name — don't rewrite from scratch, which risks introducing accidental differences.

When a hook produces derived data that the session will query (e.g., a regenerated index or extracted text), use a blocking hook at SessionStart rather than async. The cost is paid once per session; async creates a race condition where the session queries stale data.

### 5. Configure permissions

`.claude/settings.json` controls what the AI can access and which hooks run. See [templates/claude-code/settings-template.json](templates/claude-code/settings-template.json) for a deployable template.

```json
{
  "autoMemoryDirectory": "/absolute/path/to/your/project/Project/Claude Memory",
  "additionalDirectories": ["/path/to/sibling/resources"],
  "permissions": {
    "allow": [
      "Read(//path/to/external/resources/**)",
      "Bash(grep *)",
      "Bash(find *)"
    ],
    "deny": [
      "Edit(//path/to/read-only-sources/**)",
      "Write(//path/to/read-only-sources/**)"
    ]
  },
  "hooks": {
    "SessionStart": [
      {
        "hooks": [{ "type": "command", "command": "python3 \"${CLAUDE_PROJECT_DIR:-$PWD}/.claude/hooks/archive-transcripts.py\"" }]
      }
    ],
    "UserPromptSubmit": [
      {
        "hooks": [{ "type": "command", "command": "python3 \"${CLAUDE_PROJECT_DIR:-$PWD}/.claude/hooks/temporal-awareness.py\"" }]
      }
    ]
  }
}
```

Key points:

- **`autoMemoryDirectory`** — redirects auto memory into the project. Requires an absolute path or `~/`-prefixed path. Optional: Code's default location works fine if you don't need the memory files visible inside the project.
- **`additionalDirectories`** — grants access to folders outside the project root. Useful for reading sibling projects or shared resource directories.
- **Deny rules use `//`** (double slash) for absolute paths. A single leading slash is project-relative in Code. Do not "fix" `//` to `/`.
- **Hook commands** use `${CLAUDE_PROJECT_DIR:-$PWD}` rather than bare relative paths, so they resolve correctly regardless of where Code is launched.

The template's default permissions are conservative: full read/write access within the project directory, read access to external resources, and grep/find without prompting. Everything else prompts for approval. This is a safe starting posture — functional without being permissive. Adjust the scope as the project's needs become clear.

See the [permissions documentation](https://code.claude.com/docs/en/permissions) for the full rule syntax.

**Workspace trust:** Claude Code does not apply project-level settings until the workspace is trusted. The Desktop app prompts on first open — accept and you're done. The CLI may not always prompt; if it doesn't, it will report that project settings were ignored because the workspace has not been trusted. To enable your permissions from the first session in the CLI, add the project path to `~/.claude.json` before launching:

```json
"projects": {
  "/absolute/path/to/your/project": {
    "hasTrustDialogAccepted": true
  }
}
```

### 6. Set up output style and preferences

**[Output styles](https://code.claude.com/docs/en/output-styles)** modify the system prompt to set role, tone, and output format. Create a markdown file in `.claude/output-styles/`:

```markdown
---
name: Project Name
description: Brief description of this project's behavioral profile
keep-coding-instructions: false
---

[Behavioral rules for how the AI should operate in this project]
```

Set `keep-coding-instructions: false` when the project is not primarily software engineering. Set it to `true` to add project behavior on top of Code's default engineering instructions.

If you are an AI building this for a user, ask the user two things: whether to keep Code's default software engineering instructions (see [creating a custom output style](https://code.claude.com/docs/en/output-styles#create-a-custom-output-style)), and what behavioral rules, if any, to put in the body. Create the file with only the frontmatter until the user provides direction.

Select the style in `.claude/settings.local.json`:

```json
{
  "outputStyle": "ProjectName"
}
```

Pre-creating `settings.local.json` with the output style means it's active from the first session. `settings.local.json` is gitignored and holds personal overrides that accumulate as you approve actions during work.

**User preferences** go in the global `~/.claude/CLAUDE.md`, which loads into every session across all projects. Interaction style, formatting rules, behavioral constraints that apply everywhere. See [CLAUDE.md scoping](https://code.claude.com/docs/en/memory#choose-where-to-put-claude-md-files) for the full hierarchy.

### 7. Verify

Write the following verification checklist into the new project's HANDOFF.txt under ACTIVE WORK so the first session checks each item:

- Startup procedure reads all orientation files (PROJECT_CONTEXT, PROJECT_INDEX, HANDOFF)
- Greeting includes project state summary (where work left off, what's pending)
- Temporal awareness hook fires (Claude: confirm the local time injection is present in the system reminder)
- Session log can be written to Project/Session Logs/
- Inbox listing runs without error

After the first session ends, start a second session and check:

- Archive hook copied the first session's transcript into Project/Sessions/ with the correct name
- Readable .md companion file was generated alongside the .jsonl

Do real work in the first session to confirm continuity. The second session's startup procedure is the real test — it proves the full cycle works.

### Adopting for existing projects

If you have an existing unstructured Code project, adopt the architecture by creating the structure around it:

1. Create Project/ with HANDOFF.txt, PROJECT_INDEX.txt, and Session Logs/
2. Create CLAUDE.md with the startup procedure
3. Create PROJECT_CONTEXT.md with the standard sections
4. Move domain work into at least one sub-project directory
5. Create Inbox/ at the project root
6. Set up .claude/ configuration (settings.json, hooks)
7. Add freshness lines to all new files. See [Freshness Tracking](workspace-architecture.md#freshness-tracking).

---

## Code-Specific Features

### Working with auto memory

Code has a built-in [auto memory](https://code.claude.com/docs/en/memory#auto-memory) system where it stores notes across sessions: build commands, debugging insights, preferences it discovers. For projects using this workspace architecture, the project files themselves are the primary memory (the handoff, session logs, status files, and project context carry everything a session needs). Auto memory serves a different purpose: it captures behavioral knowledge about how to work with you and with the project's tooling.

Two reasonable approaches:

**Redirect auto memory into the project.** Add `"autoMemoryDirectory": "Project/Claude Memory"` to settings.json. This puts the memory files inside the project's infrastructure where they're visible and manageable. The project files govern; a note that contradicts them is stale and deleted on contact.

**Use both layers as-is.** Let auto memory handle what it's designed for (behavioral preferences, tool quirks, correction patterns) in its default location while the project architecture handles what it's designed for (work state, decisions, orientation). These are complementary: auto memory is a small notebook about how to work; the project files are the record of what work was done.

### Managing accumulated permissions

Claude Code maintains `settings.local.json` that accumulates "always allow" grants as you approve actions during work. Over time this file can grow with grants you approved without fully understanding their scope (MCP tool allows are tool-wide, not per-action; Bash allows match by prefix). Periodically review it and clear grants that are too broad. The project `settings.json` is the deliberate policy; `settings.local.json` is the accumulated ad-hoc grants.

### On-demand reads and trigger maps

For projects with substantial domain reference material (style guides, process documents, reference files), loading everything at startup wastes context. Code's larger effective context makes it tempting to load more, but the principle holds: read what you need when you need it.

A trigger map in PROJECT_CONTEXT.md names the files, their recognition cues, and what they guard against. The model applies these by judgment — when it recognizes the work type, it loads the relevant files before proceeding. This keeps startup lean while ensuring domain knowledge is loaded before the work that needs it, not after.

### Skills, subagents, and rules

These are optional extensions that develop as the project matures.

**[Skills](https://code.claude.com/docs/en/skills)** are reusable prompts for repeating workflows. Each skill lives in `.claude/skills/<name>/SKILL.md` and can bundle supporting files (checklists, templates, reference docs). Invoke with `/name` or let Claude invoke automatically when it recognizes a matching task. Use `disable-model-invocation: true` in the frontmatter for workflows you want to trigger yourself. Skills load only when invoked, keeping startup lean. Skills and agents defined at `~/.claude/` (user level) are available across all projects.

**[Subagents](https://code.claude.com/docs/en/sub-agents)** are specialized agents with their own context window, system prompt, and tool restrictions. Define them in `.claude/agents/<name>.md`. Use them for focused tasks (code review, research, audits) that benefit from isolation or parallel execution. Each agent gets a fresh context, so the main session stays clean.

**[Rules](https://code.claude.com/docs/en/memory#organize-rules-with-claude/rules/)** are instruction files in `.claude/rules/`. Rules without `paths:` frontmatter load at session start and are re-injected from disk after compaction, same as CLAUDE.md. Rules with `paths:` frontmatter load only when Claude works with matching files, and are lost on compaction until a matching file is read again. If you prefer splitting your operating instructions across multiple files rather than maintaining one large PROJECT_CONTEXT.md, rules are the mechanism for that.

---
*Part of [AI Project Architect](https://github.com/vbiroshak/ai-project-architect) — Version 4.4*
