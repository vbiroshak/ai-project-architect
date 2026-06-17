#!/usr/bin/env python3
"""Render a Claude Code transcript (.jsonl) as a readable Markdown file.

The .jsonl is the canonical, complete record of the session. This script produces
a readable companion that shows the conversation in collapsed view: user and
assistant messages in full, reasoning blocks shown as blockquotes, and tool calls
as single summary lines (inputs and results are NOT expanded — they live in the
.jsonl for anyone who needs them).

Used by the archive-transcripts hook to generate .md files alongside each archived
.jsonl. Can also be run standalone:

    python3 transcript-to-md.py input.jsonl output.md [title]

The output is readable in any text editor, QuickLook, or rendered Markdown viewer.
"""
import json
import sys
import os


def tool_line(name, inp):
    """One-line summary of a tool call (collapsed view)."""
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
    return str(name)


def render_blocks(content):
    """Convert message content (str or list of blocks) into markdown strings."""
    out = []
    if isinstance(content, str):
        if content.strip():
            out.append(content.rstrip())
        return out
    if not isinstance(content, list):
        return out
    for blk in content:
        if not isinstance(blk, dict):
            continue
        t = blk.get("type")
        if t == "text":
            txt = blk.get("text", "")
            if txt.strip():
                out.append(txt.rstrip())
        elif t == "thinking":
            txt = (blk.get("thinking") or "").strip()
            if txt:
                out.append(
                    "> _[reasoning]_\n" + "\n".join("> " + ln for ln in txt.splitlines())
                )
        elif t == "tool_use":
            out.append("→ " + tool_line(blk.get("name", "?"), blk.get("input")))
        elif t == "tool_result":
            pass  # collapsed: results stay in the .jsonl
    return out


def _has_text(content):
    if isinstance(content, str):
        return bool(content.strip())
    if isinstance(content, list):
        return any(
            isinstance(b, dict) and b.get("type") == "text" and b.get("text", "").strip()
            for b in content
        )
    return False


def render(jsonl_path, md_path, title=None):
    """Render a .jsonl transcript to a readable .md file."""
    title = title or os.path.splitext(os.path.basename(jsonl_path))[0]
    lines = [
        "# %s" % title,
        "",
        (
            "_Readable rendering of `%s` (collapsed view). "
            "The `.jsonl` beside it is the complete canonical record._"
        ) % os.path.basename(jsonl_path),
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
            m = o.get("message")
            if not isinstance(m, dict):
                continue
            content = m.get("content")
            blocks = render_blocks(content)
            if not blocks:
                continue
            role = m.get("role", o.get("type"))
            if role == "assistant":
                header = "## Assistant"
            elif _has_text(content):
                header = "## Human"
            else:
                continue
            lines.append(header)
            lines.append("")
            lines.append("\n\n".join(blocks))
            lines.append("")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    return md_path


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.stderr.write("usage: transcript-to-md.py <input.jsonl> <output.md> [title]\n")
        sys.exit(1)
    render(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else None)
