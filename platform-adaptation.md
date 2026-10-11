# Running on Another Platform

This guide is written for the AI that builds or adapts the project; the person who owns the project reads the [README](README.md). It covers running a project built with this architecture on an AI platform other than Claude Code: what the project needs from the platform, what changes and what does not, and one worked example. The architecture itself is in [workspace-architecture.md](workspace-architecture.md); the Claude Code implementation is in [claude-code-setup.md](claude-code-setup.md).

---

## What the Project Needs from a Platform

Everything the project knows and does is in plain files in its folder. A platform runs the project when it provides six things:

1. **A local session in the project folder**, with read, write and shell access to it. The session runs on the user's machine and works directly in the folder.
2. **An instruction file loaded at session start.** It carries the startup procedure: the files to read for orientation, in order. Where the platform's instruction file can import other files, the orientation files load with it; where it cannot, the startup procedure tells the AI to read them, which the architecture allows.
3. **The current time on every turn.** Where the platform can run a script on each user message and add its output to the model's context, the script injects the time. Where it cannot, the clock-file method in [patterns/temporal-awareness.md](patterns/temporal-awareness.md) applies.
4. **The session record.** Every session's transcript is part of the project's record. The platform keeps transcripts in its own store, outside the folder, in its own format; the project copies each session's transcript into Project/Sessions/ at the start of the next session, named with the session number the user gave, with a readable rendering. The next start is the reliable moment, because sessions end without warning. This needs a script that runs at session start and transcripts on disk in a known place.
5. **Permissions.** Read where the user allows, write inside the project folder, a prompt for everything else, including every destructive shell command, and the user's own choice of how much runs without asking. Each platform has its own mechanism; this part is rebuilt, not ported.
6. **Nothing that lives only inside the application.** No container, cloud session or application memory holds anything the project depends on. The files are the record.

Not needed on another platform: output styles, skills and subagents as Claude Code defines them. Role and tone text goes into the instruction file. The session-close skill is two sentences that point at the governing document's SESSION CLOSE section; where the platform has reusable prompts, ship it as one; where it does not, the user says the session is ending and the section applies.

---

## Two Paths

**Build from the repo on this platform.** No project exists yet. Follow the [setup guide](claude-code-setup.md) as the specification of what to build, with the substitutions in [What Maps to What](#what-maps-to-what). The result runs on this platform only.

**Adapt an existing project built on another platform.** The project already has its files, its record and the other platform's configuration. Ask the user which result they want, and do not assume one:

- **Additive.** Both platforms' configuration stays in the folder and the project runs on either. Each platform's instruction file carries the same startup procedure; each platform's archiver copies only its own sessions' transcripts into Project/Sessions/ and leaves the other platform's files alone; the session numbers continue in one sequence whichever platform runs the session. The project's own files are not duplicated: one governing document, one handoff, one set of logs.
- **Full.** This platform's configuration replaces the other's. Build and verify the new configuration first; remove the old one after the verification below passes on this platform.

A project still in Chat takes neither path directly: it is migrated to Claude Code first, by the [migration guide](chat-to-code-migration.md), which is written for Claude Code, and then adapted from there.

On either path, the whole project is read before anything is changed: the governing document, the handoff, the index, the task queue, the logs, every sub-project. Each project is an independent implementation of the architecture and may have adapted it in ways that matter.

---

## Rules for the AI

These apply on both paths.

- **Read every file in this repo before building anything.** The README says so for every installer; it holds here too.
- **Work from the files and the user's answers.** The repo's files, the project's files and what the user says are the facts; infer nothing you can read or ask.
- **Tell the user what will happen, then ask the setup questions, then wait for the answers.** Nothing is written until the questions in the README's setup block are settled. On the adaptation path, the additive-or-full question comes first.
- **Deploy the template text as written.** The templates are deployable text, not specifications to re-express. Fill in the brackets and change only what the platform's mechanics require: the instruction file's name, the hook registration form, the fields a script reads and writes. Section names, section order, the handoff's scope header and the wording of every rule stay as they are.
- **The project's name comes from the user.** It is one of the setup questions. It is never taken from the opening message of the session, which names the session, not the project.
- **Ask how the user will name sessions, and record it.** The session number comes from the user at the start of each session, in whatever form they use. The suggested form, because it works on every platform, is to open the session with "This is [Project] N". Write the convention into the governing document's SESSION NUMBER entry, build the archiver to recognize it, and tell the user the next session's number when the setup ends.
- **Keep the startup orientation.** The startup procedure ends by presenting where work left off, what is pending and what the inbox holds, and asking how the user would like to begin. That step is the project's continuity made visible; it stays whatever the platform's conventions for opening a conversation.
- **Startup presents the handoff; it does not carry it out.** The items in the handoff are the state of the work. At startup they are shown to the user; none of them is acted on until the user says how to begin, including the setup checks the build itself left there.
- **Approvals the platform asks of the user stay with the user.** Where the platform requires the user to approve project scripts or folders before they run, tell the user what to approve and where, then wait. Do not try to give the approval yourself through another tool, a second session or a command-line copy of the platform.
- **Build the archive at session start.** A copy taken when a session ends is not the record: sessions end by the window closing, the machine sleeping, or the application quitting, and an end-of-session event may never fire. The archiver runs at the start of the next session, finds every finished transcript of this project in the platform's store, and copies what is not yet archived.
- **Write the archiver against a real transcript.** Before writing the matcher, open the first records of an actual session file in the platform's store and read the fields as they are; documentation and memory of the format are not enough. Then run the archiver once by hand against the store and confirm it finds this project's sessions.
- **Nothing about the adaptation goes inside the project** except one changelog line and the session log entry. The project's documents describe the work, not the platform it runs on. Reference material about the platform's mechanisms belongs in the instruction file's own notes or outside the project.
- **Report what you changed and why** when the work is done, in the conversation, as the README asks of every installer.

---

## What Maps to What

| In Claude Code | What the platform has to provide |
|---|---|
| CLAUDE.md at the project root, with `@` imports of the orientation files | The instruction file the platform loads at session start, at the project root. Without an import syntax, the startup procedure's step 1 lists the orientation files to read. |
| The governing document, handoff, index, task queue, session logs, sub-projects, Inbox, Archive | Unchanged. These are the project. |
| `.claude/settings.json` hook registration | The platform's registration of a per-message script and a session-start script. |
| `temporal-awareness.py` (UserPromptSubmit) | A script on the platform's per-message event that prints the local time in a form the platform adds to the model's context; or the clock-file method. |
| `archive-transcripts.py` (SessionStart) and `transcript_to_md.py` | A script on the platform's session-start event that copies this project's finished transcripts from the platform's store into Project/Sessions/, names them `[Project]_NNNN` from the session number, never copies the live session, never overwrites a different session, reports what it did into the session, and renders each copy to a readable Markdown file. The renderer is written against the platform's transcript format. |
| `.claude/skills/handoff/SKILL.md` | The same text as the platform's reusable prompt, where it has one. |
| `.claude/settings.json` permission rules; the permission mode | The platform's own permission system, set so that the project folder is writable, other folders are readable where the user allows, and everything else prompts. |
| Output style | The role and tone text, if any, in the instruction file. |
| Workspace trust | Whatever the platform requires before project-level configuration and scripts run. |

The scripts in [templates/claude-code/](templates/claude-code/) each open with a contract in platform-neutral terms: the input they receive, what they must do, the output they produce. A port is written to the contract, then checked against the platform's documentation for the event names and fields.

---

## Worked Example: OpenAI Codex

Codex runs in the ChatGPT desktop app and as a command-line tool. Its project mechanisms map onto the six needs as follows. Documentation: [AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md.md), [hooks](https://learn.chatgpt.com/docs/hooks.md), [skills](https://learn.chatgpt.com/docs/build-skills).

**Instruction file.** Codex reads `AGENTS.md` from the project root down to the working directory, concatenating the files it finds, with a default cap of 32 KiB on the combined size. There is no import syntax. `AGENTS.md` at the project root carries the startup procedure with step 1 listing the orientation files to read (PROJECT_CONTEXT.md, PROJECT_INDEX.txt, HANDOFF.txt, and TASKS.txt where the project has one), followed by the log, Inbox and orientation steps as in the CLAUDE.md template. On the additive path CLAUDE.md stays beside it with the same steps; the governing document's opening line names both.

**Hooks.** Project hooks are registered in `.codex/hooks.json`, with the same event names and the same input and output shape as Claude Code's: JSON on stdin carrying `session_id`, `transcript_path` and `cwd`; JSON on stdout with `hookSpecificOutput.additionalContext`. Command paths are relative to the project root. Two registrations:

- `UserPromptSubmit`: the time script, which reads and discards stdin, then prints the same JSON as the Claude Code version.
- `SessionStart` with the matcher `^startup$`: the archiver, so it runs when a session is opened and not when one is resumed or compacted.

Codex does not run project hooks until the user has reviewed and trusted each hook definition: the desktop app shows a review control in the message composer at the next session after `hooks.json` changes, listing new or changed definitions; the command-line tool has `/hooks`. Trust is recorded per definition, so an unchanged hook keeps its approval when another is added. Writing the `.codex/` and `.agents/` folders needs the user's approval, because the sandbox marks them read-only. The sequence is therefore: the session that writes the hooks; the next session, where the user trusts them and the time hook starts; and the session after that, where the archiver first runs. Tell the user this when the setup ends.

**The archiver.** Codex stores each session as a JSONL file under its home directory's `sessions/` tree (the home is `~/.codex` unless `CODEX_HOME` says otherwise); archiving a conversation in the app moves its file to `archived_sessions/`, so the archiver searches both. The first record of each file is a session record whose payload carries the working directory and the session id directly. Codex records the instruction file and an environment block as user-role messages before the user's own first message, so the opening message is not the first user record: the archiver scans the user messages for the form the user chose, and the renderer leaves the injected messages out. The port: find every session file whose working directory is this project; skip the live session (its path is on stdin); take the session number from the thread's title when the title carries the project name and a number, else from the user's opening message in the form they chose, else report the session as unnamed and leave it; copy to `Project/Sessions/[Project]_NNNN.jsonl` unless a different session already holds that name, in which case keep the existing file and report the conflict; before copying, check the session ids of the files already archived and skip a session archived under any name, and derive each session's name from its own transcript alone, so a later run never gives the same session a second name; render a readable Markdown file beside each copy from the records actually present (user and assistant messages, tool calls with their command text), skipping record types it does not know. Codex documents its transcript format as not a stable interface, so the archiver reports every failure into the session through `additionalContext` rather than failing silently, and the renderer tolerates unknown records.

Codex also has a `SessionEnd` event. It fires when a conversation is archived or deleted, when the application closes normally, or after thirty minutes idle with no connected client; opening a new conversation does not end the previous one. It is not the archive trigger.

**The skill.** `.agents/skills/handoff/SKILL.md`, with `name` and `description` in its frontmatter and the two sentences pointing at SESSION CLOSE in the governing document; invoked with `$handoff` or when the user asks to close the session.

**Permissions.** Codex has no project-level permission file; the sandbox and the approval mode set in the app or on the command line decide what runs without asking. Writes inside the project folder are approved per edit in the asking mode. No rules are written for this; the user sets the mode.

**Additive layout.** When CLAUDE.md and `.claude/` stay beside `AGENTS.md` and `.codex/`, each archiver handles only its own platform's transcripts: the Claude Code archiver checks that a file in Project/Sessions/ is in its own format before comparing or rendering it, and the Codex archiver reads the session id from its own first record and reports a conflict when it finds none. Session numbers continue in one sequence; the user opens each session with the same form on either platform.

---

## Verification

The check in the [setup guide](claude-code-setup.md#7-verify) applies, with its rule that a project's sessions are the ones run in its own folder. A build or adaptation run from a session inside the project is one of the project's sessions, numbered in its sequence, and the next session checks every item, the archive included. One run from a session outside the project's folder is not: the project's first session on this platform checks the startup items, and the session after it checks the archive. Where the platform requires the user to trust the hooks before they run, the user trusts them in the project's next session, the time hook starts there once trusted, and the archive check falls to the session after that one.

On the additive path, run the same check on the other platform afterwards: its startup reads the files the new platform wrote, and its archiver takes its own session and leaves the new platform's files alone.

---
*Part of [AI Project Architect](https://github.com/vbiroshak/ai-project-architect) — Version 4.11*
