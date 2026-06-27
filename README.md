# AI Project Architect

A workspace architecture that gives AI assistants persistent, structured project knowledge on your local filesystem.

## How to set it up

Follow the guide for your platform to get started, and you can read [workspace-architecture.md](workspace-architecture.md) for a full explanation of how the system works:

**[Set up a new project in Chat](chat-setup.md)** — for Claude in Chat (Desktop app setup, mobile/web functionality) or any AI assistant with filesystem access.

**[Set up a new project in Code](claude-code-setup.md)** — for Claude Code in the Desktop app or CLI.

**[Migrate a project from Chat to Code](chat-to-code-migration.md)** — structural transformation, transcript processing, and verification.

**Other tools:** [download the repo](https://github.com/vbiroshak/ai-project-architect/tags) and provide the files to any AI assistant with filesystem access. The architecture is platform-agnostic.

## What's in this repo

| File | What it is |
|------|-----------|
| [workspace-architecture.md](workspace-architecture.md) | The architecture: principles, patterns, file roles, knowledge organization. |
| [chat-setup.md](chat-setup.md) | Setting up in Chat: project structure, startup procedure, WORKFLOW section registry, temporal awareness. |
| [claude-code-setup.md](claude-code-setup.md) | Setting up in Claude Code: project structure, fresh setup, hooks, permissions, Code-specific features. |
| [chat-to-code-migration.md](chat-to-code-migration.md) | Migrating a Chat project to Code: transcript processing, structural transformation, verification. |
| [templates/](templates/) | Deployable text for every file in the system. [Chat templates](templates/workflow-sections/) for WORKFLOW.txt sections. [Mandated file templates](templates/mandated-files/) for HANDOFF, PROJECT_INDEX, and other required files. [Code templates](templates/claude-code/) for CLAUDE.md, PROJECT_CONTEXT.md, hooks, settings, and scripts. |
| [patterns/](patterns/) | Supporting patterns: [temporal awareness](patterns/temporal-awareness.md), [evolving state](patterns/evolving-state.md), [archiving](patterns/archive-pattern.md), [agentic delegation](patterns/agentic-delegation.md). |
| [tool-guides/](tool-guides/) | Operational reference for using specific tools well. Adopted per-project, loaded on demand. |

## How it works

AI project features don't carry knowledge well across sessions. Memory is unreliable, there's no awareness of time, no way to build and maintain reference materials, no task tracking. This architecture solves that by giving the AI a living directory on your local drive that it reads, writes, and maintains directly. No external tools, no code to install, no API integrations.

The AI picks up where you left off in every new session. It logs its own work, knows what time it is and how long you've been away, and keeps startup reads lean so conversations stay responsive. Drop files in an inbox and the project notices them, relates items to ongoing work, and won't let them fall through the cracks. The AI organizes what it learns into files it maintains and indexes, reading only what's relevant instead of loading everything into context. The whole project lives on the filesystem, portable to a new device or account.

Works for a single project or many. Multiple projects can share a knowledge base and coordinate through a dedicated coordinator project.

## Contributing

This is a project I maintain for my own work. Hopefully you find it useful and can adapt it to yours. If you run into problems or have suggestions, open an issue on the repo.

## Background

Built by a non-developer through iterative design and daily use.

## Status

Active development. Tested across multiple projects in different domains, continually being refined and updated.

## License

[MIT](LICENSE)

---
*Part of [AI Project Architect](https://github.com/vbiroshak/ai-project-architect) — Version 4.4*
