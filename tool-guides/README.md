# Tool Guides

Operational reference for using specific tools well. Each guide is standalone and covers one tool.

Tool guides answer "how do I use this tool efficiently and correctly?" They're loaded on demand by projects that use the tool, not at startup. A project that doesn't use a given tool doesn't need its guide.

Tool guides are distinct from patterns. A pattern describes a type of thing in the workspace or a technique that shapes how work is done. A tool guide describes how to operate a specific tool. See [Tool Guides in the architecture doc](../workspace-architecture.md#tool-guides) for the full distinction.

## Guides

| Guide | What it covers |
|-------|---------------|
| [Chrome DevTools Guide](chrome-devtools-guide.md) | DOM-first approach to Claude in Chrome. Tool reference, click-by-ref workflow, screenshot decision rule, form filling patterns, verification techniques. |
| [Filesystem Tools Guide](filesystem-tools-guide.md) | Which tools act on which arena (user filesystem vs. container vs. past chats vs. web). Search decision rule, tool reference with gotchas, known footguns. |
| [Cowork Delegation Guide](cowork-delegation-guide.md) | Writing effective Cowork prompts. Architecture and capabilities, prompt structure, sub-agent batch sizing, safety patterns, the prompt review cycle. |

## Adoption

Copy the guides you need into your project's Tool Guides/ directory (`Workflow Files/Tool Guides/` in Chat, `Project/Tool Guides/` in Code). Save them with a `.txt` extension — the repo uses `.md` for GitHub rendering, but deployed project files use `.txt`. List them in your governing document's TOOL GUIDES section so the AI reads them on demand when relevant work begins.

The Filesystem Tools and Cowork Delegation guides apply to Chat projects only. The Chrome guide applies to both platforms.

---
*Part of [AI Project Architect](https://github.com/vbiroshak/ai-project-architect) — Version 4.6*
