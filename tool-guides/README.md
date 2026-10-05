# Tool Guides

Operational reference for using specific tools well. Each guide is standalone and covers one tool.

Tool guides answer "how do I use this tool efficiently and correctly?" They're loaded on demand by projects that use the tool, not at startup. A project that doesn't use a given tool doesn't need its guide.

Tool guides are distinct from patterns. A pattern describes a type of thing in the workspace or a technique that shapes how work is done. A tool guide describes how to operate a specific tool. See [Tool Guides in the architecture doc](../workspace-architecture.md#tool-guides) for the full distinction.

## Guides

| Guide | What it covers |
|-------|---------------|
| [Chrome DevTools Guide](chrome-devtools-guide.md) | DOM-first approach to Claude in Chrome. Tool reference, click-by-ref workflow, screenshot decision rule, form filling patterns, verification techniques. |

## Adoption

Copy the guides you need into your project's `Project/Tool Guides/` directory. Save them with a `.txt` extension — the repo uses `.md` for GitHub rendering, but deployed project files use `.txt`. List them in your governing document's TOOL GUIDES section so the AI reads them on demand when relevant work begins.

---
*Part of [AI Project Architect](https://github.com/vbiroshak/ai-project-architect) — Version 4.9*
