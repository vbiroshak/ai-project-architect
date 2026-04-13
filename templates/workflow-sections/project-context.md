# Project Context

WORKFLOW section — project-specific, universal preamble with entries that vary.

## Template Text

```
---
PROJECT CONTEXT

Project-specific context and preferences not covered by account-wide user preferences. Do not duplicate system-level preferences.

When the user corrects a project-specific behavior, write it here immediately and mention it.

Current context:

  FILE DELETION: The AI cannot delete files. Move to Inbox/ with "DELETE ME" at the front. Give the user a heads up.

  FACTUAL GROUNDING: For verifiable claims in this project's domain (such as [domain-specific examples]), verify via search rather than relying on training data or assumptions.

  [Additional project-specific entries accumulate here through use]
```

## Notes

The preamble (first three lines through "mention it.") and the FILE DELETION seed entry are universal. FACTUAL GROUNDING uses a domain-specific template (see [Factual Grounding](../../workspace-architecture.md#factual-grounding) in the architecture document). All other entries are project-specific and accumulate over time.

---
*Part of [AI Project Architect](https://github.com/vbiroshak/ai-project-architect) — Version 4.2*
