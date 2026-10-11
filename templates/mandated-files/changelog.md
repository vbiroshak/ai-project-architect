# Changelog

Per project, optional. Running record of structural and infrastructure changes. Located at Project/CHANGELOG.txt.

Carries freshness lines. Updated whenever the project's structure or infrastructure changes.

## Structural Template

```
[PROJECT] — CHANGELOG
Last updated: [Month DD, YYYY] (Session NNN)
Last reviewed: [Month DD, YYYY]

Running record of structural and infrastructure changes to this project. One line per change, reverse chronological.

Infrastructure means things that shape how the project works as a workspace: governing document sections, mandated file conventions, directory structure, template text, and alignments to a new version of the architecture. Domain content is excluded — edits to session logs, handoffs, status files, task queues, sub-project reference files, and the actual work of the project do not go here. A good test: if the change would be identical across every project built on this architecture, it's infrastructure and belongs here. If it only makes sense in the context of this project's work, it's domain and doesn't.

Not a session log. Session logs hold narrative, reasoning, and process. This file holds the short factual record of what changed.

Current architecture version: [X.X]

---

YYYY-MM-DD — Session NNN — [What changed: dense and factual, not how it was decided.]
```

## Notes

The version line records the architecture version the project was built on or last aligned to. Update it when the project is brought to a newer version.

Entries are one line each, newest first, below the separator. A change made from outside the project (a coordinator project propagating a change, for example) cites that project's session rather than this one's.

---
*Part of [AI Project Architect](https://github.com/vbiroshak/ai-project-architect) — Version 4.11*
