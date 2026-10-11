# Setting Up in Claude Code

This guide is written for the AI that builds the project; the person who owns the project reads the [README](README.md). It covers building and running a project with this workspace architecture in Claude Code, in the desktop app or in a terminal. The principles and patterns behind the system are in [workspace-architecture.md](workspace-architecture.md). To migrate an existing Chat project, follow [chat-to-code-migration.md](chat-to-code-migration.md).

---

## What Code Provides

Claude Code gives the AI native filesystem access and several features this architecture uses:

- **[CLAUDE.md](https://code.claude.com/docs/en/memory)** — a markdown file at the project root that loads automatically into every session. Carries the startup procedure.
- **[Event hooks](https://code.claude.com/docs/en/hooks)** — scripts that run on specific events (session start, each user message, and others). Used for temporal awareness and transcript archiving.
- **[Settings](https://code.claude.com/docs/en/settings)** — project-level permissions controlling which files can be read or written, which shell commands are allowed without prompting, and which paths are denied.
- **[Output styles](https://code.claude.com/docs/en/output-styles)** — per-project behavioral profiles that modify the system prompt. Set role, tone, and output format without repeating instructions every turn.
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
    settings.json             permissions, hooks
    settings.local.json       output style, personal overrides
    hooks/                    event scripts: the time on every turn, the transcript archive
    output-styles/            behavioral profiles (optional)
    skills/                   reusable prompts (optional; handoff/ closes a session)
    agents/                   specialized subagents (optional)
    rules/                    path-scoped instructions (optional)
  Inbox/
  Project/                    project infrastructure
    PROJECT_CONTEXT.md        governing document
    HANDOFF.txt
    PROJECT_INDEX.txt
    TASKS.txt                 (optional)
    CHANGELOG.txt             (optional)
    Lessons/                  (optional)
    Session Logs/
      Session_XXXX.txt        4-digit, one per session
    Sessions/                 archived transcripts (step 4)
  [Sub-Project A]/
  Archive/
```

The core that every Code project needs: CLAUDE.md, PROJECT_CONTEXT.md (or equivalent governing document), HANDOFF.txt, PROJECT_INDEX.txt, Inbox/, Session Logs/, Sessions/ with the hooks that fill it (step 4), at least one sub-project directory. Everything else is optional and depends on what serves the work.

**What's optional and why:**

- **TASKS.txt** — a file-based queue of open work, read at startup, for projects whose work carries across sessions in more items than the handoff should hold. A small project may not need one. If used: active items only, no DONE section. When a task completes, remove it from the queue and note completion in the session log.
- **Lessons/** — operational knowledge that applies across the project's areas, as an indexed collection. Useful once a project has accumulated some; see [Knowledge Architecture](workspace-architecture.md#knowledge-architecture).
- **CHANGELOG.txt** — useful for projects with infrastructure changes to track; optional for simpler projects.

---

## Fresh Setup

To build a new project in Code using this architecture:

**Platform note:** the steps below run as written on macOS and Linux. On Windows, two things come first. Install [Git for Windows](https://git-scm.com/downloads/win): Claude Code runs without it, but the hook commands in step 5 are written for the Git Bash shell it provides (without it, register the PowerShell form shown there). The hooks in step 4 also require Python (verify with `python --version` or `py --version`; if neither responds, install from [python.org](https://www.python.org/downloads/) with "Add python.exe to PATH" checked). After installing either one, the desktop app must be restarted, or a new terminal opened for the CLI, before the change takes effect. Windows command and path forms appear in step 5. Determine the platform before starting and apply the Windows notes as you reach them.

### 1. Create the project directory

Create the project directory with this structure:
- CLAUDE.md at the root (step 2)
- Project/ containing HANDOFF.txt, PROJECT_INDEX.txt, Session Logs/, and Sessions/
- Inbox/ for asynchronous items between the user and the AI
- At least one sub-project folder for the project's domain work

Create Project/Sessions/ even though it starts empty: the archive hook (step 4) archives into it when it exists; without it, the hook uses a root-level Sessions/ if there is one and otherwise creates a `recall/sessions/` directory at the project root.

The following components are optional. Explain each one to the user in plain terms and ask whether they want it. For additional directories, ask: are there any other folders on your computer you want this project to be able to read and write without asking? The user names the folders; you find the paths.

| Component | What it does | Where it goes |
|-----------|-------------|---------------|
| Task queue | File-based cross-session task tracking | Project/TASKS.txt + section in PROJECT_CONTEXT.md + `@` import in CLAUDE.md |
| Additional directories | File access to folders outside the project | `permissions.additionalDirectories` in settings.json |
| Shared knowledge base | Cross-project shared resources | Section in PROJECT_CONTEXT.md |
| Output style | Role, tone, and behavioral profile | .claude/output-styles/ + `outputStyle` in settings.local.json (step 6) |
| Session close skill | A `/handoff` command that runs the SESSION CLOSE procedure in PROJECT_CONTEXT.md | Copy [templates/claude-code/skills/handoff/](templates/claude-code/skills/handoff/) to .claude/skills/handoff/ (the folder name is the command name; rename it if the user prefers another) |
| Lessons directory | Structured operational knowledge | Project/Lessons/ with index |
| Changelog | Record of structural/infrastructure changes | Project/CHANGELOG.txt, from the [changelog template](templates/mandated-files/changelog.md) |

See the directory tree in [The Code Project Structure](#the-code-project-structure) above for the full layout. The [Code templates](templates/claude-code/) provide starting content for [CLAUDE.md](templates/claude-code/CLAUDE-template.md), [PROJECT_CONTEXT.md](templates/claude-code/PROJECT-CONTEXT-template.md), [PROJECT_INDEX.txt](templates/claude-code/PROJECT-INDEX-template.md), and [settings.json](templates/claude-code/settings-template.json). For HANDOFF.txt format, see the [handoff template](templates/mandated-files/handoff.md).

### 2. Create CLAUDE.md

[CLAUDE.md](https://code.claude.com/docs/en/memory) loads automatically at the start of every session. It carries the startup procedure: the sequence of files to read for orientation. Create it from the [CLAUDE.md template](templates/claude-code/CLAUDE-template.md), which holds the text and explains the `@` imports and the compaction re-read line.

Add project-specific startup steps (sub-project activation, task queue reads, domain-specific loads) as additional numbered steps. Keep CLAUDE.md under 200 lines — instructions beyond that length reduce adherence.

### 3. Create PROJECT_CONTEXT.md

PROJECT_CONTEXT.md is the governing document: the substantive operating knowledge every session needs from the first message. The startup procedure lives in CLAUDE.md; everything else lives here.

The [PROJECT_CONTEXT template](templates/claude-code/PROJECT-CONTEXT-template.md) provides the full deployable text with all standard sections: What This Project Does, Sub-Project Activation, Session Logs, Handoff, Session Close, Inbox, Temporal Awareness, and Project Context, plus optional sections for Task Queue and Shared Knowledge Base. Deploy the text as written: fill in the brackets (the project name, the sub-projects, the domain examples, the session-naming form from README question 9) and change nothing else.

### 4. Set up hooks

Create `.claude/hooks/` in the project directory and register the hooks in `.claude/settings.json`. Three scripts provide the core session infrastructure:

**Temporal awareness** (UserPromptSubmit): Injects the current local time into every turn, before the AI processes each message.

**Transcript archiving** (SessionStart): Every session's transcript belongs to the project's record (see [Portable by Design](workspace-architecture.md#portable-by-design)). At the start of each session the hook copies every finished transcript of the project from Claude Code's store into Project/Sessions/, named with the session number, and renders each one to a readable file. The session number is the user's: the hook reads the two forms a user can choose at setup (README question 9), a `/rename` title of the project name and a number ("MyProject 42"), checked first, then a "This is MyProject 42" opening message; a free-form `/rename` title becomes the filename as-is, and a session with neither is archived under its UUID. Number-named sessions are formatted as `MyProject_0042.jsonl` (zero-padded); the name may contain spaces and accented letters. A `PROJECT_NAME` constant at the top of the script normalizes casing and prevents false matches. The hook archives into Project/Sessions/ when it exists (create it in step 1), then a root-level Sessions/, and otherwise creates `recall/sessions/`. It touches only transcripts in Claude Code's format; archives another platform's hook has placed in the same folder are left alone, and a name they already hold is reported as a conflict.

**Transcript renderer** (companion script): Renders each archived transcript as a readable Markdown file (collapsed view: messages in full, tool calls as one-line summaries). The archiver imports it when the two sit in the same folder.

A hook passes context to the session by printing a JSON object to stdout with an `additionalContext` field inside `hookSpecificOutput`; the text appears as a system reminder attached to the user's message. The temporal-awareness hook injects the local time this way.

All three scripts go into `.claude/hooks/` from [templates/claude-code/](templates/claude-code/). Copy the files exactly (with `cp`, for example), not retyped or regenerated: a rewritten copy can silently diverge from the tested source. Set the `PROJECT_NAME` constant at the top of the archiver to the project's name.

A hook that produces data the session will query (a regenerated index, extracted text) runs blocking at SessionStart, not async: the cost is paid once per session, and an async hook lets the session query stale data.

### 5. Configure permissions

`.claude/settings.json` controls what the AI can access and which hooks run. See [templates/claude-code/settings-template.json](templates/claude-code/settings-template.json) for a deployable template.

```json
{
  "permissions": {
    "additionalDirectories": ["/path/to/external/resources"],
    "allow": [
      "Read(//path/to/your/project/**)",
      "Edit(//path/to/your/project/**)",
      "Read(//path/to/external/resources/**)"
    ],
    "deny": [
      "Edit(//path/to/read-only-sources/**)"
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

- **`additionalDirectories`** — inside `permissions`. Adds folders outside the project root as working directories, such as sibling projects or shared resource directories. Files there become readable without prompts, and edits there follow the current permission mode. To keep an added folder read-only in every mode, add an `Edit` deny rule for its path.
- **File rules use `Read` and `Edit`.** An `Edit` rule covers every tool that changes files. A path rule written for another tool name, such as `Write`, is accepted but never checked.
- **Absolute paths in rules use `//`** (double slash). A single leading slash is project-relative in Code. Do not "fix" `//` to `/`.
- **Hook commands** use `${CLAUDE_PROJECT_DIR:-$PWD}` rather than bare relative paths, so they resolve correctly regardless of where Code is launched.

**Windows:**

- With Git for Windows installed, hook commands run through Git Bash, so the commands above work with one substitution: `python` in place of `python3`.
- Without Git for Windows, hook commands run through PowerShell, where `${CLAUDE_PROJECT_DIR:-$PWD}` does not expand. Register the PowerShell form instead:

```json
"hooks": {
  "SessionStart": [
    { "hooks": [{ "type": "command", "shell": "powershell", "command": "python \"$env:CLAUDE_PROJECT_DIR\\.claude\\hooks\\archive-transcripts.py\"" }] }
  ],
  "UserPromptSubmit": [
    { "hooks": [{ "type": "command", "shell": "powershell", "command": "python \"$env:CLAUDE_PROJECT_DIR\\.claude\\hooks\\temporal-awareness.py\"" }] }
  ]
}
```

- Absolute permission rules use POSIX-normalized drive syntax: paths are normalized before matching (`C:\Users\alice` becomes `/c/Users/alice`), so write `//c/Users/Name/project/**`.
- Other absolute-path values (`additionalDirectories`) take standard Windows paths with JSON-escaped backslashes: `C:\\Users\\Name\\...`.
- Confirm which Python command responds (`python --version` or `py --version`) before writing settings.json, and confirm the hooks fire in step 7 rather than assuming registration worked. See the [hooks documentation](https://code.claude.com/docs/en/hooks) for shell selection behavior.

**What the template grants.** The template's rules pre-approve reading and editing inside the project directory and reading the external resources listed, and the file registers the two hooks. Nothing else is pre-approved.

**What decides the rest.** Every other action follows the session's [permission mode](https://code.claude.com/docs/en/permission-modes), which sets how much Claude does without asking, from asking before each edit and command to working without prompts. Rules in settings.json sit on top of the mode: allow rules pre-approve specific actions, and deny rules block them in every mode.

**What the user can adjust.** These are the user's to set to the way they want to work:

- The permission mode for a session, and the mode new sessions start in (`permissions.defaultMode`).
- Allow rules, to pre-approve commands or paths the user uses often.
- Ask and deny rules, to require a prompt for specific actions or to block them.
- Additional directories, to extend file access beyond the project.

Explain these to the user at setup; do not set them without direction.

See the [permissions documentation](https://code.claude.com/docs/en/permissions) for the rule syntax and the [permission modes documentation](https://code.claude.com/docs/en/permission-modes) for what each mode does.

**Workspace trust:** Claude Code does not apply project-level settings until the workspace is trusted. The desktop app prompts on first open; the user accepts. The CLI may not prompt; then it reports that project settings were ignored because the workspace is not trusted. To have project settings apply from the first CLI session, add the project path to `~/.claude.json` (on Windows, `%USERPROFILE%\.claude.json`) before launching:

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

Ask the user two things: whether to keep Code's default software engineering instructions (see [creating a custom output style](https://code.claude.com/docs/en/output-styles#create-a-custom-output-style)), and what behavioral rules, if any, to put in the body. Create the file with only the frontmatter until the user provides direction. What belongs where: the output style sets role, tone, and response format; what the AI should know about the project goes in PROJECT_CONTEXT.md; preferences that apply across projects go in the global `~/.claude/CLAUDE.md`. A style is an instruction, not a guarantee; anything that must happen every time belongs in a [hook](https://code.claude.com/docs/en/hooks-guide) or a permission rule.

Select the style in `.claude/settings.local.json`:

```json
{
  "outputStyle": "ProjectName"
}
```

Creating `settings.local.json` with the output style at setup makes the style active from the first session. The file holds the user's personal settings for this project, including approvals saved during work. If the project is a git repository, add the file to `.gitignore`; Claude Code does that only for a file it creates itself.

**User preferences** go in the global `~/.claude/CLAUDE.md`, which loads into every session across all projects. Interaction style, formatting rules, behavioral constraints that apply everywhere. See [CLAUDE.md scoping](https://code.claude.com/docs/en/memory#choose-where-to-put-claude-md-files) for the full hierarchy.

### 7. Verify

A project runs as local sessions in its folder: the user starts each session in the project's folder on their own machine, by running `claude` inside the folder in the CLI or by choosing a Local session with the folder selected in the desktop app. The **Projects** feature in Claude Code, which coordinates sessions running in the cloud, is a different thing and is not used here. How to start a session: Anthropic's [CLI quickstart](https://code.claude.com/docs/en/quickstart) or [desktop quickstart](https://code.claude.com/docs/en/desktop-quickstart).

Write the following verification checklist into the new project's HANDOFF.txt under ACTIVE WORK, for the project's next session to check:

- Startup procedure reads all orientation files (PROJECT_CONTEXT, PROJECT_INDEX, HANDOFF)
- Greeting includes project state summary (where work left off, what's pending)
- Temporal awareness hook fires (confirm the local time injection is present in the system reminder)
- Session log can be written to Project/Session Logs/
- Inbox listing runs without error
- The session-naming form the user chose is in PROJECT_CONTEXT (SESSION NUMBER), and the user was told the next session's number
- Archive hook copied the earlier sessions' transcripts from this folder into Project/Sessions/ with the correct names
- Readable .md companion files were generated alongside the .jsonl files

A project's sessions are the ones run in its own folder (see [Concise Logging](workspace-architecture.md#concise-logging)). When the setup runs in the project's folder, it is the project's Session 1, and Session 2 checks every item: its start archives Session 1. When the setup runs from a session outside the project's folder, as when a coordinator project builds a project in a different folder, the setup is not one of the project's sessions: the new project's first session checks every item except the two archive items, which have no earlier session to find yet, and the session after it checks those.

If either hook fails to fire, re-check the hook command against the Windows notes in step 5 — the wrong Python command name or the wrong shell form are the likely causes on Windows.

The session that checks the archive is the real test: its startup continues from the previous session's log and handoff, and that session's transcript is in Project/Sessions/, which proves the full cycle works.

### Adopting for existing projects

For an existing folder of project files without this structure (an unstructured Code project, or a Chat project that kept its files in a local folder), build the structure around them:

1. Create Project/ with HANDOFF.txt, PROJECT_INDEX.txt, Session Logs/, and Sessions/
2. Create CLAUDE.md with the startup procedure
3. Create PROJECT_CONTEXT.md with the standard sections
4. Move domain work into at least one sub-project directory
5. Create Inbox/ at the project root
6. Set up .claude/ configuration (settings.json, hooks)
7. Add freshness lines to all new files. See [Freshness Tracking](workspace-architecture.md#freshness-tracking).

---

## Code-Specific Features

### Auto memory

Claude Code has a memory feature of its own, [auto memory](https://code.claude.com/docs/en/memory#auto-memory), where Claude saves notes for itself across sessions. This system works with it on or off: the project files are the record, and where a memory note and a project file disagree, the project file governs. To rely on the files alone, set `"autoMemoryEnabled": false` in settings.json.

### Managing accumulated permissions

`settings.local.json` accumulates "always allow" grants as the user approves actions during work, some broader than the user understood (MCP tool allows are tool-wide, not per action; Bash allows match by prefix). Review it periodically and clear grants that are too broad. `settings.json` is the deliberate policy; `settings.local.json` is the accumulated grants.

### On-demand reads and trigger maps

A project with substantial reference material (style guides, process documents, reference files) wastes context by loading it all at startup. Code's larger context window makes loading more tempting; the principle holds: read what you need when you need it.

A trigger map in PROJECT_CONTEXT.md names the files, the cues that call for them, and what they guard against; the AI loads the relevant files when it recognizes the work type, before proceeding. Startup stays lean and domain knowledge loads before the work that needs it.

### Skills, subagents, and rules

These are optional extensions that develop as the project matures.

**[Skills](https://code.claude.com/docs/en/skills)** are reusable prompts for repeating workflows. Each skill lives in `.claude/skills/<name>/SKILL.md` and can bundle supporting files (checklists, templates, reference docs). Invoke with `/name` or let Claude invoke automatically when it recognizes a matching task. Use `disable-model-invocation: true` in the frontmatter for workflows the user triggers by hand. Skills load only when invoked, keeping startup lean. Skills and agents defined at `~/.claude/` (user level) are available across all projects.

**[Subagents](https://code.claude.com/docs/en/sub-agents)** are specialized agents with their own context window, system prompt, and tool restrictions. Define them in `.claude/agents/<name>.md`. Use them for focused tasks (code review, research, audits) that benefit from isolation or parallel execution. Each agent gets a fresh context, so the main session stays clean.

**[Rules](https://code.claude.com/docs/en/memory#organize-rules-with-claude/rules/)** are instruction files in `.claude/rules/`. Rules without `paths:` frontmatter load at session start and are re-injected from disk after compaction, same as CLAUDE.md. Rules with `paths:` frontmatter load only when Claude works with matching files, and are lost on compaction until a matching file is read again. For a user who prefers operating instructions split across several files rather than one large PROJECT_CONTEXT.md, rules are the mechanism.

---
*Part of [AI Project Architect](https://github.com/vbiroshak/ai-project-architect) — Version 4.11*
