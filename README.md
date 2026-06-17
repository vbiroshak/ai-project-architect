# AI Project Architect

A design pattern that moves AI project knowledge to a living filesystem the AI reads, writes, and maintains directly. Your projects live on your own drive, fully portable and backed up, with built-in session continuity, temporal awareness, task tracking, and multi-project coordination.

## The problem

If you've used AI project features, you've seen what AI is capable of in a single conversation and felt the limitations across many. Memory that doesn't carry over reliably, no awareness of time, no ability to build and organize reference materials, no task tracking across sessions. This system was built to overcome those limitations using only native tools.

## What this is

The AI gets a living directory on your local drive that it reads, writes, and maintains directly. No external tools, no code to install, no API integrations. Works with Claude Desktop (Chat) or Claude Code.

The AI picks up where you left off in every new chat. It logs its own work proactively, knows what time it is and how long you've been away, and keeps startup reads lean so conversations stay responsive.

Drop any files or folders in a project inbox as you work. The project checks its own inbox at startup, notices what's new, relates items to ongoing work when it can, and won't let them fall through the cracks. The AI organizes what it learns into files it maintains and indexes, reading only what's relevant to the current work instead of loading everything into context. The whole project lives on the filesystem, so it's portable to a new device or account.

The system works for a single project or many. Multiple projects can share a knowledge base and coordinate through a dedicated coordinator project.

Built with **Claude Desktop** and **Claude Code**. The architecture documents, templates, and patterns are platform-agnostic and should work with any AI assistant that has filesystem access. See [claude-code-setup.md](claude-code-setup.md) for the Code-specific setup guide. Web and mobile work without filesystem access. The AI continues from conversational context, then writes logs and updates files when you're back on desktop.

## Getting started

You need a directory on your local drive and an AI assistant with filesystem access. The two tested environments:

**Claude Desktop (Chat):** Install the Claude Desktop app (macOS or Windows), enable the Filesystem extension, and grant it access to your project directory. Set tool permissions to Always Allow for the smoothest experience — the AI reads and writes files frequently, and if the extension is only scoped to your project directory, it can only touch files it manages. Then give Claude the architecture document and templates from this repo, describe your project, and ask it to build the workspace. It will scaffold the directory, create the files, and give you the project instructions to paste into your project settings.

**Claude Code:** Open Claude Code in your project directory, give it the architecture document and templates, and ask it to build the workspace. See [claude-code-setup.md](claude-code-setup.md) for the full setup guide, including hooks, permissions, and migration from Chat.

**Other tools:** [Download the latest version](https://github.com/vbiroshak/ai-project-architect/tags) or provide the files directly to any AI assistant with filesystem access. The architecture is platform-agnostic. (Some tools fetch cached content from the web, so providing files directly ensures you get the newest version.)

Every new session reads the workspace and continues where the last one left off.


## What's in this repo

| File | What it is |
|------|-----------|
| [workspace-architecture.md](workspace-architecture.md) | The complete architecture. Principles, structure, file roles, startup sequence, knowledge organization. Start here. |
| [claude-code-setup.md](claude-code-setup.md) | Setting up in Claude Code: fresh project setup, migrating from Chat, hooks, permissions, and Code-specific features. |
| [templates/](templates/) | Deployable text for every file in the system. Workflow sections go into WORKFLOW.txt verbatim. Mandated file templates show the prescribed structure for handoffs, references, status files, indexes, and more. Includes [Claude Code templates](templates/claude-code/) (hooks, settings, scripts). |
| [patterns/](patterns/) | Supporting patterns developed through use: [temporal awareness](patterns/temporal-awareness.md), [evolving state](patterns/evolving-state.md), [archiving](patterns/archive-pattern.md), [agentic delegation](patterns/agentic-delegation.md). |
| [tool-guides/](tool-guides/) | Operational reference for using specific tools well. Adopted per-project as needed, loaded on demand. |

## Contributing

This is a project I maintain for my own work. Hopefully you find it useful and can adapt it to yours. If you run into problems or have suggestions, open an issue on the repo.

## Background

Built by a non-developer through iterative design and daily use.

## Status

Active development. Tested across multiple projects in different domains, continually being refined and updated.

## License

[MIT](LICENSE)

---
*Part of [AI Project Architect](https://github.com/vbiroshak/ai-project-architect) — Version 4.3*
