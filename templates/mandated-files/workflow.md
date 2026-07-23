# WORKFLOW.txt (Chat)

Not a standalone template. WORKFLOW.txt is the governing document for Chat projects, built by combining the [workflow section templates](../workflow-sections/) in prescribed order. Code projects use PROJECT_CONTEXT.md instead — see the [Code PROJECT_CONTEXT template](../claude-code/PROJECT-CONTEXT-template.md).

## Assembly

Title block at the top:

```
[PROJECT NAME] PROJECT WORKFLOW
Last updated: [Month DD, YYYY] (Session NNN)
Last reviewed: [Month DD, YYYY]
```

In coordinated multi-project setups (see The Coordinator Project in the architecture doc), a propagated-sections paragraph follows the title block, with the section list matching what the coordinator actually maintains in this document:

```
Sections maintained by the coordinator project and updated by propagation: [SECTION NAMES]. Don't edit them locally, even to apply a correction from the user — route corrections to the coordinator's inbox. Every other section is this project's own.
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
| 8 | Handoff | always |
| 9 | Temporal Awareness | always |
| 10 | Inbox | always |
| 11 | Shared Knowledge Base | always (if running multiple projects) |
| 12 | Project Context | always |

Project-specific sections (2, 4 file pointers, 5 pointers, 12 entries) get filled with project content. All others use the template text verbatim.

---
*Part of [AI Project Architect](https://github.com/vbiroshak/ai-project-architect) — Version 4.7*
