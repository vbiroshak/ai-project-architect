# Cowork Delegation Guide

Reflects tool behavior as of April 2026. Cowork's capabilities evolve frequently; verify against the official documentation links at the bottom before modifying this guide.

Operational guide for delegating tasks to Cowork well. Read before writing a Cowork prompt. For the general methodology (when to delegate, the process, what stays in conversation), see the [Agentic Task Delegation](../patterns/agentic-delegation.md) pattern. This guide covers Cowork-specific operational knowledge: what it is, how to write prompts for it, and what to watch for.

---

## What Cowork Is

Cowork runs Claude in an agentic architecture built on the Claude Agent SDK. It has its own system prompt, a skills system, MCP server integrations, and a sandboxed Linux shell. It runs the same underlying models available to Chat and Code, but operates in a fundamentally different mode: an agentic tool-use loop where it proactively reads, writes, executes, and verifies rather than responding to conversational turns.

### Capabilities

**Filesystem:** Read, write, edit, glob, grep, delete (with user approval per directory — Cowork requests permission when needed). Starts with access to the directory the user selects, but can request access to additional directories during the session.

**Shell:** Sandboxed Linux bash with Python, Node, and common CLI tools. Can install additional packages (pip, npm). This means specialized libraries (pandas, python-docx, Pillow, etc.) are available for data processing, format conversion, and analysis.

**Web:** Web search, web fetch. Available without additional setup.

**Browser:** Full browser automation via Claude in Chrome (navigate, screenshot, read page, click, fill forms, execute JavaScript, read console and network requests). Requires computer use to be enabled in Settings.

**Documents:** Skill-driven creation of docx, pptx, xlsx, and pdf. Skills are SKILL.md files containing tested instructions for each format. Cowork reads the relevant skill before beginning document work, which means it has accumulated best practices for formatting, library choices, and output quality. Prompt authors should focus on content and requirements, not formatting mechanics.

**External services:** MCP connectors to services like Slack, Asana, Jira, Google Drive, and others. Require user setup and connection.

**Interaction:** Can ask the user structured questions mid-task, with freeform response available as an option. The user can also queue messages for Cowork mid-task. For tasks with a few predictable decision points, Cowork can handle them without needing every decision pre-made in the prompt.

**Scheduling:** Can create recurring or one-time scheduled tasks. A capability Chat does not have.

**Sub-agents:** Parallel worker dispatch for batch operations.

**Progress:** Uses a TodoList tool that renders as a visible progress widget. The user can see which step Cowork is on, what's completed, and what remains. Prompt authors don't need to build in "report your progress" instructions.

### Context and Memory

Cowork has its own form of projects: persistent, self-contained workspaces with their own files, links, instructions, and memory, which are structurally different from Chat projects. It also has sessions, user preferences that persist across sessions, and the skills system. A prompt author who assumes Cowork works like Chat projects may set expectations that don't match. User preferences do provide some continuity (formatting, communication style, working patterns), so you don't need to redundantly specify those.

---

## Who You're Writing For

A common failure when writing Cowork prompts is misunderstanding who you're writing for. There are two mistakes to watch for:

**Writing down:** treating Cowork as a lesser model that needs step-by-step instructions, explicit tool usage guidance, and hand-holding through a procedure. This over-constrains an Opus-level agent and produces worse results than letting it figure out the approach.

**Writing sideways:** treating Cowork as if it were another Chat session with your project instructions, project files, and conversation history loaded into context. Cowork has none of these. References to "the project," "our conventions," or "the approach we discussed" mean nothing to it.

The correct frame: Cowork is a peer with different tools and no shared Chat-side context (though Cowork's own standing instructions and user preferences do persist). Give it the problem, the constraints, and enough concrete detail about the actual files to work with. Let it figure out the approach. Its operational perspective (tool awareness, parallelism strategies, edge case handling) is often better than what Chat would specify.

---

## Prompt Structure

A good Cowork prompt is a standalone document. It contains everything the agent needs without any other context. The structure of an effective Cowork prompt:

**Background:** What the task is and why it matters. If earlier attempts failed, describe what went wrong and why. This prevents Cowork from repeating the same mistakes and gives it the full problem shape.

**What the files actually look like:** Show real examples from the actual files, with line numbers or paths. Not descriptions of what the files contain — actual content samples. Concrete examples are what let Cowork build accurate detection logic.

**What the output should look like:** Specific format, location, naming. If an index, show the exact entry format. If modified files, show before-and-after examples. For document creation tasks (docx, pptx, xlsx), focus on content and structure. Cowork's skills handle formatting mechanics.

**Constraints and boundaries:** What not to touch, what to skip, what directories are off-limits. Path exclusions. File types to ignore. Golden rules for ambiguous cases (e.g., "when in doubt about duplicates, KEEP BOTH").

**Test cases:** For any task involving file modification or data extraction, include test cases with expected results. Specific files, specific lines, specific expected outcomes. An effective quality mechanism.

**Process requirements:** If the task requires a specific execution order (like dry-run-then-verify), state it explicitly and explain why.

**What does NOT go in a Cowork prompt:** tool usage instructions (it knows its tools better than Chat does), step-by-step procedure for how to write code (it will write better code than Chat would specify), project context it doesn't need for the task, formatting mechanics for document types where Cowork has skills.

---

## Sub-Agent Architecture

Cowork can dispatch parallel sub-agents, which is its primary advantage for scale tasks. Operational knowledge:

**Batch sizing:** There is a reliable agent/item ratio, and it shifts as Cowork evolves. Below the current reliable ceiling, sub-agents inspect each file properly. Above it, they begin hallucinating metadata for later entries rather than actually reading files, and the failure mode is silent — the output looks plausible but is fabricated. Because the failure is silent, Cowork cannot self-assess the ceiling reliably from inside. Under-size, verify the output, and scale up only if verification holds. Asking Cowork for an estimate can give a best-guess starting point but does not replace verification. Over-sizing corrupts the output.

**Anti-hallucination safeguards:** Include explicit instructions like "MUST actually inspect each file. Do NOT fabricate descriptions from filenames. If a file cannot be read, output 'UNREADABLE' rather than guessing." Without this, agents under load will infer metadata from filenames and output confident-sounding fabrications.

**Output format consistency:** Give each agent the exact output format template. Agents with vague instructions produce inconsistent formats that are painful to merge. Include a literal example entry, not just a format description.

**Splitting strategy:** By subfolder when folders are roughly equal size. Alphabetically when a single folder is too large. Very small folders can be combined into one agent's batch. The prompt should specify the split or let Cowork decide based on its discovery phase.

---

## File Handling

Cowork works in two directory contexts:

**Session directory:** A temporary scratch space where Cowork does intermediate work. Files here are not immediately visible to the user.

**User workspace:** The directory the user selected when starting the task. Final deliverables go here and are presented via file cards in the conversation.

If a prompt says "save results to [path]" and that path is inside the user's workspace folder, Cowork writes there directly. Understanding this two-directory model explains why Cowork sometimes creates files that aren't immediately visible — they may be in the session directory, not yet copied to the workspace.

Cowork can also request access to additional directories on the user's machine beyond the initially selected one.

---

## Safety Patterns

**Dry-run-then-verify:** For any task that modifies files, the prompt should require a dry-run mode. Write output files alongside originals without modifying them. Verify against test cases. Only after verification, apply changes.

**Backup traps:** Backups taken between phases can become stale. If Cowork takes a backup at the start of phase 1, then other work happens, restoring that backup overwrites the intervening changes. The prompt should explicitly warn: take a fresh backup immediately before applying, not at the start of the task.

**Idempotency proof:** After applying changes, run the script again and confirm zero modifications. This proves the script doesn't double-apply and that the output is stable.

**Source preservation:** For tasks that merge, organize, or restructure files, the prompt should specify COPY to the output location, never MOVE or DELETE from the source. The user decides when to clean up sources after verifying the output.

---

## The Prompt Review Cycle

The [agentic delegation pattern](../patterns/agentic-delegation.md) describes prompt review as a core step, not optional. For Cowork specifically:

Chat writes the initial prompt from project context. Cowork reviews it and suggests improvements. This cycle matters because Cowork brings operational perspective Chat lacks: knowledge of its own tools, awareness of edge cases in filesystem operations, better strategies for parallelism and batching, and the ability to spot assumptions about file contents that don't match reality.

For simple, bounded tasks (create INDEX.txt files, rename files matching a pattern), the review step can be skipped. The threshold: if the task modifies files or has edge cases, get the review.

---

## What Makes a Good Delegation Candidate

Tasks that work well with Cowork:

- Bulk file operations across many directories (text reformatting, metadata standardization)
- Building indexes from large file collections (document libraries, research archives)
- Deduplication, merging, and reorganization of overlapping file sets
- Auditing files for consistency (format standards, naming conventions)
- Document creation from specifications (presentations, reports, spreadsheets) — Cowork's skill system produces high-quality output for supported formats
- Web research compiled into a local document or report
- Tasks that combine web lookup with file creation or modification
- Recurring tasks that should run on a schedule
- Tasks requiring external service data (with appropriate MCP connectors)
- Any task where the volume makes it impractical in Chat

Tasks that don't work well:

- Anything requiring project strategic context (Cowork doesn't have it)
- Work where the right answer depends on decisions not yet made
- Drafting that needs voice calibration or iterative creative feedback
- Tasks requiring extensive iterative judgment where the back-and-forth of Chat conversation is the point (Cowork can ask structured questions mid-task, but Chat's fluid conversation is better for exploratory work)

---

## Documentation

Anthropic's official documentation (capabilities may have changed since this guide was written):

- [Get started with Cowork](https://support.claude.com/en/articles/13345190-get-started-with-cowork)
- [Cowork product page](https://www.anthropic.com/product/claude-cowork)
- [Install Claude Desktop](https://support.claude.com/en/articles/10065433-install-claude-desktop)

---
*Part of [AI Project Architect](https://github.com/vbiroshak/ai-project-architect) — Version 4.7*
