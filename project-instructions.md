# Project Instructions Template

Paste this into your AI project's custom instructions. Replace `[path]` with the actual path to your project directory on your filesystem. This is the same text that appears in the architecture document, extracted here for quick reference.

The example below uses Claude Desktop's Filesystem extension. Adapt for other AI platforms with filesystem access.

```
Workspace: All project files live on the filesystem at [path]. You have Filesystem tools that give you full access to this directory and everything inside it, including reading, writing, creating, editing, searching, and moving files and directories. At session startup, use these tools to read WORKFLOW.txt at the project path and follow its procedures.

When Filesystem tools are not available, let the user know and explain that the session will operate from project memory and conversation context. Capabilities will be limited. Remember any work that should be logged or written to the filesystem per your workflow instructions, and do so when these tools become available again.
```

## Why it's structured this way

The instructions describe capabilities using verbs (reading, writing, creating, editing, searching, moving) rather than naming specific tools. This means extension updates that rename, add, or remove tools don't require instruction changes. "Filesystem tools" maps to the prefix the AI sees on every tool in its context.

The first block asserts what the tools can do and commands an action: read WORKFLOW.txt. There is no evaluation step where the AI decides whether it has access. The second block handles graceful degradation when the tools aren't available (web, mobile) and instructs the AI to catch up on logging when the tools return.

You paste this once and never edit it again. All workflow evolution happens in the filesystem files that the AI maintains directly.
