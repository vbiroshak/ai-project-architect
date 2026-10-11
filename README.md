# AI Project Architect

A workspace architecture that gives an AI assistant persistent, structured project knowledge in a folder on your computer.

**Quick start**

1. [Download the repo](https://github.com/vbiroshak/ai-project-architect/tags) and put it in the folder that will hold the project.
2. Give it to your AI and ask it to build the project.
3. Answer its questions. [Set it up](#set-it-up) below has the detail.

## What it does

The project lives in a folder you own. Its instructions, its record, its files, and the AI's notes are plain text there, readable by any AI that can work in that folder and by you with a text editor. Nothing the project depends on lives inside one application, so you can move the project to another device, account, service, or AI, and the next session reads the folder and continues.

In every new session the AI picks up where you left off. It logs its own work, knows the time and how long you have been away, and reads at startup as much as the work needs. Drop files in the inbox and the AI notices them, relates them to ongoing work, and files them in the project as needed. What the AI learns goes into files it keeps and indexes. When you are done, say so, or type `/handoff`, and the AI closes the session so the next one can continue.

Works for a single project or many. Several projects can share a knowledge base folder, and a coordinator project can manage them all.

## What this system requires

An AI that can open a folder on your computer, read the instructions in it, write to it, and follow its instructions and documentation in that session and in every session after it. The project also keeps a copy of every session's transcript in its folder, taken at the start of the next session, so the application the AI runs in must keep each session's transcript on disk.

This system was built with Claude and has been tested with OpenAI Codex. It should adapt to any AI that works with folder-based projects in this way. The architecture document applies to any platform; the setup guide, the templates, and the migration guide are written for Claude Code; the [adaptation guide](platform-adaptation.md) covers running on another AI.

## Set it up

> [!IMPORTANT]
> **Built in Claude Code and tested there; the setup below is written for it.** Claude Code runs in the Claude desktop app as well as in the terminal. If your projects are in Chat, migrate them.

The AI does the setup. You tell it what you want and answer its questions.

- **A new project.** Put the repo in the folder that will hold the project, start a Claude Code session in that folder, and tell Claude to install it. Claude follows the [setup guide](claude-code-setup.md) and leaves a checklist in the project's handoff; your next session in that folder runs the checks and confirms the project works.
- **A project you are moving from Chat.** Put the repo in a folder, start a Claude Code session in that folder, and tell Claude you are moving a Chat project and where its files are. The folder you start the Code session in can be the project's own, but another folder is better: the migration is then not one of the project's sessions, and the project's next Code session is the next number in its sequence and continues where Chat left off. Claude follows the [migration guide](chat-to-code-migration.md), which covers projects built with this system and Chat projects that were not, and will ask you for a data export of your Claude account. A [coordinator project](workspace-architecture.md#the-coordinator-project) can migrate all of your Chat projects, set up new ones, and manage the project architecture going forward.
- **A project on another AI.** Put the repo in the folder, start a session there, and tell the AI to build the project adapted to itself. For an existing project, tell the AI to adapt it; it will ask whether to keep both platforms' configuration or replace the old one. The AI follows the [adaptation guide](platform-adaptation.md). A Chat project goes to Claude Code first, by the bullet above, and is adapted from there, because the migration guide is written for Claude Code.

The setup runs on macOS and Windows. Windows specifics (hook registration, path forms) are in the setup guide.

## Why Code, not Chat

- **A Code session works in the folder.** In Claude Code a local session runs on your computer, works directly in the project's folder, and saves data there.
- **Code runs in the desktop app or the terminal.** In the app, the Code tab sits beside Chat: you type in a message box and Claude replies. See Anthropic's [desktop quickstart](https://code.claude.com/docs/en/desktop-quickstart).
- **Chat reaches a folder only through the desktop app and an extension.** Anthropic changes that connection with app updates, and a change there can stop a Chat project from reading its own files.
- **Chat cannot build a Code project.** Claude in Chat does not have Code's tools and does not know how a Code session works, so it cannot build one even with this repo in front of it. Setup and migration run in Claude Code.

The Chat setup guide and templates from earlier versions are in [release v4.8](https://github.com/vbiroshak/ai-project-architect/tree/v4.8).

## What "project" means here

A project here is a working area: a folder on your computer, and a numbered series of sessions in it, each continuing from the last. It can be a topic, a domain, a body of work, or a project that holds sub-projects across several of those. Its instructions, its record, and its files are in the folder, and the AI reads and maintains them.

Anthropic uses the same word for two other things: a project in Chat, which stores chats, instructions, files, and memory in your Claude account; and Projects in Claude Code, which coordinates sessions running in the cloud. This repo names those two in full, "a Chat project" and "Projects in Claude Code"; "project" on its own means the working area described above. "Chat" in this repo is the side of the Claude app and claude.ai that is not the Code tab: the app labels it "Claude", Anthropic's documentation calls it chat, and it includes what Anthropic called Cowork before merging the two.

## What's in this repo

| File | What it is |
|------|-----------|
| [workspace-architecture.md](workspace-architecture.md) | The architecture: principles, patterns, file roles, knowledge organization. |
| [claude-code-setup.md](claude-code-setup.md) | Setting up in Claude Code: project structure, fresh setup, hooks, permissions, Code-specific features. |
| [chat-to-code-migration.md](chat-to-code-migration.md) | Migrating a Chat project to Code: what to carry over, transcript processing, structural transformation, verification. |
| [platform-adaptation.md](platform-adaptation.md) | Running on another AI platform: what the project needs from a platform, what maps to what, the rules for the adapting AI, a worked example. |
| [templates/](templates/) | Deployable text for every file in the system. [Code templates](templates/claude-code/) for CLAUDE.md, PROJECT_CONTEXT.md, PROJECT_INDEX.txt, hooks, settings, scripts, and the session close skill. [Mandated file templates](templates/mandated-files/) for HANDOFF, status files, indexes, the task queue, and the changelog. |
| [patterns/](patterns/) | Supporting patterns: [temporal awareness](patterns/temporal-awareness.md), [evolving state](patterns/evolving-state.md), [archiving](patterns/archive-pattern.md). |

## For the AI doing the setup

Read every file in this repo before building anything. Work from the repo's files, the project's files and the user's answers; infer nothing you can read or ask. Then tell the user what will happen: you will ask a few questions, then build the folders and files the project needs. Ask the questions and wait for the answers before writing anything. Settle these with the user:

1. Starting point: a new project, an existing folder to build the project around, or a Chat project being migrated?
2. Location: install in this directory or elsewhere?
3. Name: what to call the project. The name comes from the user, never from the opening message of the session.
4. Description: what the project does.
5. First sub-project: what to call the folder for the work the project will do, and what it covers. The name comes from the user, not from the description.
6. Optional components: which to include (the setup guide lists them).
7. Software engineering instructions: keep or remove from the output style.
8. Cleanup: keep or remove the downloaded repo files after setup.
9. Session naming: how the user will give each session its number. The suggested form is to open every session with "This is [Project] N". The Claude Code archiver reads that form and a `/rename` title of the project name and a number; a session named any other way is archived under its title or its UUID. On another platform, build the archiver to read the form the user chooses. Write the chosen form into the governing document.

Then follow the [setup guide](claude-code-setup.md) or the [migration guide](chat-to-code-migration.md). Deploy the template text as written: fill in the brackets and change nothing else. If you are not Claude Code, follow the [adaptation guide](platform-adaptation.md) as well; it says what changes for your platform and what does not.

## About

A project I maintain for my own work, built by a non-developer through iterative design and daily use across several projects in different domains. In active development. If you find it useful and run into problems or have suggestions, open an issue on the repo.

[MIT License](LICENSE)

---
*Part of [AI Project Architect](https://github.com/vbiroshak/ai-project-architect) — Version 4.11*
