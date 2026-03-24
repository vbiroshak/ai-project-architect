# Project Instructions Template

Paste this into your AI project's custom instructions. Replace `[path]` with the actual path to your project directory on your filesystem. This is the same text that appears in the architecture document, extracted here for quick reference.

The example below uses Claude Desktop's Filesystem extension. Adapt the tool names for other AI platforms with filesystem access.

```
Workspace: All project files live on the filesystem at [path]. At session startup, call Filesystem:list_allowed_directories to confirm filesystem access. Then call Filesystem:list_directory on the project path to confirm you can read it. These tools provide full read and write access to the project filesystem, including write_file, edit_file, move_file, and create_directory.

When Filesystem is available, read WORKFLOW.txt and follow its procedures.

When Filesystem is unavailable, let the user know and explain that the session will operate from project memory and conversation context. Capabilities will be limited compared to Desktop sessions. Note any decisions or information that should be synced to the filesystem next time Desktop access is available.
```

## Why it's structured this way

The three-block structure exists because AI assistants skip evaluating implicit conditions. "When Filesystem is available, do X" assumes the AI has already checked availability, but nothing forces that check. Making the check an explicit action in the first block fixes this.

The first block tells the AI exactly what tool calls to make and confirms both access and write capabilities. The second block routes to WORKFLOW.txt, which contains everything else. The third block handles graceful degradation when filesystem access isn't available.

You paste this once and never edit it again. All workflow evolution happens in the filesystem files that the AI maintains directly.
