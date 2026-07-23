# Agentic Task Delegation

A methodology for delegating bounded tasks to agentic tools while retaining strategic oversight in conversation.

---

## When to Delegate

Delegation works well when a task is:

- Detail-intensive at scale (reading many files, auditing, sorting, building indexes, bulk edits)
- Clearly bounded to a specific scope
- Describable without needing the full project context
- Something that would consume significant context window and conversation time if done inline

Examples: organizing source documents into case folders, sorting and identifying meaningful data in archival collections, categorizing and renaming financial documents, processing batches of emails or screenshots, building inventories of large file collections, extracting structured data from unstructured sources, auditing files for consistency, applying mechanical changes across a codebase or workspace.

Delegation does not work well for tasks requiring strategic judgment or project context, drafting that needs voice calibration, work that depends on decisions not yet made, or anything where the right answer requires understanding the broader project.

---

## Know Your Delegate

One common mistake in writing delegation prompts is not understanding who you're writing for. Different agents have different models, tools, and capabilities. A prompt written for the wrong level of capability either over-constrains a capable agent (spelling out what it can figure out) or under-specifies for a limited one (assuming judgment it can't exercise).

Before writing a prompt, establish:

- **What model is the agent running?** A frontier model reasons, infers, and adapts. A smaller model needs more explicit structure. Writing step-by-step instructions for a frontier model wastes prompt space on procedure it would handle better on its own. Writing loose goals for a small model produces unreliable results.
- **What tools does it have?** Filesystem access, code execution, web search, sub-agent coordination, ability to delete files? The prompt should be written for the tools available, not for the tools the prompt author uses.
- **What can it do that you can't?** Agentic tools often have capabilities the conversational AI doesn't: running scripts, coordinating parallel workers, processing files at scale, interacting with the filesystem in ways a chat session cannot. A good prompt leverages these rather than dictating a procedure the agent would improve on.
- **What context does it lack?** The agent typically has no access to project history, conventions, or strategic context. The prompt supplies the context the agent needs, not a procedure to follow.

The general principle: delegation prompts are proposals, not instructions. A capable agent receiving a well-contextualized prompt will often find a better approach than the one the prompt author imagined. Write for understanding, not compliance.

---

## The Process

### 1. Scope the Task

Identify what needs doing, what the inputs are, and what the output should look like. Make key decisions before writing the prompt. The delegate has no project context to inform judgment calls.

Questions to resolve: What's the scope (which files, folders, systems)? What does the output look like? What should the delegate not touch? What documentation should it produce?

### 2. Draft the Prompt

Write task instructions as a standalone text file saved to the project. The prompt must contain everything the delegate needs without any other context.

What goes in the prompt depends on the delegate's capabilities (see Know Your Delegate). For a capable agent, focus on:

- What the task is and why it matters (context, not just procedure)
- What the files or inputs actually look like, with concrete examples
- What the output should look like
- Constraints and boundaries (what not to modify, what to skip)
- Where to write results

For less capable agents, add more explicit structure: step-by-step sequences, format specifications, verification checklists.

The prompt author is typically a conversational AI with project context but without the delegate's tools. This means the prompt may contain assumptions about the filesystem, file contents, or approach that don't hold. The next step catches this.

### 3. Have the Delegate Review the Prompt

Before running the task, give the delegate the prompt and ask for feedback. This is not optional for complex delegations.

The delegate brings operational perspective the prompt author lacks: knowledge of its own tools, awareness of edge cases in filesystem operations, better strategies for parallelism or batching, and ability to spot assumptions that don't match the actual file state. A prompt that looks complete from the conversational side often has significant improvements the delegate identifies immediately.

The review-then-iterate cycle is the core of good delegation. The conversational AI provides project context and strategic intent. The delegate provides operational expertise. Neither alone writes the best prompt.

### 4. Hand Off

The human provides the prompt to the delegate and points it at the appropriate scope. Start a fresh session for each task. Leftover context from previous tasks causes unexpected behavior.

Scope the delegate's access to what it needs. Broader access than necessary lets it get distracted or make changes outside the task boundary.

### 5. Monitor

The human monitors execution. The conversational AI advises if questions arise, relaying information between the delegate and the conversation as needed. Watch for the delegate requesting permissions beyond what the task requires, or creating unexpected artifacts.

### 6. Review and Integrate

The conversational AI reviews what the delegate produced: checks outputs, reads any documentation or reports, verifies nothing was missed or mishandled. Then does the integration work that requires project context: updating cross-references, writing to project files, connecting the output to the broader project state.

---

## Examples

The examples below use Claude's Cowork feature, but the pattern applies to any agentic delegation: Claude Code, custom scripts, or equivalent features in other AI platforms.

**Cowork (Claude Desktop):** Has full filesystem access including the ability to delete files. Can coordinate and run sub-agents in parallel. Can run code. Can process files at scale. The prompt should provide context and constraints, not step-by-step procedure. Cowork will figure out the approach. See the companion [Cowork Delegation Guide](../tool-guides/cowork-delegation-guide.md) for operational details.

**Claude Code:** Runs in the terminal. Has code execution and filesystem access. Strong at programmatic tasks: writing and running scripts, git operations, code refactoring. The prompt can describe the goal and let it choose the implementation.

**Custom scripts or smaller models:** May need more explicit structure, verification steps, and output format specifications depending on capability.

---

## What Stays in Conversation vs. What Gets Delegated

The delegate handles work that is bounded and describable without project context. The conversational AI handles everything that requires strategic judgment, project knowledge, voice calibration, or integration across the project.

The division: the delegate reads, processes, sorts, audits, and documents. The conversational AI judges, writes, connects, and integrates.

---
*Part of [AI Project Architect](https://github.com/vbiroshak/ai-project-architect) — Version 4.7*
