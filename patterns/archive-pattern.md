# Sub-Project Archive Pattern

---

## The Problem

A completed sub-project's files clutter the project root beside active work, get loaded by activation sequences that no longer apply, and give no sign whether the work is finished or dormant. The project still needs to reference completed work when it comes up.

Deleting loses the record; leaving the files in place obscures what is active. The pattern freezes completed work, keeps it discoverable, and clears the root for what is live.

---

## The Solution

### Structure

Archive/ lives at the project root, alongside active sub-projects. The root always shows only what is live plus one archive folder.

```
Project/
  [governing document]
  Inbox/
  [project infrastructure]/
    HANDOFF.txt
    Session Logs/          ← stay at project level, never archived
  Archive/
    ARCHIVE_INDEX.txt      ← archive inventory
    Completed Project - YYYY-MM/   ← frozen
  Active Project/                  ← live work
```

### Naming

"Project Name - YYYY-MM", the completion date only: it is what you need at a glance, sortable and unambiguous. Start dates are in the session logs.

### Closing Before Archiving

Before moving a sub-project to Archive/, add a closing note to its status file: completed, the archive date, a pointer to any successor. The archived file then explains why it stops where it does and where the remaining work went.

### Discoverability

Two layers ensure past work is findable:

1. **ARCHIVE_INDEX.txt** inside Archive/ holds a brief inventory: a few lines per entry on what the sub-project covered, when it completed, where it lives in Archive/, and its key files. Future sessions check here when past work is referenced.

2. **The governing document** carries the convention in its sub-project activation section (completed work moves to Archive/; ARCHIVE_INDEX.txt holds the inventory), so the archive is reachable from startup without adding to startup reads.

### Session Logs

Session logs stay at the project level: they span all sub-projects, past and present, and do not move into the archive with the sub-project they covered.

### Seeding a Successor

When remaining work from a completed sub-project becomes a new one, seed it with current data only: read each file against the current state and the session logs, and carry forward only what the new sub-project needs. It gets its own status file, task queue, and reference material, built fresh.

---

## Activation Sequence Maintenance

When a sub-project is archived and a new one created, update the governing document's activation section: add the new sub-project and remove the old entry, since archived sub-projects are read directly, not activated.

---

## Implementation

The archive convention is carried in the governing document's sub-project activation section: see the [PROJECT_CONTEXT template](../templates/claude-code/PROJECT-CONTEXT-template.md). For the ARCHIVE_INDEX.txt format, see the [archive index template](../templates/mandated-files/archive-index.md).

---
*Part of [AI Project Architect](https://github.com/vbiroshak/ai-project-architect) — Version 4.11*
