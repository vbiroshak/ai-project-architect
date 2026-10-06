# AI Project Architect

A workspace architecture that gives AI assistants persistent, structured project knowledge on your local filesystem.

[Download the repo.](https://github.com/vbiroshak/ai-project-architect/tags)

## What "project" means here

In this repo, a project is a continuing body of work carried across a numbered series of sessions, with its instructions, working record, and files kept in a folder on your computer that the AI reads and maintains.

Anthropic uses the same word for other things: a project in Claude Chat, which stores chats, instructions, files, and memory in your Claude account, and Projects in Claude Code, which coordinates sessions running in the cloud. Where this repo means one of those, it says so by name. The setup guide explains how a project in this repo's sense is set up in Claude Code.

## How to set it up

> [!IMPORTANT]
> **This system runs in Claude Code.** Claude Code is not only a command-line tool. It also runs in the Claude desktop app, in a conversation window much like Chat. If your projects are in Chat, migrate them.

Claude does the setup. You tell it what you want and answer its questions.

- **A new project.** Put the repo in the folder that will hold the project, start a Claude Code session in that folder, and tell Claude to install it. Claude follows the [setup guide](claude-code-setup.md); the guide's last step tells you how to confirm the project works.
- **A project you are moving from Chat.** Start at [Starting a Migration](chat-to-code-migration.md#starting-a-migration) in the migration guide. It covers projects built with this system and Chat projects that were not.

Read [workspace-architecture.md](workspace-architecture.md) for a full explanation of how the system works. The setup runs on macOS and Windows; Windows specifics (hook registration, path forms) are covered in the setup guide.

### Why Code

This system needs the AI to read and write a folder on your computer.

- **In Claude Code, that is how a session works.** A local session runs on your computer, works directly in the project's folder, and is saved there.
- **You do not need the command line.** The Claude desktop app has a Code tab beside Chat. You type in a message box and Claude replies, as in Chat. See Anthropic's [desktop quickstart](https://code.claude.com/docs/en/desktop-quickstart).
- **Chat reaches the folder indirectly.** A Chat session depends on the desktop app and an extension to reach the folder. Anthropic decides how that connection works, and it changes with app updates. A change there can stop a Chat project from reading its own files.

The Chat setup guide and templates from earlier versions are in [release v4.8](https://github.com/vbiroshak/ai-project-architect/tree/v4.8).

**Other tools:** [download the repo](https://github.com/vbiroshak/ai-project-architect/tags) and provide the files to any AI. The architecture design is broadly platform-agnostic and can be adapted to any AI with filesystem access.

## What's in this repo

| File | What it is |
|------|-----------|
| [workspace-architecture.md](workspace-architecture.md) | The architecture: principles, patterns, file roles, knowledge organization. |
| [claude-code-setup.md](claude-code-setup.md) | Setting up in Claude Code: project structure, fresh setup, hooks, permissions, Code-specific features. |
| [chat-to-code-migration.md](chat-to-code-migration.md) | Migrating a Chat project to Code: what to carry over, transcript processing, structural transformation, verification. |
| [templates/](templates/) | Deployable text for every file in the system. [Code templates](templates/claude-code/) for CLAUDE.md, PROJECT_CONTEXT.md, PROJECT_INDEX.txt, hooks, settings, and scripts. [Mandated file templates](templates/mandated-files/) for HANDOFF, status files, indexes, and the task queue. |
| [patterns/](patterns/) | Supporting patterns: [temporal awareness](patterns/temporal-awareness.md), [evolving state](patterns/evolving-state.md), [archiving](patterns/archive-pattern.md), [agentic delegation](patterns/agentic-delegation.md). |
| [tool-guides/](tool-guides/) | Operational reference for using specific tools well. Adopted per-project, loaded on demand. |

## How it works

Most built-in AI project features don't carry knowledge well across sessions. Memory is unreliable, there's no awareness of time, no way to build and maintain reference materials, no task tracking. This architecture solves that by giving the AI a directory on your local drive that it reads, writes, and maintains directly — using only the native tools your AI application already has.

The AI picks up where you left off in every new session. It logs its own work, knows what time it is and how long you've been away, and lets you make your startup reads as lean or as rich as your work demands. Drop files in an inbox and the project notices them, relates items to ongoing work, and won't let them fall through the cracks. The AI organizes what it learns into files it maintains and indexes, reading, creating, and editing relevant project files on demand. The whole project lives on your filesystem, not on the cloud, making it portable to any device, account, or service.

Works for a single project or many. Multiple projects can share a common knowledge base folder and you can manage them all through a dedicated coordinator project.

## Setting up a new project

At minimum, walk through these steps with the user before building anything:

1. Starting point — a new project, an existing folder to build the project around, or a Chat project being migrated?
2. Location — install in this directory or elsewhere?
3. Name — what to call the project
4. Description — what the project does
5. Optional components — which to include (task queue, lessons, tool guides, etc.)
6. Software engineering instructions — keep or remove from the output style
7. Cleanup — keep or remove the downloaded repo files after setup

## Contributing

This is a project I maintain for my own work. Hopefully you find it useful and can adapt it to yours. If you run into problems or have suggestions, open an issue on the repo.

## Background

Built by a non-developer through iterative design and daily use.

## Status

Active development. Tested across multiple projects in different domains, continually being refined and updated.

## License

[MIT](LICENSE)

---
*Part of [AI Project Architect](https://github.com/vbiroshak/ai-project-architect) — Version 4.10*
