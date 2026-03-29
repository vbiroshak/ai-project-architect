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
| 3 | What This Project Does | always (structure varies by tier) |
| 4 | Sub-Project Activation | always |
| 5 | Task Queue | only if the project uses one |
| 6 | Session Logs | always |
| 7 | Temporal Awareness | always |
| 8 | Inbox | always |
| 9 | Shared Knowledge Base | always (if running multiple projects) |
| 10 | Project Context | always |
| 11 | Archive | when archived sub-projects exist |

Project-specific sections (2, 3, 4 file pointers, 10 entries) get filled with project content. All others use the template text verbatim.

Target size: 4-6 KB assembled.
