# Templates

Deployable templates for building and maintaining workspaces. Each template contains the exact text or structural pattern to use in your project files.

Two categories:

**[Workflow Sections](workflow-sections/)** — The sections that make up WORKFLOW.txt. Universal sections are deployed verbatim; project-specific sections show the structure with fill-in areas. See the [WORKFLOW Section Registry](../workspace-architecture.md#workflow-section-registry) in the architecture document for the prescribed order and descriptions.

- [Session Startup Procedure](workflow-sections/session-startup-procedure.md) — universal
- [Base Path](workflow-sections/base-path.md) — project-specific
- [What This Project Does](workflow-sections/what-this-project-does.md) — project-specific
- [Sub-Project Activation](workflow-sections/sub-project-activation.md) — universal pattern, file pointers vary
- [Task Queue](workflow-sections/task-queue.md) — optional
- [Session Logs](workflow-sections/session-logs.md) — universal
- [Temporal Awareness](workflow-sections/temporal-awareness.md) — universal
- [Inbox](workflow-sections/inbox.md) — universal
- [Shared Knowledge Base](workflow-sections/shared-knowledge-base.md) — universal (multi-project)
- [Project Context](workflow-sections/project-context.md) — project-specific
- [Archive](workflow-sections/archive.md) — optional

**[Mandated Files](mandated-files/)** — Structural templates for the files prescribed by the architecture. Some contain canonical text (project instructions), others show the prescribed structure and format conventions.

- [Project Instructions](mandated-files/project-instructions.md) — canonical text, path is only variable
- [WORKFLOW](mandated-files/workflow.md) — assembly instructions
- [HANDOFF](mandated-files/handoff.md) — structural template
- [REFERENCE](mandated-files/reference.md) — structural template
- [Status File](mandated-files/status-file.md) — per sub-project
- [Index File](mandated-files/index-file.md) — per collection folder
- [Lessons Index](mandated-files/lessons-index.md) — operational knowledge routing
- [Tasks](mandated-files/tasks.md) — active items queue
- [Archive Index](mandated-files/archive-index.md) — archived sub-project inventory
