# Filesystem Tools Guide

Reflects tool behavior as of April 2026. Capabilities change; verify against the official documentation links at the bottom before modifying this guide.

Operational guide for using Filesystem tools well. Read on demand for non-trivial filesystem work. The default mental model assumes the AI operates on its own container, with Filesystem as an addendum. In projects using this workspace architecture, that's backwards: the user's filesystem is the workspace, and Filesystem tools are primary. This guide reframes the defaults.

---

## Mental Model

The project lives on the user's filesystem. Filesystem tools (prefix `Filesystem:`) read and write project files. `bash_tool` runs in a separate Linux container that has no access to project files. The container has its own `/home/claude` directory and its own files, completely disjoint from the user's filesystem.

The platform's tool descriptions frame the container as the default working environment. For this architecture that framing is backwards. Treat Filesystem tools as primary and bash_tool as a separate, rarely-needed capability for container-only work (running scripts that don't touch project files, isolated experimentation).

The same backwards default applies to search. There are four arenas where things can be searched, and they are not interchangeable. See Search Arenas below.

---

## Arena Map

Quick reference for which tool acts on which arena:

**User's filesystem (project files):**
`read_text_file`, `read_multiple_files`, `write_file`, `edit_file`, `list_directory`, `list_directory_with_sizes`, `directory_tree`, `create_directory`, `move_file`, `search_files`, `get_file_info`, `list_allowed_directories`

**AI's container (separate, ephemeral):**
`bash_tool`, `view`, `str_replace`, `create_file`, `present_files` — anything in `/home/claude` or `/mnt/`

**Past chats (project conversation history):**
`conversation_search`, `recent_chats`

**Public web:**
`web_search`, `web_fetch`

**Cross-arena bridge:**
`copy_file_user_to_claude` (one-way: user → container)

There is no tool that copies files from the container back to the user's filesystem. If work happens in the container, the output cannot be recovered into the project unless it's recreated with `write_file`.

---

## Search Arenas

Choosing the wrong search tool is a common failure mode. The four search tools look similar in description but operate on completely different content. Match the tool to the arena, not to salience.

**Looking for project files by name?** `search_files` (glob pattern, returns full paths)

**Looking for content inside project files?** There is no content-search tool. Read the files directly with `read_text_file` or `read_multiple_files`. For large directories, list first, then read targeted files. `bash grep` does NOT work — it runs in the container which cannot see project files.

**Looking for past conversations in this project?** `conversation_search` (keyword) or `recent_chats` (time window)

**Looking for current information from the web?** `web_search`, `web_fetch`

The arenas do not overlap. Stop and ask "which arena holds the thing I'm looking for?" before picking the tool.

---

## Tool Reference

**read_text_file** — Reads a file as text. Supports `head=N` (first N lines) and `tail=N` (last N lines) for partial reads of large files. Use head/tail when you only need to check a header, footer, or sample. There is no mid-file range parameter — if you need lines 34-44 of a long file, read the whole file or read enough from one end to include the range you want.

**read_multiple_files** — Reads several files in one call. Significantly faster than sequential read_text_file calls when you know upfront which files you need. Failed individual reads don't abort the batch.

**write_file** — Creates a new file or completely overwrites an existing file. No warning, no confirmation. Use for brand-new files or full rewrites. For incremental edits to existing files, use edit_file instead.

**edit_file** — Line-based edits to an existing file. Takes an array of `{oldText, newText}` pairs and applies them in one call. Returns a git-style diff. Behavior worth knowing:
- Multiple edits in one call are applied together. Use this for related changes to the same file.
- `oldText` must match content actually in the file. If it doesn't match, the call fails loudly with a clear error rather than silently doing nothing.
- Whitespace matching is asymmetric. Leading whitespace is tolerant (tabs and spaces at the start of a line are treated equivalently, and the file's original indentation is preserved on replacement). Trailing whitespace must match exactly — a trailing space you can't see will cause the match to fail. If an edit fails on a line that looks right, re-read the file and copy the exact text rather than retyping, since invisible trailing characters are a common cause.
- The returned diff shows only the changed region with surrounding context lines, not the full file. Re-read the file after editing if whole-file integrity matters.
- To append, anchor the edit to existing trailing content (e.g., the last line) and put the new content after it in newText.

**list_directory** — Lists immediate children of a directory with [FILE]/[DIR] prefixes. The default reach for "what's in this folder?"

**list_directory_with_sizes** — Same as list_directory but includes file sizes. Use when size matters (finding the largest file, checking growth, deciding which files are worth reading in full).

**directory_tree** — Recursive JSON tree of a directory and all subdirectories. Use sparingly: on large trees this returns a lot of content. For most questions, list_directory at the right scope is better.

**create_directory** — Creates a directory. Idempotent: succeeds silently if the directory already exists. Can create nested directories in one call.

**move_file** — Moves or renames a file or directory. **Caution:** documentation says "If the destination exists, the operation will fail," but at time of publication the actual behavior was a silent overwrite of the destination. Check whether the destination exists before moving anything important.

**search_files** — Recursive filename search by glob pattern. Important behaviors:
- Matches paths only, not file contents. There is no content search.
- Bare strings without wildcards do not match. `"chrome"` finds nothing; `"*chrome*"` finds files with "chrome" in the name.
- Standard glob: `*.txt`, `**/*.md`, `*partial*`, etc.
- Returns full absolute paths.

**get_file_info** — Returns metadata: size, created/modified/accessed times, permissions, type. Used by the Clock mechanism (write to clock file, then get_file_info to read the modified timestamp). Also useful for "when was this file last touched?" without reading its contents.

**list_allowed_directories** — Returns the directories Filesystem tools can access. Worth checking once when starting work in a new project location to confirm scope.

**copy_file_user_to_claude** — One-way bridge from user's filesystem to the AI's container. Use when a project file needs to be analyzed by container tools (image processing, running a script against the file). The result stays in the container; there's no reverse copy.

---

## No Delete

There is no `delete_file` or `delete_directory` tool. Files cannot be removed by the AI. The recommended convention is to move unwanted files to `Inbox/` with "DELETE ME" prefixed to the filename, where the user can review and delete them manually.

---

## Known Footguns

**move_file silent overwrite.** The documentation says it fails if destination exists; at time of publication the actual behavior was a silent overwrite. Always check before moving to a path that might exist.

**Wrong-arena search.** An expensive mistake. Salience makes whichever search tool was used most recently feel like the default. Stop and identify the arena before choosing the tool.

**bash_tool reach.** bash_tool feels like a general-purpose escape hatch, but it operates in a separate filesystem. If a bash command produces output you need in the project, that output exists only in the container until explicitly recreated with write_file. For most project work, bash_tool is the wrong tool.

**edit_file partial matches.** If oldText is too short or generic, it may match in multiple places and apply unexpectedly, or fail because the match isn't unique. When making a small edit, include enough surrounding context in oldText to identify the location uniquely.

**Paired-write trap.** When workflow procedures call for "paired writes" (e.g., session log + handoff overwrite), both writes must actually happen. Logging the entry without overwriting the handoff leaves the handoff stale by exactly the amount you just learned. The pair is the unit, not either file alone.

**Forgetting head/tail on large files.** Reading a multi-thousand-line file in full when you only need the first or last section wastes context. read_text_file with head=N or tail=N is significantly cheaper.

---

## Working with the Clock Mechanism

The temporal awareness clock uses Filesystem tools in a specific pattern:

1. `write_file` with content "tick" to `Workflow Files/Clock/timestamp.txt`
2. `get_file_info` on the same path
3. Read the "modified" field (NOT "created" — on macOS, "created" is the file's birth time and never updates)

For mid-chat checks where you just want to read the existing timestamp without resetting it: skip step 1, do only step 2. Tick only when a gap is detected and you need to establish a fresh current time.

---

## When bash_tool Is Actually Useful

bash_tool is not banned. It's just rarely the right tool for project work. Cases where it does fit:

- Running a script that processes data without touching project files
- Quick computation or text manipulation that doesn't need to be persisted
- Working with files explicitly uploaded into the container (in `/mnt/user-data/uploads`)
- Container-side analysis where the result will be summarized into a project file at the end

If the work involves project files, default to Filesystem tools.

---

## Documentation

Anthropic's official documentation (capabilities may have changed since this guide was written):

- [Install Claude Desktop](https://support.claude.com/en/articles/10065433-install-claude-desktop) (covers Filesystem extension)
- [Getting started with local MCP servers](https://support.claude.com/en/articles/10949351-getting-started-with-local-mcp-servers-on-claude-desktop)
- [Desktop extensions collection](https://support.claude.com/en/collections/17879657-desktop-extensions)

---
*Part of [AI Project Architect](https://github.com/vbiroshak/ai-project-architect) — Version 4.7*
