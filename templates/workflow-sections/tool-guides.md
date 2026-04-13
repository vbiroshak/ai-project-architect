# Tool Guides

WORKFLOW section — universal, identical across all projects.

## Template Text

```
---
TOOL GUIDES

Operational guides for using specific tools well. Read on demand when starting work that uses the tool.

  CHROME BROWSER: Claude in Chrome is available for live web tasks but Chrome is not normally running. When you need to access a live web page, ask the user to open Chrome. The web_fetch tool returns stale cached content for some sites. See Workflow Files/Tool Guides/chrome-devtools-guide.txt.

  FILESYSTEM TOOLS: bash_tool operates on Claude's container, not the user's filesystem, and cannot see or modify project files — do not reach for it as a default. Use Filesystem tools (prefix Filesystem:) for all file operations on project files. See Workflow Files/Tool Guides/filesystem-tools-guide.txt.

  COWORK DELEGATION: Cowork is available for delegating bounded, detail-intensive tasks. See Workflow Files/Tool Guides/cowork-delegation-guide.txt for prompt structure, sub-agents, and safety patterns.
```

## Notes

Lists the tool guides available in `Workflow Files/Tool Guides/`. Each entry is a one-line operational pointer plus a guide path. Projects adopt only the guides relevant to their work; entries for unused tools can be omitted. The section reframes default tool selection at startup so the AI doesn't slip into bash-first thinking when the project lives on the user's filesystem.

---
*Part of [AI Project Architect](https://github.com/vbiroshak/ai-project-architect) — Version 4.2*
