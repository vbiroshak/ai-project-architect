#!/usr/bin/env python3
"""SessionStart hook — archives completed session transcripts into the project.

Claude Code stores raw transcripts as .jsonl files in ~/.claude/projects/<slug>/,
but that folder is ephemeral (cleaned up periodically) and the files are named by
UUID. This hook makes a permanent, human-readable copy in the project's Sessions/
directory every time a new session starts.

It copies every completed transcript (every .jsonl that is NOT the current session)
into your project's Workflow Files/Sessions/ folder. Opening a new session means
the previous one is finished, so the copy is always complete.

Naming: the hook looks for a declaration line in the opening human message, like
"This is [Project] 42" or "[Project] Session 42". If found, the file is saved as
[Project]_42.jsonl. If not found, the UUID filename is kept (nothing is lost).

Register in .claude/settings.json under hooks > SessionStart.

CUSTOMIZE: Change PROJECT_NAME below to match your project, and adjust the regex
patterns in NUM_PATTERNS if your sessions use a different declaration format.
Adjust SESSIONS_SUBDIR if your project keeps transcripts elsewhere.
"""
import json
import sys
import os
import re
import shutil
import glob

# --- CONFIGURATION ---
# The name used in your session declarations (e.g., "This is MyProject 15").
PROJECT_NAME = "Project"
# Where transcripts are saved, relative to the project root.
SESSIONS_SUBDIR = os.path.join("Workflow Files", "Sessions")
# --- END CONFIGURATION ---

# Patterns to extract the session number from the opening human message.
# Matches "This is Project 42" or "Project 42" (case-insensitive for "this is").
NUM_PATTERNS = [
    re.compile(r"[Tt]his is %s\s+(\d+(?:\.\d+)?)" % re.escape(PROJECT_NAME)),
    re.compile(r"\b%s\s+(\d+(?:\.\d+)?)\b" % re.escape(PROJECT_NAME)),
]


def session_num(path):
    """Extract the session number from the transcript's opening human message."""
    try:
        with open(path, encoding="utf-8", errors="replace") as f:
            for i, line in enumerate(f):
                if i > 60:
                    break
                try:
                    o = json.loads(line)
                except Exception:
                    continue
                if o.get("type") != "user":
                    continue
                c = o.get("message", {}).get("content")
                if isinstance(c, list):
                    txt = " ".join(
                        b.get("text", "") for b in c
                        if isinstance(b, dict) and b.get("type") == "text"
                    )
                elif isinstance(c, str):
                    txt = c
                else:
                    continue
                txt = txt.strip()
                if not txt or txt.startswith("<"):
                    continue
                for rx in NUM_PATTERNS:
                    m = rx.search(txt)
                    if m:
                        return m.group(1)
    except Exception:
        return None
    return None


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        data = {}
    transcript_path = data.get("transcript_path", "")
    session_id = data.get("session_id", "")
    cwd = data.get("cwd") or os.getcwd()

    # Locate the source transcript directory.
    if transcript_path:
        src_dir = os.path.dirname(os.path.realpath(transcript_path))
        current_base = os.path.basename(transcript_path)
    else:
        slug = re.sub(r"[^A-Za-z0-9]", "-", cwd)
        src_dir = os.path.expanduser(os.path.join("~/.claude/projects", slug))
        current_base = (session_id + ".jsonl") if session_id else ""

    # Destination directory (relative to the project root).
    # This script lives at .claude/hooks/, so project root is two levels up.
    code_root = os.path.realpath(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "..")
    )
    sessions_dir = os.path.join(code_root, SESSIONS_SUBDIR)
    os.makedirs(sessions_dir, exist_ok=True)

    if not os.path.isdir(src_dir):
        sys.exit(0)

    copied = []
    for src in sorted(glob.glob(os.path.join(src_dir, "*.jsonl"))):
        base = os.path.basename(src)
        if base == current_base:
            continue  # skip the current session (still being written)
        num = session_num(src)
        uuid_dst = os.path.join(sessions_dir, base)
        try:
            ssize = os.path.getsize(src)
            if num:
                fname = "%s_%s.jsonl" % (PROJECT_NAME, num)
                friendly = os.path.join(sessions_dir, fname)
                if os.path.exists(friendly) and os.path.getsize(friendly) >= ssize:
                    continue
                if os.path.exists(uuid_dst):
                    os.replace(uuid_dst, friendly)
                    if os.path.getsize(friendly) >= ssize:
                        copied.append(fname + " (named)")
                        continue
                shutil.copy2(src, friendly)
                copied.append(fname)
            else:
                if os.path.exists(uuid_dst) and os.path.getsize(uuid_dst) >= ssize:
                    continue
                shutil.copy2(src, uuid_dst)
                copied.append(base)
        except Exception:
            pass

    # Render readable Markdown versions if transcript-to-md.py is available.
    try:
        import importlib.util
        conv = os.path.join(os.path.dirname(os.path.realpath(__file__)), "transcript-to-md.py")
        if os.path.exists(conv):
            spec = importlib.util.spec_from_file_location("transcript_to_md", conv)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            for jp in glob.glob(os.path.join(sessions_dir, "*.jsonl")):
                mp = jp[:-6] + ".md"
                if (not os.path.exists(mp)) or os.path.getmtime(jp) > os.path.getmtime(mp):
                    mod.render(jp, mp)
    except Exception:
        pass

    if copied:
        print(json.dumps({"hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": "Archived transcript(s) to Sessions/: " + ", ".join(copied),
        }}))
    sys.exit(0)


if __name__ == "__main__":
    main()
