#!/usr/bin/env python3
"""
Prepare the sources before the agent reads anything.  Run by a person, from the workspace folder:

    python tools/prepare-sources/prepare_sources.py

What it does (it never changes or deletes your source files):
  1. Measures every file in sources/ (size and number of lines), without the agent having to open it.
  2. Splits every file that is too large (default: over 200 KB or 3,000 lines) into logical parts with the
     split tool, so that NO part is over 150 KB or 2,500 lines. Files that changed since they were split are
     split again.
  3. Writes the inventory the agent must follow: brd-work/index/inventory.md (+ pages and inventory.json).
     The agent reads only the files the inventory lists as "read". Run this again whenever sources change.

Options:  --sources sources  --out brd-work/index  --large-kb 200  --large-lines 3000  --part-kb 150  --part-lines 2500
"""
import argparse
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "split-large-files"))
from split_export import split_file, SPLITTABLE  # noqa: E402

CONVERT = (".docx", ".doc", ".pdf", ".xlsx", ".xls", ".pptx", ".ppt", ".rtf", ".odt", ".png", ".jpg", ".jpeg",
           ".gif", ".bmp", ".tif", ".tiff", ".vsdx", ".msg", ".eml", ".zip")
PAGE_ROWS = 300


def count_lines(path):
    n, last = 0, b""
    with open(path, "rb") as f:
        while True:
            b = f.read(1 << 20)
            if not b:
                break
            n += b.count(b"\n")
            last = b[-1:]
    return n + (1 if last and last != b"\n" else 0)


def measure(path):
    return os.path.getsize(path), count_lines(path)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--sources", default="sources")
    ap.add_argument("--out", default=os.path.join("brd-work", "index"))
    ap.add_argument("--large-kb", type=int, default=200)
    ap.add_argument("--large-lines", type=int, default=3000)
    ap.add_argument("--part-kb", type=int, default=150)
    ap.add_argument("--part-lines", type=int, default=2500)
    a = ap.parse_args()
    if not os.path.isdir(a.sources):
        sys.exit(f"No '{a.sources}' folder here. Run this from the workspace folder (the one that holds sources/).")
    os.makedirs(a.out, exist_ok=True)
    large_b, part_b = a.large_kb * 1024, a.part_kb * 1024

    # 1. find originals (skip .parts folders, hidden files, README files)
    originals = []
    for root, dirs, files in os.walk(a.sources):
        dirs[:] = sorted(d for d in dirs if not d.startswith(".") and not d.endswith(".parts"))
        for fn in sorted(files):
            if fn.startswith(".") or fn.lower() in ("readme.txt", "readme.md"):
                continue
            originals.append(os.path.join(root, fn))

    rows, problems, split_now = [], [], []
    t0 = time.time()
    for p in originals:
        rel = os.path.relpath(p, ".").replace(os.sep, "/")
        ext = os.path.splitext(p)[1].lower()
        size, lines = measure(p)
        folder = rel.split("/")[1] if rel.count("/") >= 2 else ""
        big = size > large_b or lines > a.large_lines
        if ext in CONVERT:
            rows.append({"path": rel, "folder": folder, "kb": size // 1024, "lines": lines, "status": "convert first",
                         "note": "not readable by the agent: provide a Markdown or CSV version"})
            problems.append(rows[-1]); continue
        if not big:
            rows.append({"path": rel, "folder": folder, "kb": size // 1024, "lines": lines, "status": "read", "note": ""})
            continue
        if ext not in SPLITTABLE:
            rows.append({"path": rel, "folder": folder, "kb": size // 1024, "lines": lines, "status": "too large",
                         "note": f"type {ext or '(none)'} cannot be split: convert to .md/.csv/.json first"})
            problems.append(rows[-1]); continue
        # large and splittable: split (again if the original changed)
        pdir = p + ".parts"
        meta = os.path.join(pdir, ".split.json")
        st = os.stat(p)
        fresh = False
        if os.path.exists(meta):
            try:
                m = json.load(open(meta, encoding="utf-8"))
                fresh = (m.get("size") == st.st_size and m.get("mtime") == int(st.st_mtime)
                         and m.get("max_kb") == a.part_kb and m.get("max_lines") == a.part_lines)
            except Exception:
                fresh = False
        note = "split earlier, unchanged"
        if not fresh:
            try:
                r = split_file(p, a.part_kb, a.part_lines, force=True)
                note = f"split now into {r['parts']} parts" + (f" ({r['continued']} continue a large unit)" if r["continued"] else "")
                split_now.append(rel)
            except Exception as e:
                rows.append({"path": rel, "folder": folder, "kb": size // 1024, "lines": lines, "status": "too large",
                             "note": f"split failed: {e}"})
                problems.append(rows[-1]); continue
        rows.append({"path": rel, "folder": folder, "kb": size // 1024, "lines": lines,
                     "status": "split: do not read, read its parts", "note": note})
        # list the parts and the index; check every part is within the limits
        for fn in sorted(os.listdir(pdir)):
            if fn.startswith("."):
                continue
            pp = os.path.join(pdir, fn)
            prel = os.path.relpath(pp, ".").replace(os.sep, "/")
            ps, pl = measure(pp)
            if fn.endswith(".objects.csv"):
                status, pnote = "lookup: search only, do not read whole", "which part holds which object"
            elif fn.endswith(".index.md"):
                status, pnote = "read", f"split index of {os.path.basename(p)}"
            else:
                status, pnote = "read", f"part of {os.path.basename(p)}"
            if status == "read" and (ps > part_b + 4096 or pl > a.part_lines + 5):
                status, pnote = "too large", f"part over the limit ({ps//1024} KB, {pl} lines): report this"
                problems.append({"path": prel, "folder": folder, "kb": ps // 1024, "lines": pl, "status": status, "note": pnote})
            rows.append({"path": prel, "folder": folder, "kb": ps // 1024, "lines": pl, "status": status, "note": pnote})

    to_read = [r for r in rows if r["status"] == "read"]
    total_kb = sum(r["kb"] for r in to_read)
    total_lines = sum(r["lines"] for r in to_read)
    stamp = time.strftime("%Y-%m-%d %H:%M")

    json.dump({"generated": stamp, "limits": vars(a), "files": rows}, open(os.path.join(a.out, "inventory.json"), "w",
              encoding="utf-8"), indent=1)
    pages = [rows[i:i + PAGE_ROWS] for i in range(0, len(rows), PAGE_ROWS)] or [[]]
    for n, pg in enumerate(pages, 1):
        with open(os.path.join(a.out, f"inventory-{n:02d}.md"), "w", encoding="utf-8") as f:
            f.write(f"# Inventory page {n} of {len(pages)} (generated {stamp})\n\n| # | Path | KB | Lines | Status | Note |\n|---|---|---|---|---|---|\n")
            for i, r in enumerate(pg, (n - 1) * PAGE_ROWS + 1):
                f.write(f"| {i} | {r['path']} | {r['kb']} | {r['lines']} | {r['status']} | {r['note']} |\n")
            f.write("<!-- end of file -->\n")
    by_folder = {}
    for r in rows:
        d = by_folder.setdefault(r["folder"] or "(top)", {"read": 0, "split": 0, "other": 0, "kb": 0, "lines": 0})
        key = "read" if r["status"] == "read" else ("split" if r["status"].startswith("split") else "other")
        d[key] += 1
        if r["status"] == "read":
            d["kb"] += r["kb"]; d["lines"] += r["lines"]
    with open(os.path.join(a.out, "inventory.md"), "w", encoding="utf-8") as f:
        f.write(f"# Source inventory\n\nGenerated {stamp} by tools/prepare-sources/prepare_sources.py. "
                f"Run it again whenever sources change.\n\n")
        f.write("**Rules for the agent:** read only files whose status is `read`, each in full. Never open a file whose status "
                "is `split`, `lookup`, `convert first` or `too large`, and never open any file under sources/ that is not listed "
                "in the inventory pages: ask the user to run this script again instead.\n\n")
        f.write(f"- Source files found: {len(originals)}\n- Files and parts to read: {len(to_read)} "
                f"({total_kb:,} KB, {total_lines:,} lines)\n- Split into parts: {sum(1 for r in rows if r['status'].startswith('split'))}"
                f" (this run: {len(split_now)})\n- Problems: {len(problems)}\n- Limits: files over {a.large_kb} KB or "
                f"{a.large_lines} lines are split; no part over {a.part_kb} KB or {a.part_lines} lines\n"
                f"- Inventory pages: {len(pages)} (`inventory-01.md` …), {PAGE_ROWS} rows each\n\n")
        f.write("## By folder\n\n| Folder | To read | Split originals | Other | KB to read | Lines to read |\n|---|---|---|---|---|---|\n")
        for k, d in sorted(by_folder.items()):
            f.write(f"| {k} | {d['read']} | {d['split']} | {d['other']} | {d['kb']:,} | {d['lines']:,} |\n")
        f.write("\n## Problems (must be fixed before the build continues)\n\n")
        if problems:
            f.write("| Path | KB | Lines | Status | What to do |\n|---|---|---|---|---|\n")
            for r in problems:
                f.write(f"| {r['path']} | {r['kb']} | {r['lines']} | {r['status']} | {r['note']} |\n")
        else:
            f.write("None.\n")
        f.write("<!-- end of file -->\n")

    print(f"Sources: {len(originals)} files · to read: {len(to_read)} files/parts ({total_kb:,} KB) · "
          f"split this run: {len(split_now)} · problems: {len(problems)} · {time.time()-t0:.1f}s")
    print(f"Inventory: {os.path.join(a.out, 'inventory.md')}")
    for r in problems:
        print(f"  PROBLEM  {r['path']}: {r['status']} - {r['note']}")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
