# WORKFLOW.txt

Not a standalone template. WORKFLOW.txt is built by combining the [workflow section templates](../workflow-sections/) in prescribed order.

## Assembly

Title block at the top:

```
[PROJECT NAME] PROJECT WORKFLOW
Last updated: [Month DD, YYYY] (Session NNN)
Last reviewed: [Month DD, YYYY]
```

Sections follow in order, each with a `---` separator and ALL CAPS heading:

| # | Section | When to Include |
|---|---------|-----------------|
| 1 | Session Startup Procedure | always |
| 2 | Base Path | always |
| 3 | Tool Guides | always |
| 4 | What This Project Does | always (structure varies by tier) |
| 5 | Sub-Project Activation | always |
| 6 | Task Queue | only if the project uses one |
| 7 | Session Logs | always |
| 8 | Temporal Awareness | always |
| 9 | Inbox | always |
| 10 | Shared Knowledge Base | always (if running multiple projects) |
| 11 | Project Context | always |

Additional sections prescribed by patterns sit outside the numbered registry. The Archive section (prescribed by the [archive pattern](../../patterns/archive-pattern.md)) is added after Sub-Project Activation when the project archives its first sub-project.

Project-specific sections (2, 3, 4 file pointers, 10 entries) get filled with project content. All others use the template text verbatim.

---
*Part of [AI Project Architect](https://github.com/vbiroshak/ai-project-architect) — Version 4.3*
