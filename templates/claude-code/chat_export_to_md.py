#!/usr/bin/env python3
"""
chat_export_to_md.py — convert Claude.ai Chat data-export .json transcripts
into readable collapsed-view .md files.

WHY THIS EXISTS
A Chat data export gives one .json per conversation. Each message stores the
turn TWICE: a flattened `text` field and a structured `content` array of typed
blocks. In the flattened `text` field the Claude app has ALREADY replaced every
tool_use / tool_result with the literal placeholder

    ```This block is not supported on your current device yet.```

So any converter that reads `text` inherits that placeholder and loses all tool
activity. The real data lives in the `content` blocks. This converter walks the
`content` array, so tool calls survive as one-line summaries.

FORMAT (collapsed view)
  Title line:   # {json name}
  (blank)
  Subtitle:     _Claude.ai chat, created {created_at} (collapsed view).
                The `.json` beside this file is the complete canonical record._
  (blank)
  Per message:  ## User   (sender == human)   |   ## Claude   (assistant)
                body = content blocks joined by blank lines:
                  text        -> verbatim, but skip if whitespace-only
                  thinking    -> "> _[reasoning]_" then each line blockquoted
                  tool_use    -> one-line summary
                  tool_result -> omitted
                  token_budget / unknown -> omitted
                attachments/files appended as marker lines
  File ends with a trailing newline.

HEADER PRESERVATION
If a .md already exists beside the .json, its header (everything up to the
first "## " line) is PRESERVED and only the body is regenerated. This keeps
any hand-cleaned titles intact.

USAGE
  python3 chat_export_to_md.py <dir>            # convert every *.json in <dir>
  python3 chat_export_to_md.py <file.json> ...  # convert specific files
  python3 chat_export_to_md.py <dir> --glob 'MyProject_*.json'

Each <name>.json writes/overwrites <name>.md beside it. The .json is never
modified. Verify after: there should be zero "This block is not supported"
strings in the output.
"""
import json
import os
import sys
import glob


def render_block(c):
    t = c.get("type")
    if t == "text":
        txt = c.get("text") or ""
        return txt if txt.strip() else None
    if t == "thinking":
        txt = c.get("thinking") or c.get("text") or ""
        if not txt.strip():
            return None
        lines = ["> " + l if l else "> " for l in txt.split("\n")]
        return "> _[reasoning]_\n" + "\n".join(lines)
    if t == "tool_use":
        return "→ " + (c.get("name") or "")
    return None


def render_body(d):
    o = []
    for m in d["chat_messages"]:
        o.append("## " + ("User" if m.get("sender") == "human" else "Claude"))
        o.append("")
        parts = []
        for c in m.get("content", []):
            r = render_block(c)
            if r is not None:
                parts.append(r)
        markers = []
        for a in (m.get("attachments") or []):
            markers.append("_(attachment: " + (a.get("file_name") or "?") + ")_")
        for f in (m.get("files") or []):
            markers.append("_(file: " + (f.get("file_name") or "?") + ")_")
        if markers:
            parts.append("\n".join(markers))
        o.append("\n\n".join(parts))
        o.append("")
    return "\n".join(o)


def generated_header(d):
    head = [
        "# " + (d.get("name") or ""),
        "",
        "_Claude.ai chat, created " + (d.get("created_at") or "") +
        " (collapsed view). The `.json` beside this file is the complete canonical record._",
        "",
    ]
    return "\n".join(head)


def existing_header(md_path):
    if not os.path.exists(md_path):
        return None
    lines = open(md_path).read().split("\n")
    for i, l in enumerate(lines):
        if l.startswith("## "):
            return "\n".join(lines[:i])
    return None


def convert_file(json_path):
    d = json.load(open(json_path))
    md_path = json_path[:-5] + ".md" if json_path.endswith(".json") else json_path + ".md"
    header = existing_header(md_path)
    if header is None:
        header = generated_header(d)
    out = header + "\n" + render_body(d) + "\n"
    open(md_path, "w").write(out)
    return md_path


def main(argv):
    if not argv:
        print(__doc__)
        return 1
    targets = []
    pattern = "*.json"
    args = [a for a in argv]
    if "--glob" in args:
        i = args.index("--glob")
        pattern = args[i + 1]
        del args[i:i + 2]
    for a in args:
        if os.path.isdir(a):
            targets.extend(sorted(glob.glob(os.path.join(a, pattern))))
        else:
            targets.append(a)
    if not targets:
        print("no .json targets found")
        return 1
    for t in targets:
        out = convert_file(t)
        print("wrote", out)
    print(f"done: {len(targets)} file(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
