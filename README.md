# AI Project Architect

A design pattern for sustained knowledge work with AI assistants, using only native tools.

## The problem

AI project features aren't built for ongoing work. Memory is unpredictable, project files are static uploads with cache issues, there's no reliable continuity between chats, no way to share findings across projects, and no mechanism for the AI to maintain its own working documents across conversations.

If you've noticed your AI getting less reliable as chats get longer, or found yourself re-explaining context every time you start a new conversation, you've hit the walls this system was built to solve.

## What this is

A workspace architecture that turns an AI chat application into a persistent project environment. It gives the AI a living project directory on your local drive that it reads, writes, and maintains directly. The AI manages the project through conversation. Agentic tools handle bounded mechanical tasks like file organization. All access the same filesystem, and the workspace gives them shared context.

No external tools, no code to install, no API integrations. Everything here works with features already built into your AI application.

This was developed with and currently targets **Claude Desktop** (using the Filesystem extension and Claude Desktop's Chat, Cowork, and Code modes). The architectural principles (handoff-driven orientation, context cost optimization, session logging, temporal awareness, indexed collections) are transferable to any AI assistant with filesystem access. As other AI applications gain persistent tool use, this pattern should adapt to them with minimal changes to the tool-specific implementation details.

The design is optimized for a core constraint: everything the AI reads at startup stays in context for the entire conversation and gets reprocessed every turn. A 50 KB startup across 20 turns means that content is processed roughly 20 times. Every design decision balances orientation quality against context cost.

The result: the AI picks up exactly where you left off in every new chat, maintains its own session logs and documentation, knows what time it is and how long it's been since you last worked together, and keeps startup reads around 12-23 KB (down from 30-55 KB before optimizing).

## What you get

**Continuity across chats.**<br>
Every new conversation picks up where the last one left off. No re-explaining your project, your preferences, or what you were working on.

**Context cost optimization.**<br>
Startup reads ~12-23 KB instead of 30-55 KB. Chats stay responsive longer because the AI isn't burning context on unnecessary history.

**Temporal awareness.**<br>
The AI knows what day and time it is and how long since your last session. It can reason about deadlines, weekdays, and whether you've been away for an hour or a week.

**Proactive documentation.**<br>
The AI logs decisions, reasoning, and state changes as you work, without being asked. If a chat ends unexpectedly, nothing is lost.

**Asynchronous intake.**<br>
Drop files in the project inbox between sessions. The AI notices them when you return and processes them in context.

**Accumulated knowledge.**<br>
Operational lessons, reference materials, domain rules, and behavioral corrections grow over time without ballooning context cost.

**Task delegation.**<br>
Hand off mechanical work (file organization, indexing, batch processing) to agentic tools sharing the same filesystem. Chat retains strategic oversight.

**Sub-project organization.**<br>
Multiple workstreams in one project, each with their own reference files and structure shaped by the domain.

**Portability.**<br>
The entire project lives on the filesystem, including the instructions for setting it up. Recreate it on a new account, a different device, or for someone else.

**Multi-project coordination.**<br>
Optional coordinator project with a shared knowledge base. Projects discover techniques independently and publish them for others to adopt.

**Graceful degradation.**<br>
Full features on desktop. On web or mobile, chats note what needs syncing when you're back.

## Core concepts

Four ideas shape the architecture. Understanding these makes the full document click.

**Handoff-driven orientation.** Every new chat reads a compact state snapshot (HANDOFF.txt) that tells it where every area of the project stands, what's pending, and what to read for depth. The handoff is overwritten every time the AI logs anything, so it's always current. Session logs are the archive. The handoff is the orientation. Separating these two functions is what makes startup fast and accurate.

**Context cost awareness.** Everything the AI reads at startup stays in context for the entire conversation and gets reprocessed every turn. This means every file in the startup sequence has to earn its place. The architecture keeps startup reads to 12-23 KB by loading only what the current chat needs: the workflow, the handoff, one session log for narrative continuity, an inbox listing, and a clock check. Everything else loads on demand.

**Indexed collections.** Any folder where content accumulates gets an index file at creation time. The AI reads the index to know what's available, then pulls only the file it needs. Cost stays flat regardless of how large the collection grows. This is the card catalog principle applied to every growing folder in the workspace.

**Temporal awareness.** AI assistants have no internal clock. The workspace gives them one through a persistent file whose modification timestamp becomes the current time. The AI also checks how long since the last session, giving it context about whether this is a continuation from an hour ago or a return after a week.

## The workspace structure

Every project follows the same layout:

```
[Project]/
  WORKFLOW.txt              ← entry point, read at startup
  Inbox/                    ← async interface, both directions
  Workflow Files/
    HANDOFF.txt             ← state snapshot, overwritten constantly
    REFERENCE.txt           ← on-demand: structure, procedures, sub-project pointers
    TASKS.txt               ← active items only, on-demand
    Clock/timestamp.txt     ← temporal awareness mechanism
    Lessons/
      LESSONS_INDEX.txt     ← index for accumulated knowledge
      [topic].txt
    Session Logs/
      Session_XXX.txt
  [Sub-Project A]/          ← shaped by the domain
    [SubProj]_STATUS.txt    ← orientation (current state)
    [SubProj]_REFERENCE.txt ← domain knowledge
  [Sub-Project B]/
```

**WORKFLOW.txt** is lean. Startup procedure, project description, temporal awareness, logging rules, and project-specific context. Only what earns its place in every context window.

**HANDOFF.txt** is the continuity mechanism. A compact state snapshot covering where every area of the project stands, what's pending, and reading pointers for depth. Gets overwritten every time the AI logs anything. Chats can hit context limits without warning, so nothing important waits for "end of session."

**Session logs** capture decisions, state changes, and reasoning. Not process narration. The handoff tells you where things stand; the log tells you how they got there.

**The Clock file** gives the AI temporal awareness. The AI writes to the file (establishing the current time) and reads its last-modified metadata to calculate how long since the previous session. No more confusion about whether it's been an hour or three days.

**Indexed collections** handle anything that accumulates. An index file plus individual topic files, like a card catalog. The AI reads the index to know what exists, pulls only what it needs. Cost is the index read plus the one file you need, rather than reading the entire collection to find it.

**Startup reads about 12-23 KB total:** WORKFLOW.txt, HANDOFF.txt, session log(s) identified by the handoff, an inbox listing, and a clock check.

## How to use this

### What you'll need

- **Claude Desktop app** (macOS or Windows) with the Filesystem extension enabled
- **A single dedicated directory on your local drive** where all project directories will live (e.g., `AI Projects` on your Desktop)

This is built for people who manage projects through AI chat and want persistent continuity between conversations. The full system works in the Claude Desktop app, where Chat manages the project and can delegate to Cowork and Code. Cowork runs agents on a local VM and can coordinate multiple workstreams in parallel. Code operates from the terminal with direct access to development tools. Both have capabilities Chat doesn't, and the workspace gives Chat the context to delegate effectively. It does not work on web or mobile interfaces (no filesystem access), but the workspace degrades gracefully: chats on web or mobile note what needs syncing when you're back on desktop.

### Quick start (Claude Desktop)

1. **Create a dedicated root directory** for all your project files. This is a single folder (e.g., `AI Projects` on your Desktop) where every project directory will live. Starting with an empty directory is cleanest.

2. **Enable the Filesystem extension** in the Claude Desktop app. Go to Settings, find the Filesystem extension, turn it on, and grant it access to this directory. You can add multiple directories to the extension, but the same permissions apply to all of them. Every project and chat in the desktop app can access everything you've granted. In this setup, you grant access to one root directory containing all your projects. That means every project can read every other project's files, which is by design: it enables cross-project coordination, the shared knowledge base, and delegation via inbox notes.

3. **Set tool permissions to Always Allow.** In Settings under Tool Permissions, the Filesystem tools are grouped into read-only, write/delete, and other categories. Set all three to "Always allow." The workspace involves frequent file reads and writes during normal conversation. If permissions are set to ask every time, you'll be approving dozens of tool calls per session. Always Allow lets the AI work fluidly.

4. **Give Claude the architecture document.** In a new or existing project, start a chat and give Claude the [workspace architecture document](workspace-architecture.md). Tell it about your project and ask it to build the workspace structure for you.

That's it. Claude will scaffold the directory, create the files, and provide you with the project instructions to paste into your project settings (customized with your actual file path). From then on, every new chat in that project reads the workspace and picks up where the last one left off.

The [project instructions template](project-instructions.md) is included in this repo for reference. Claude will generate the correct version for your project (with your actual file path) after reading the architecture document. You then copy and paste it into your Claude.ai project settings. Claude can't write to that area itself.

### Adapting to other AI applications

The workspace architecture document is designed to be understood by any capable AI assistant. If your AI application provides filesystem read/write access, you can give it the architecture document and ask it to build the workspace. The tool-specific details (MCP tool names, project instructions format) will need translation to your platform, but the structural design, principles, and file organization are platform-independent.

### Scaling up

The architecture works for a single project or many. Each project gets its own directory and its own project in your AI application. For multiple projects, you can optionally add a coordinator project that tracks cross-project changes and maintains a shared knowledge base (documented in the architecture document under "Knowledge Architecture").

## What's in this repo

| File | What it is |
|------|-----------|
| [workspace-architecture.md](workspace-architecture.md) | The complete workspace design. This is the core document. Give it to your AI to build your workspace. |
| [project-instructions.md](project-instructions.md) | The text you paste into Claude's project settings. Three lines, identical for every project except the file path. Adapt for other AI platforms. |
| [patterns/](patterns/) | Supporting patterns and techniques developed through use. Optional reading that adds depth as your workspace matures. |

### Patterns

These are standalone documents, each covering one technique. They're not required to get started but become valuable as you use the workspace:

- **[Temporal Awareness](patterns/temporal-awareness.md)**: How the AI determines the current time and detects gaps between sessions using a persistent Clock file and filesystem metadata. AI assistants have no idea what time it is or how long you've been away.
- **[Evolving State in Handoffs](patterns/evolving-state.md)**: Logging in-progress topics at their current state of thinking, not just as open or closed. Prevents the next session from restarting work that's already been partially decided.
- **[Sub-Project Archive Pattern](patterns/archive-pattern.md)**: How to freeze completed sub-projects while keeping them discoverable.
- **[Agentic Task Delegation](patterns/agentic-delegation.md)**: Collaborating with agentic tools that have capabilities Chat doesn't. Chat provides the strategic context, agents review plans, improve prompts, and execute.

## Design principles

A few things that shaped the architecture, learned through building it:

**Instructions must be action sequences, not conditions.** "When X happens, do Y" fails because AI assistants don't reliably check conditions before acting. "Do A to check for X. If X, then do Y" works because the check is itself an action.

**Orientation and archive are separate functions.** HANDOFF.txt orients. Session logs archive. Loading all session logs at startup conflates the two. The handoff points to specific logs to load, so startup reads scale to the project rather than growing with history.

**Directory structure is UX.** When you open a project folder, it should be transparent and easy to navigate. Sub-project folders show what the project does. System files are organized out of the way.

**Start new chats often.** With this system you lose nothing by starting fresh. Every new chat reads the handoff, checks the inbox, and continues where the last one left off. Chats stay responsive and the context window stays wide.

**Project memory masks bad instructions.** AI assistants compensate for inadequate instructions using memory from prior chats. Always test structural changes in fresh chats and sometimes fresh projects.

## Contributing

This is a reference implementation. Adapt it to your needs rather than submitting pull requests. If something doesn't work the way you expected, or if you've built something interesting on top of it, open an issue. Hearing what breaks is as useful as hearing what works.

## Background

This system was built by a non-developer through iterative design and daily use across multiple AI projects.

## Status

Active development. The architecture is tested across multiple projects spanning different domains, but it is still being built. Not everything works reliably yet. It continues to be refined through daily use.

## License

[MIT](LICENSE)
