# AI Project Architect

A workspace architecture for sustained knowledge work with AI assistants.

## The problem

AI project features aren't built for ongoing work. Memory is unpredictable, project files are static uploads, there's no reliable continuity between chats, and no mechanism for the AI to maintain its own documentation across conversations.

If you've found yourself re-explaining context every new conversation, you've hit the wall this system was built to solve.

## What this is

A design pattern that turns an AI chat into a persistent project environment. The AI gets a living directory on your local drive that it reads, writes, and maintains directly. No external tools, no code to install, no API integrations. Everything works with features already built into your AI application.

The AI picks up where you left off in every new chat. It logs its own work proactively, knows what time it is and how long you've been away, and keeps startup reads lean so conversations stay responsive. You can drop files in a project inbox between sessions and they'll be waiting when you return. Knowledge accumulates over time without ballooning context cost. The whole project lives on the filesystem, so it's portable to a new device or account.

The system works for a single project or many. Multiple projects can share a knowledge base and coordinate through a dedicated coordinator project, all documented in the architecture.

Built with and currently targeting **Claude Desktop** (Filesystem extension, Chat, Cowork, and Code). The principles transfer to any AI assistant with filesystem access. Web and mobile work in a limited mode, with the AI noting what needs syncing when you're back on desktop.

## Getting started

You need the **Claude Desktop app** (macOS or Windows) with the Filesystem extension enabled, and a directory on your local drive for your project files.

1. **Create a root directory** for your projects (e.g., `AI Projects` on your Desktop).

2. **Enable the Filesystem extension** in Claude Desktop settings and grant it access to this directory. Every project under this directory will be accessible, which is by design: it enables cross-project coordination and delegation.

3. **Set tool permissions to Always Allow.** The workspace involves frequent file reads and writes during normal conversation. Approving each one individually isn't practical.

4. **Give Claude the architecture document and templates.** Start a chat, provide [workspace-architecture.md](workspace-architecture.md) and the [templates](templates/) directory. Describe your project and ask Claude to build the workspace. It will scaffold the directory, create the files, and give you the project instructions to paste into your project settings.

That's it. Every new chat in that project reads the workspace and continues where the last one left off.

**Caching warning:** AI assistants fetching web pages may receive cached content that's days or weeks old. Verify you're getting the current version before building from this repo.

For other AI platforms with filesystem access, the architecture document is designed to be platform-independent. Tool-specific details will need translation, but the structure and principles apply broadly.

## What's in this repo

| File | What it is |
|------|-----------|
| [workspace-architecture.md](workspace-architecture.md) | The complete architecture. Principles, structure, file roles, startup sequence, knowledge organization. Start here. |
| [templates/](templates/) | Deployable text for every file in the system. Workflow sections go into WORKFLOW.txt verbatim. Mandated file templates show the prescribed structure for handoffs, references, status files, indexes, and more. |
| [patterns/](patterns/) | Supporting patterns developed through use: [temporal awareness](patterns/temporal-awareness.md), [evolving state](patterns/evolving-state.md), [archiving](patterns/archive-pattern.md), [agentic delegation](patterns/agentic-delegation.md). |

## Contributing

This is a reference implementation. Adapt it to your needs rather than submitting pull requests. If something breaks or you've built something interesting on top of it, open an issue.

## Background

Built by a non-developer through iterative design and daily use across multiple AI projects.

## Status

Active development. Tested across multiple projects in different domains, still being refined.

## License

[MIT](LICENSE)

---
*Part of [AI Project Architect](https://github.com/vbiroshak/ai-project-architect) — Version 4.1*
