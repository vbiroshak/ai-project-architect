# Sub-Project Archive Pattern

---

## The Problem

When a sub-project completes, its files become dead weight in the project root. They clutter the directory alongside active work, they get loaded by activation sequences that no longer apply, and there is no signal that the work is finished vs. dormant. Meanwhile the project needs to be able to reference completed work when it comes up in conversation.

Deleting is wrong (the historical record has value). Leaving in place is wrong (it obscures what is active). The project needs a pattern that freezes completed work, keeps it discoverable, and clears the root for what is live.

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

"Project Name - YYYY-MM" using the completion date only. Start dates are documented in session logs. Completion date is what you need at a glance: when did this wrap up. Sortable, unambiguous.

### Closing Before Archiving

Before moving a sub-project to Archive/, add a closing note to its status file. The note records: project completed, archive date, pointer to any successor project. This makes the archive self-documenting. Anyone who reads the archived status file understands why it stops where it does and where the remaining work went.

### Discoverability

Two layers ensure past work is findable:

1. **ARCHIVE_INDEX.txt** inside the Archive/ directory carries a brief inventory of archived sub-projects. A few lines per entry: what the project covered, when it completed, where it lives in Archive/, and key files inside it. This is the index. Future sessions check here when past work is referenced.

2. **The governing document** carries the archive convention in its sub-project activation section: completed work moves to Archive/, and ARCHIVE_INDEX.txt holds the inventory. This is the pointer. It ensures the archive is reachable from the standard startup path without adding to startup reads.

### Session Logs

Session logs stay at the project level. They span all sub-projects (past and present) and are shared infrastructure. They do not move into the archive with the sub-project they covered.

### Seeding a Successor

When remaining work from a completed sub-project becomes a new sub-project, seed it with clean, current data only. Do not copy stale files forward. Read each file against current state and session log history during the seeding process, carrying forward only what the new project actually needs. The new sub-project gets its own status file, task queue, and reference material built fresh.

---

## Design Rationale

**Why not Active/Closed folders?** Some projects use Active/ and Closed/ folders for lightweight, uniform items like cases or tickets. Sub-projects are large, structurally distinct bodies of work with their own reference files, task queues, and design artifacts. They do not share operational infrastructure. The Active/Closed pattern would leave completed sub-projects at root with only a status marker, cluttering the directory with work that will never be activated again.

**Why Archive/ at root?** Active sub-projects live at root. Completed ones live in Archive/. The root always shows only what is live plus one archive folder. This scales: future completed sub-projects drop into Archive/, future active ones appear at root.

**Why completion date only?** The start date is historical context found in session logs. The completion date is operational: it tells you how recent the archived work is at a glance. Including both creates unnecessarily long folder names.

---

## Known Issues

**Activation sequence maintenance:** When a sub-project is archived and a new one created, the governing document's sub-project activation section must be updated to point at the new sub-project. The old activation entry should be removed since archived sub-projects are read directly, not activated through the startup path.

**Archive size over time:** Projects with many completed sub-projects will accumulate large Archive/ directories. Not a practical concern at typical project scales. If it becomes one, ARCHIVE_INDEX.txt provides the index layer so Archive/ itself rarely needs to be listed.

---

## Implementation

The archive convention is carried in the governing document's sub-project activation section: see the [Chat template](../templates/workflow-sections/sub-project-activation.md) or the [Code template](../templates/claude-code/PROJECT-CONTEXT-template.md). For the ARCHIVE_INDEX.txt format, see the [archive index template](../templates/mandated-files/archive-index.md).

---
*Part of [AI Project Architect](https://github.com/vbiroshak/ai-project-architect) — Version 4.7*
