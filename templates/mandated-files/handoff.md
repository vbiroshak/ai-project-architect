# HANDOFF.txt

Startup orientation file. Overwritten with each session log (paired writes). Controls what context loads at activation. Target size: under 2 KB.

## Structural Template

```
[PROJECT] HANDOFF
Last updated: [date] (Session NNN)
Last reviewed: [date]

---
SESSION [NNN] — [BRIEF TITLE]

[Most recent session or session group. Key decisions, file changes, current state.]

ACTIVATION CONTEXT:
  Read: [Session log(s) to load]
  [Label]: [Status file, work plan, or other relevant file]

---
[EFFORT OR TOPIC] — [STATUS PHRASE]

[Current state of an active effort. What's next, decisions pending. One section per active effort needing its own context.]

---
KNOWN FIXES NEEDED

[Corrections or cleanup discovered but not yet addressed. Remove when fixed.]

---
OTHER PENDING

[Open items not tied to an effort section above.]

---
SESSION CONTEXT

Session NNN: [Compressed summary]
Session NNN: [Compressed summary]

---
FOR DEPTH

Sessions NNN-NNN — [Topic area]
Session NNN — [Topic]
```

## Notes

Sections are situational. A fresh project may have only the session summary and activation context. Other sections appear as needed and disappear when resolved.

SESSION CONTEXT carries compressed summaries of recent sessions (typically 3-5). Older sessions roll off or get absorbed into FOR DEPTH.

ACTIVATION CONTEXT scales to complexity: one session log for lightweight efforts, a work plan plus status file plus log range for complex ones.
