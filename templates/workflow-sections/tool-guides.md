# Tool Guides

WORKFLOW section — universal, identical across all projects.

## Template Text

```
---
TOOL GUIDES

Required guides to read before using tools.

  CHROME BROWSER: Before loading any Claude in Chrome tool via tool_search, read Workflow Files/Tool Guides/chrome-devtools-guide.txt. Claude in Chrome is available for live web tasks. Try the tool first; if Chrome isn't running, the tool will say so and you can ask the user to open it. The web_fetch tool returns stale cached content for some sites.

  FILESYSTEM TOOLS: bash_tool operates on Claude's container, not the user's filesystem, and cannot see or modify project files — do not reach for it as a default. Use Filesystem tools (prefix Filesystem:) for all file operations on project files. See Workflow Files/Tool Guides/filesystem-tools-guide.txt.

  COWORK DELEGATION: Before delegating or writing prompts, read Workflow Files/Tool Guides/cowork-delegation-guide.txt. Cowork is available for delegating bounded, detail-intensive tasks.
```

## Notes

Lists the tool guides available in `Workflow Files/Tool Guides/`. Chrome and Cowork entries carry hard preconditions — the guide must be read before loading or using the tool. Projects adopt only the guides relevant to their work; entries for unused tools can be omitted.

---
*Part of [AI Project Architect](https://github.com/vbiroshak/ai-project-architect) — Version 4.3*
