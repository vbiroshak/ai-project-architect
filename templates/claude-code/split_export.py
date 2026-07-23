#!/usr/bin/env python3
"""
split_export.py — split a Claude.ai bulk data export into individual
per-project conversation .json files, named for migration.

THE PROBLEM
Anthropic's data export bundles ALL conversations across ALL projects into
a single conversations.json file. Projects are listed separately in
projects/*.json but do NOT reference their conversations, and conversations
do NOT carry a project_uuid. The only way to associate a conversation with
a project is by its content — the conversation `name` field or the opener
message text.

WHAT THIS DOES
Reads conversations.json from a data-export batch directory. For each
conversation, identifies its project from the `name` field (pattern:
"ProjectName N"). Writes each conversation as an individual .json file
into a staging directory organized by project, named with the 4-digit
convention (e.g., MyProject_0042.json).

The individual .json files have the same structure as one conversation
from the bulk export (uuid, name, summary, created_at, updated_at,
account, chat_messages). chat_export_to_md.py can then convert each
to a readable .md.

NAMING
The conversation name "MyProject 42" becomes MyProject_0042.json. The number is
extracted from the name. Conversations with decimal-style names
(e.g., "MyProject 1.0") are reported as warnings and skipped.

SETUP
Edit the KNOWN_PROJECTS list below with YOUR project names. The script
matches conversations whose name field follows the pattern
"ProjectName N" (e.g., "MyProject 42", "OtherProject 1").

USAGE
  python3 split_export.py <batch-dir> <output-dir> [--project MyProject] [--dry-run]

On Windows, invoke with python instead of python3.

  <batch-dir>   the data-export batch directory containing conversations.json
  <output-dir>  where to write the per-project directories

  --project X   process only project X (can be repeated)
  --dry-run     report what would be written without writing
  --include-unnamed   also write unnamed/unmatched conversations to _unmatched/

OUTPUT STRUCTURE
  <output-dir>/
    MyProject/
      MyProject_0001.json
      MyProject_0002.json
      ...
    OtherProject/
      OtherProject_0001.json
      ...
    _unmatched/         (only with --include-unnamed)
      unmatched_001.json
      ...
    _duplicates/        (conversations whose number collides with one already
      ...                written — quarantined for manual resolution)
    manifest.txt        summary of what was written
"""
import json
import os
import re
import sys


# EDIT THIS LIST with your project names — these must match the names
# as they appear in your Claude.ai conversation titles (e.g., "MyProject 42"
# means "MyProject" should be in this list).
KNOWN_PROJECTS = [
    "MyProject",
    # Add your project names here
]

NAME_RE = re.compile(
    r"^(" + "|".join(re.escape(p) for p in KNOWN_PROJECTS) + r")\s+(\d+)$"
)


def identify_project(convo):
    name = convo.get("name", "").strip()
    if not name:
        return None, None
    m = NAME_RE.match(name)
    if m:
        return m.group(1), int(m.group(2))
    m2 = re.match(
        r"^(" + "|".join(re.escape(p) for p in KNOWN_PROJECTS) + r")\s+(\d+\.\d+)",
        name,
    )
    if m2:
        return m2.group(1), None
    return None, None


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 1

    batch_dir = argv[0]
    output_dir = argv[1]
    filter_projects = []
    dry_run = False
    include_unnamed = False

    i = 2
    while i < len(argv):
        if argv[i] == "--project" and i + 1 < len(argv):
            filter_projects.append(argv[i + 1])
            i += 2
        elif argv[i] == "--dry-run":
            dry_run = True
            i += 1
        elif argv[i] == "--include-unnamed":
            include_unnamed = True
            i += 1
        else:
            print(f"unknown argument: {argv[i]}")
            return 1

    conv_path = os.path.join(batch_dir, "conversations.json")
    if not os.path.exists(conv_path):
        print(f"not found: {conv_path}")
        return 1

    with open(conv_path, encoding="utf-8") as f:
        convos = json.load(f)
    print(f"loaded {len(convos)} conversations from {conv_path}")

    by_project = {}
    decimal_warnings = []
    unmatched = []

    for c in convos:
        project, num = identify_project(c)
        if project and num is not None:
            if filter_projects and project not in filter_projects:
                continue
            by_project.setdefault(project, []).append((num, c))
        elif project and num is None:
            decimal_warnings.append((project, c.get("name", ""), c.get("uuid", "")))
        else:
            unmatched.append(c)

    for project in by_project:
        by_project[project].sort(key=lambda x: x[0])

    print()
    for project in sorted(by_project):
        nums = [n for n, _ in by_project[project]]
        print(f"  {project}: {len(nums)} conversations (#{min(nums)}-#{max(nums)})")
        expected = set(range(min(nums), max(nums) + 1))
        missing = expected - set(nums)
        if missing:
            print(f"    WARNING: missing numbers: {sorted(missing)}")
        from collections import Counter
        dupes = [n for n, count in Counter(nums).items() if count > 1]
        if dupes:
            print(f"    WARNING: duplicate numbers: {sorted(dupes)}")

    if decimal_warnings:
        print(f"\n  {len(decimal_warnings)} decimal-named conversations (skipped):")
        for proj, name, uuid in decimal_warnings:
            print(f"    {proj}: {name}")

    print(f"\n  {len(unmatched)} unmatched conversations")

    if dry_run:
        print("\n--dry-run: nothing written")
        return 0

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    manifest_lines = []
    total_written = 0

    total_duplicates = 0

    for project in sorted(by_project):
        proj_dir = os.path.join(output_dir, project)
        os.makedirs(proj_dir, exist_ok=True)
        written_nums = set()
        for num, c in by_project[project]:
            if num in written_nums:
                # Duplicate number: quarantine for manual resolution rather than
                # silently overwriting the conversation already written.
                dup_dir = os.path.join(output_dir, "_duplicates")
                os.makedirs(dup_dir, exist_ok=True)
                filename = f"{project}_{num:04d}_{c.get('uuid', '')[:8]}.json"
                filepath = os.path.join(dup_dir, filename)
                with open(filepath, "w", encoding="utf-8") as f:
                    json.dump(c, f, indent=2, ensure_ascii=False)
                manifest_lines.append(
                    f"{filename}  {c.get('created_at', '')[:10]}  {c.get('name', '')}  DUPLICATE NUMBER — resolve manually"
                )
                total_duplicates += 1
                continue
            written_nums.add(num)
            filename = f"{project}_{num:04d}.json"
            filepath = os.path.join(proj_dir, filename)
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(c, f, indent=2, ensure_ascii=False)
            manifest_lines.append(
                f"{filename}  {c.get('created_at', '')[:10]}  {c.get('name', '')}"
            )
            total_written += 1

    if include_unnamed and unmatched:
        un_dir = os.path.join(output_dir, "_unmatched")
        os.makedirs(un_dir, exist_ok=True)
        for i, c in enumerate(unmatched, 1):
            filename = f"unmatched_{i:03d}.json"
            filepath = os.path.join(un_dir, filename)
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(c, f, indent=2, ensure_ascii=False)
            manifest_lines.append(
                f"{filename}  {c.get('created_at', '')[:10]}  {c.get('name', '')}"
            )
            total_written += 1

    manifest_path = os.path.join(output_dir, "manifest.txt")
    with open(manifest_path, "w", encoding="utf-8") as f:
        f.write("\n".join(manifest_lines) + "\n")

    print(f"\nwrote {total_written} files to {output_dir}")
    if total_duplicates:
        print(f"QUARANTINED {total_duplicates} duplicate-numbered conversation(s) to _duplicates/ — resolve manually before placing")
    print(f"manifest: {manifest_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

# Version 4.7
