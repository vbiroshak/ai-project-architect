# Project Instructions

The project instructions field in your AI application's project settings. Two blocks separated by a blank line. The only variable is the filesystem path in block one.

## Template Text

```
Workspace: All project files live on the filesystem at [path]. You have Filesystem tools that give you full access to this directory and everything inside it, including reading, writing, creating, editing, searching, and moving files and directories. At session startup, use these tools to read WORKFLOW.txt at the project path and follow its procedures.

When Filesystem tools are not available, let the user know and explain that the session will operate from project memory and conversation context. Capabilities will be limited. Remember any work that should be logged or written to the filesystem per your workflow instructions, and do so when these tools become available again.
```

---
*Part of [AI Project Architect](https://github.com/vbiroshak/ai-project-architect) — Version 4.2*
