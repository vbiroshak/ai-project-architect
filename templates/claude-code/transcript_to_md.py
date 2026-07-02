# Render a Claude Code transcript (.jsonl) as a human- and Claude-readable Markdown file.
#
# The .jsonl stays the canonical, complete record; this .md is the readable companion (open in
# QuickLook / TextEdit). It mirrors the chat UI's COLLAPSED view: User and AI messages in full,
# AI reasoning shown, and each tool call as a single summary line — the tool's inputs and results
# are NOT expanded here (they live complete in the .jsonl). That keeps the readable view legible.
import json, sys, os, re
from datetime import datetime, timezone


def tool_line(name, inp):
    """One-line summary of a tool call, mirroring the collapsed chat-UI label."""
    d = inp if isinstance(inp, dict) else {}

    def base(key):
        v = d.get(key) or ""
        return os.path.basename(v) if isinstance(v, str) and v else (v or "")

    if name == "Read":
        return "Read `%s`" % base("file_path")
    if name in ("Edit", "MultiEdit"):
        return "Edited `%s`" % base("file_path")
    if name == "Write":
        return "Wrote `%s`" % base("file_path")
    if name == "NotebookEdit":
        return "Edited notebook `%s`" % base("notebook_path")
    if name == "Bash":
        return "Ran: %s" % (d.get("description") or str(d.get("command") or "")[:70])
    if name == "Grep":
        return "Searched: `%s`" % (d.get("pattern") or "")
    if name == "Glob":
        return "Globbed: `%s`" % (d.get("pattern") or "")
    if name in ("Agent", "Task"):
        return "Launched agent: %s" % (d.get("description") or d.get("subagent_type") or "")
    if name == "WebFetch":
        return "Fetched: %s" % (d.get("url") or "")
    if name == "WebSearch":
        return "Web search: %s" % (d.get("query") or "")
    if name == "ToolSearch":
        return "Tool search: %s" % (d.get("query") or "")
    if name == "TodoWrite":
        return "Updated todo list"
    return str(name)



# Blocks the chat UI never shows the user — removed entirely.
_REMOVE_RES = [
    re.compile(r"<task-notification>.*?</task-notification>", re.DOTALL),
    re.compile(r"<system-reminder>.*?</system-reminder>", re.DOTALL),
    re.compile(r"<local-command-caveat>.*?</local-command-caveat>", re.DOTALL),
    re.compile(r"<command-name>.*?</command-name>", re.DOTALL),
    re.compile(r"<command-message>.*?</command-message>", re.DOTALL),
    re.compile(r"<command-args>.*?</command-args>", re.DOTALL),
]
_STDOUT_RE = re.compile(r"<local-command-stdout>(.*?)</local-command-stdout>", re.DOTALL)


def _strip_system_tags(text):
    """Make a turn's text match the chat UI: unwrap command output to its plain text
    (so a /model switch reads 'Set model to ...'), and remove blocks the UI never shows
    (task notifications, system reminders, the raw command-invocation tags)."""
    text = _STDOUT_RE.sub(lambda m: m.group(1), text)  # keep the visible "Set model to ..." line
    for rx in _REMOVE_RES:
        text = rx.sub("", text)
    return text.strip()


def render_blocks(content):
    """content is a str or a list of blocks; return a list of markdown strings."""
    out = []
    if isinstance(content, str):
        cleaned = _strip_system_tags(content)
        if cleaned:
            out.append(cleaned.rstrip())
        return out
    if not isinstance(content, list):
        return out
    for blk in content:
        if not isinstance(blk, dict):
            continue
        t = blk.get("type")
        if t == "text":
            txt = _strip_system_tags(blk.get("text", ""))
            if txt:
                out.append(txt.rstrip())
        elif t == "thinking":
            txt = (blk.get("thinking") or "").strip()
            if txt:  # only present if showThinkingSummaries surfaced a summary; redacted (empty) by default
                out.append("> _[reasoning]_\n" + "\n".join("> " + ln for ln in txt.splitlines()))
        elif t == "tool_use":
            out.append("→ " + tool_line(blk.get("name", "?"), blk.get("input")))
        elif t == "tool_result":
            pass  # collapsed view: the result is in the .jsonl, not the readable .md
    return out


def _format_timestamp(ts_str):
    """Format an ISO timestamp string for display in turn headers."""
    if not ts_str:
        return None
    try:
        dt = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
        local = dt.astimezone()
        return local.strftime("%Y-%m-%d %H:%M %Z")
    except (ValueError, TypeError):
        return None


def _has_text(content):
    if isinstance(content, str):
        return bool(_strip_system_tags(content))
    if isinstance(content, list):
        return any(isinstance(b, dict) and b.get("type") == "text" and _strip_system_tags(b.get("text", "")) for b in content)
    return False


def render(jsonl_path, md_path, title=None):
    title = title or os.path.splitext(os.path.basename(jsonl_path))[0]
    lines = [
        "# %s" % title,
        "",
        "_Readable rendering of `%s` (collapsed view). The `.jsonl` beside it is the complete canonical record — full tool inputs and results._" % os.path.basename(jsonl_path),
        "",
    ]
    with open(jsonl_path, "r", encoding="utf-8", errors="replace") as f:
        for raw in f:
            raw = raw.strip()
            if not raw:
                continue
            try:
                o = json.loads(raw)
            except Exception:
                continue
            if o.get("type") not in ("user", "assistant"):
                continue
            if o.get("isMeta"):
                continue  # system-injected content (skill loads, etc.) — not visible in chat UI
            m = o.get("message")
            if not isinstance(m, dict):
                continue
            content = m.get("content")
            blocks = render_blocks(content)
            if not blocks:
                continue
            role = m.get("role", o.get("type"))
            if role == "assistant":
                label = "Claude"
            elif _has_text(content):
                label = "User"
            else:
                continue  # a user record carrying only tool results — nothing to show collapsed
            ts = _format_timestamp(o.get("timestamp") or o.get("created_at") or o.get("ts"))
            header = "## %s — %s" % (label, ts) if ts else "## %s" % label
            lines.append(header)
            lines.append("")
            lines.append("\n\n".join(blocks))
            lines.append("")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    return md_path


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.stderr.write("usage: transcript_to_md.py <in.jsonl> <out.md> [title]\n")
        sys.exit(1)
    render(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else None)

# Version 4.6
