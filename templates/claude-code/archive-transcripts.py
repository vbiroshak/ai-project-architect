"""SessionStart hook: archive and render session transcripts.

Copies completed session transcripts from Claude Code's internal storage to the
project's transcript directory, then renders each .jsonl to a readable .md file.

Runs at the start of every session and copies every COMPLETED transcript (everything
except the current session). Opening a new session means the previous one is finished,
so the copy is always complete.

Naming priority: numbered custom-title (/rename) → numbered text pattern ("This is X N")
→ free-form custom-title → UUID. Sanitizes titles for filesystem safety.

Copies only; never deletes a source transcript.
"""

import json, sys, os, re, shutil, glob

PROJECT_NAME = ""

NAME_NUM_RE = re.compile(r"^([\w-]+)\s+(\d+(?:\.\d+)?)$")
TEXT_PATTERN_RE = re.compile(r"^[Tt]his is ([\w-]+)\s+(\d+(?:\.\d+)?)")


def load_config(config_path):
    try:
        with open(config_path) as f:
            return json.load(f)
    except Exception:
        return {}


def sanitize_filename(name):
    name = re.sub(r'[<>:"/\\|?*]', '', name)
    name = name.strip('. ')
    if not name:
        return None
    if len(name) > 200:
        name = name[:200]
    return name


def format_numbered(name, num_str, project_name, project_name_tier):
    """Format a name+number into ProjectName_NNNN, applying casing normalization."""
    if project_name:
        if name.lower() == project_name.lower():
            name = project_name
    if num_str.isdigit():
        num_str = "%04d" % int(num_str)
    return "%s_%s" % (name, num_str)


def custom_title_from_transcript(path):
    """Extract the last custom-title from a transcript. Returns (name, number) tuple for numbered titles, plain string for free-form, or None."""
    last_title = None
    try:
        with open(path, encoding="utf-8", errors="replace") as f:
            for line in f:
                line = line.strip()
                if not line or "custom-title" not in line:
                    continue
                try:
                    o = json.loads(line)
                except Exception:
                    continue
                if o.get("type") == "custom-title":
                    title = o.get("customTitle", "").strip()
                    if title:
                        last_title = title
    except Exception:
        pass
    if not last_title:
        return None
    m = NAME_NUM_RE.match(last_title)
    if m:
        return (m.group(1), m.group(2))
    safe = sanitize_filename(last_title)
    return safe if safe else None


def text_pattern_from_transcript(path):
    """Scan the first user message for 'This is ProjectName N'. Returns (name, number) tuple or None."""
    try:
        with open(path, encoding="utf-8", errors="replace") as f:
            for i, line in enumerate(f):
                if i > 60:
                    break
                try:
                    o = json.loads(line.strip())
                except Exception:
                    continue
                if o.get("type") != "user":
                    continue
                c = o.get("message", {}).get("content")
                if isinstance(c, list):
                    txt = " ".join(b.get("text", "") for b in c if isinstance(b, dict) and b.get("type") == "text")
                elif isinstance(c, str):
                    txt = c
                else:
                    continue
                txt = txt.strip()
                if not txt or txt.startswith("<"):
                    continue
                # Only the first real user message counts as the opener.
                m = TEXT_PATTERN_RE.search(txt)
                return (m.group(1), m.group(2)) if m else None
    except Exception:
        pass
    return None


def transcript_session_id(path):
    """Read the sessionId from the first records of a transcript. Returns the id string or None."""
    try:
        with open(path, encoding="utf-8", errors="replace") as f:
            for i, line in enumerate(f):
                if i > 20:
                    break
                try:
                    o = json.loads(line.strip())
                except Exception:
                    continue
                sid = o.get("sessionId")
                if sid:
                    return sid
    except Exception:
        pass
    return None


def resolve_transcripts_dir(config, project_dir):
    """Resolve the transcript directory, relative to project_dir."""
    if config.get("transcripts_dir"):
        return config["transcripts_dir"]
    if os.path.isdir(os.path.join(project_dir, "Project", "Sessions")):
        return "Project/Sessions"
    if os.path.isdir(os.path.join(project_dir, "Sessions")):
        return "Sessions"
    return "recall/sessions"


def resolve_project_name(config, project_dir):
    """Resolve project name and its authority tier. Returns (name, tier) where tier 1-2 are authoritative, tier 3 is inferred."""
    name = config.get("project_name", "")
    if name:
        return (name, 1)
    if PROJECT_NAME:
        return (PROJECT_NAME, 2)
    basename = os.path.basename(project_dir)
    if basename:
        return (basename, 3)
    return ("", 4)


def resolve_filename(src, project_name, project_name_tier):
    """Determine the archive filename for a transcript. Returns the filename stem (without .jsonl) or None for UUID."""
    ct = custom_title_from_transcript(src)
    tp = text_pattern_from_transcript(src)

    # Tier 1: numbered custom-title
    if isinstance(ct, tuple):
        name, num = ct
        return format_numbered(name, num, project_name, project_name_tier)

    # Tier 2: numbered text-pattern
    if isinstance(tp, tuple):
        cap_name, num = tp
        if project_name_tier in (1, 2):
            if cap_name.lower() != project_name.lower():
                tp = None
            else:
                cap_name = project_name
        elif project_name_tier == 3:
            if cap_name.lower() == project_name.lower():
                cap_name = project_name
        if tp is not None:
            return format_numbered(cap_name, num, project_name, project_name_tier)

    # Tier 3: free-form custom-title
    if isinstance(ct, str):
        return ct

    # Tier 4: UUID
    return None


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        data = {}

    project_dir = data.get("cwd") or os.getcwd()
    config = load_config(os.path.join(project_dir, "recall", "config.json"))
    transcripts_dir_rel = resolve_transcripts_dir(config, project_dir)
    project_name, project_name_tier = resolve_project_name(config, project_dir)

    transcript_path = data.get("transcript_path", "")
    session_id = data.get("session_id", "")

    if transcript_path:
        src_dir = os.path.dirname(os.path.realpath(transcript_path))
        current_base = os.path.basename(transcript_path)
    else:
        slug = re.sub(r"[^A-Za-z0-9]", "-", project_dir)
        src_dir = os.path.expanduser(os.path.join("~/.claude/projects", slug))
        current_base = (session_id + ".jsonl") if session_id else ""

    sessions_dir = os.path.join(project_dir, transcripts_dir_rel)
    os.makedirs(sessions_dir, exist_ok=True)

    if not os.path.isdir(src_dir):
        sys.exit(0)

    sources = sorted(glob.glob(os.path.join(src_dir, "*.jsonl")))

    if not current_base and sources:
        # No session identity from stdin — guard against copying the live transcript.
        current_base = os.path.basename(max(sources, key=os.path.getmtime))

    copied = []
    conflicts = []
    for src in sources:
        base = os.path.basename(src)
        if base == current_base:
            continue

        stem = resolve_filename(src, project_name, project_name_tier)
        uuid_dst = os.path.join(sessions_dir, base)

        try:
            ssize = os.path.getsize(src)
            if stem:
                fname = stem + ".jsonl"
                friendly = os.path.join(sessions_dir, fname)
                if os.path.exists(friendly):
                    # A different session already archived under this name is a
                    # naming conflict — preserve the existing archive and report.
                    src_sid = transcript_session_id(src)
                    dst_sid = transcript_session_id(friendly)
                    if src_sid and dst_sid and src_sid != dst_sid:
                        conflicts.append(fname)
                        continue
                    if os.path.getsize(friendly) >= ssize:
                        continue
                if os.path.exists(uuid_dst):
                    os.replace(uuid_dst, friendly)
                    uuid_md = uuid_dst[:-6] + ".md"
                    if os.path.exists(uuid_md):
                        os.replace(uuid_md, friendly[:-6] + ".md")
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

    # Render readable .md beside each archived .jsonl
    try:
        import importlib.util
        conv = os.path.join(os.path.dirname(os.path.abspath(__file__)), "transcript_to_md.py")
        spec = importlib.util.spec_from_file_location("transcript_to_md", conv)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        for jp in glob.glob(os.path.join(sessions_dir, "*.jsonl")):
            mp = jp[:-6] + ".md"
            if (not os.path.exists(mp)) or os.path.getmtime(jp) > os.path.getmtime(mp):
                mod.render(jp, mp)
    except Exception:
        pass

    notes = []
    if copied:
        notes.append("Archived transcript(s): " + ", ".join(copied))
    if conflicts:
        notes.append(
            "NAMING CONFLICT — not archived (a different session is already archived under this name; "
            "renumber one of them with /rename, it will archive at the next session start): "
            + ", ".join(conflicts)
        )
    if notes:
        print(json.dumps({"hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": " ".join(notes),
        }}))
    sys.exit(0)


if __name__ == "__main__":
    main()

# Version 4.6
