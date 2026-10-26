#!/usr/bin/env python3
"""
Split a large source file into logical parts the agent can read safely.

Normally you do not run this directly: tools/prepare-sources/prepare_sources.py measures every
source file and calls this for every file that is too large. You can also run it on one file:

    python split_export.py <file> [--max-kb 150] [--max-lines 2500] [--force]

Output: a folder "<file>.parts/" next to the file with the parts, a short index "<stem>.index.md",
(CSV) an object lookup "<stem>.objects.csv" (for searching, not reading), and ".split.json"
(what was split, so prepare_sources.py can tell when the original changes). The original is never changed.

HARD LIMIT: no part is ever larger than --max-kb or longer than --max-lines.

Logical units, kept together whenever they fit:
  CSV        one object (schema + object): all its rows, in order (code exports: all chunks of one object)
  Markdown   one section under a level-1 or level-2 heading
  JSON       one item of the main list (one job or pipeline)
Grouping: CSV by schema, then business group (usp_rebate_calc -> rebate); Markdown by chapter; JSON in order.
A part never mixes two schemas (CSV) or two chapters (Markdown).

A unit too big for one part is split at the most natural point available and marked
"continued" in the index:
  CSV        between rows (a row is never cut; a single cell too large goes to a .txt side file)
  Markdown   at lower headings (### …), then between paragraphs, then between lines
  JSON       the item is written as indented text and split between lines (.txt parts)
"""
import argparse
import csv
import json
import os
import re
import shutil
import sys
from collections import OrderedDict

SCHEMA_COLS = ["schema_name", "table_schema", "specific_schema", "volume_schema", "referencing_schema",
               "source_schema", "object_schema"]
OBJECT_COLS = ["object_name", "table_name", "procedure_name", "routine_name", "specific_name",
               "referencing_object", "referencing_entity_name", "job_name", "pipeline_name", "name"]
PREFIXES = ["usp_", "sp_", "proc_", "p_", "vw_", "v_", "fn_", "f_", "udf_", "tvf_", "tbl_", "t_", "tr_", "trg_",
            "dim_", "fact_", "fct_", "stg_", "stage_", "rpt_", "tmp_", "ref_", "lkp_", "map_", "hist_", "load_", "etl_"]
SPLITTABLE = (".csv", ".md", ".markdown", ".txt", ".json")


# ---------------------------------------------------------------- helpers
def read_text(path):
    """Read a text file whatever its encoding (UTF-8 with or without BOM, UTF-16, Windows-1252)."""
    raw = open(path, "rb").read()
    if raw.startswith(b"\xff\xfe") or raw.startswith(b"\xfe\xff"):
        return raw.decode("utf-16")
    for enc in ("utf-8-sig", "cp1252"):
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", errors="replace")


def nbytes(s):
    return len(s.encode("utf-8"))


def nlines(s):
    return s.count("\n") + (0 if s.endswith("\n") or not s else 1)


def business_group(name):
    if not name:
        return "other"
    n = name.strip().strip("[]").lower()
    for p in PREFIXES:
        if n.startswith(p) and len(n) > len(p):
            n = n[len(p):]
            break
    tokens = [t for t in re.split(r"[_\-\s\.]+", n) if t and not t.isdigit()]
    return tokens[0] if tokens else "other"


def safe(s):
    s = re.sub(r"[^A-Za-z0-9]+", "-", str(s)).strip("-").lower()
    return (s or "x")[:40]


def pick(cols, candidates):
    low = {c.strip().lower(): c for c in cols}
    for c in candidates:
        if c in low:
            return low[c]
    return None


class Unit:
    """A piece of content that should stay together. size/lines measured as written."""
    def __init__(self, label, payload, size, lines, cont=None):
        self.label, self.payload, self.size, self.lines, self.cont = label, payload, size, lines, cont


def pack(groups, max_bytes, max_lines):
    """groups: [(boundary, group_name, [Unit])]. Every unit must already fit the limits.
    Returns parts: [{boundary, groups:set, units:[Unit], size, lines}]."""
    parts, cur = [], None

    def close():
        nonlocal cur
        if cur and cur["units"]:
            parts.append(cur)
        cur = None

    for boundary, gname, units in groups:
        gsize, glines = sum(u.size for u in units), sum(u.lines for u in units)
        if cur and (cur["boundary"] != boundary or cur["size"] + gsize > max_bytes or cur["lines"] + glines > max_lines):
            close()
        for u in units:
            if cur and (cur["size"] + u.size > max_bytes or cur["lines"] + u.lines > max_lines):
                close()
            if cur is None:
                cur = {"boundary": boundary, "groups": set(), "units": [], "size": 0, "lines": 0}
            cur["groups"].add(gname)
            cur["units"].append(u)
            cur["size"] += u.size
            cur["lines"] += u.lines
    close()
    return parts


def chunk_lines(text, max_bytes, max_lines):
    """Split text into pieces within the limits, preferring paragraph breaks, then line breaks;
    a single line longer than the limit is cut (last resort)."""
    pieces, cur, cur_b, cur_l = [], [], 0, 0
    for ln in text.splitlines(keepends=True):
        b = nbytes(ln)
        while b > max_bytes:                       # last resort: one enormous line
            cut = ln.encode("utf-8")[:max_bytes].decode("utf-8", errors="ignore")
            if cur:
                pieces.append("".join(cur)); cur, cur_b, cur_l = [], 0, 0
            pieces.append(cut + "\n")
            ln = ln[len(cut):]
            b = nbytes(ln)
        if cur and (cur_b + b > max_bytes or cur_l + 1 > max_lines):
            # step back to the last blank line in the current piece, if there is one
            idx = max((i for i, x in enumerate(cur) if not x.strip()), default=-1)
            if 0 < idx < len(cur) - 1:
                pieces.append("".join(cur[:idx + 1])); cur = cur[idx + 1:]
            else:
                pieces.append("".join(cur)); cur = []
            cur_b, cur_l = sum(nbytes(x) for x in cur), len(cur)
        cur.append(ln); cur_b += b; cur_l += 1
    if cur:
        pieces.append("".join(cur))
    return [p for p in pieces if p]


# ---------------------------------------------------------------- CSV
def split_csv(path, max_bytes, max_lines, outdir, stem):
    csv.field_size_limit(min(sys.maxsize, 2**31 - 1))
    rows = list(csv.reader(read_text(path).splitlines(keepends=True)))
    if not rows:
        return [], "empty file", None, []
    header, rows = rows[0], rows[1:]
    scol, ocol = pick(header, SCHEMA_COLS), pick(header, OBJECT_COLS)
    si = header.index(scol) if scol else None
    oi = header.index(ocol) if ocol else None
    side_files = []

    def rowtext(r):
        from io import StringIO
        b = StringIO(); csv.writer(b).writerow(r); return b.getvalue()

    hsize = nbytes(rowtext(header))
    cap_b, cap_l = max_bytes - hsize, max_lines - 1
    objects = OrderedDict()
    for i, r in enumerate(rows):
        sch = r[si] if si is not None and si < len(r) else ""
        obj = r[oi] if oi is not None and oi < len(r) else f"row{i+2}"
        t = rowtext(r)
        if nbytes(t) > cap_b:                       # a single row too large: move its biggest cell to a side file
            k = max(range(len(r)), key=lambda j: len(r[j]))
            side = f"{stem}_row{i+2}_col-{safe(header[k] if k < len(header) else k)}.txt"
            pieces = chunk_lines(r[k], cap_b, cap_l)
            names = []
            for n, p in enumerate(pieces, 1):
                nm = side if len(pieces) == 1 else side.replace(".txt", f"_{n:02d}.txt")
                with open(os.path.join(outdir, nm), "w", encoding="utf-8") as f:
                    f.write(f"<!-- Cell '{header[k] if k < len(header) else k}' of row {i+2} of {os.path.basename(path)}"
                            f" ({sch}.{obj}), piece {n} of {len(pieces)} -->\n" + p)
                names.append(nm)
            side_files += names
            r = list(r); r[k] = "[cell too large for one part: see " + ", ".join(names) + "]"
            t = rowtext(r)
        objects.setdefault((sch, obj), []).append((r, nbytes(t), max(1, t.count("\n"))))

    by = OrderedDict()
    for (sch, obj), rs in objects.items():
        g = business_group(obj) if oi is not None else "rows"
        size, lines = sum(x[1] for x in rs), sum(x[2] for x in rs)
        if size <= cap_b and lines <= cap_l:
            us = [Unit((sch, obj), [x[0] for x in rs], size, lines)]
        else:                                        # object too big: split between rows, marked "continued"
            us, cur, cb, cl = [], [], 0, 0
            for r, b, l in rs:
                if cur and (cb + b > cap_b or cl + l > cap_l):
                    us.append(cur); cur, cb, cl = [], 0, 0
                cur.append((r, b, l)); cb += b; cl += l
            if cur:
                us.append(cur)
            us = [Unit((sch, obj), [x[0] for x in c], sum(x[1] for x in c), sum(x[2] for x in c),
                       cont=(n, len(us))) for n, c in enumerate(us, 1)]
        by.setdefault((sch, g), []).extend(us)
    groups = [(k[0], k[1], v) for k, v in sorted(by.items(), key=lambda kv: (kv[0][0].lower(), kv[0][1]))]
    parts = pack(groups, cap_b, cap_l)
    written = []
    for n, p in enumerate(parts, 1):
        sch = p["boundary"] or "no-schema"
        grp = next(iter(p["groups"])) if len(p["groups"]) == 1 else "mixed"
        fname = f"{stem}_part{n:03d}_{safe(sch)}_{safe(grp)}.csv"
        with open(os.path.join(outdir, fname), "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f); w.writerow(header)
            for u in p["units"]:
                w.writerows(u.payload)
        labels = [u.label[1] + (f" (part {u.cont[0]} of {u.cont[1]})" if u.cont else "") for u in p["units"]]
        written.append({"file": fname, "boundary": sch, "groups": sorted(p["groups"]), "items": labels,
                        "objects": [(u.label[0], u.label[1]) for u in p["units"]],
                        "continued": any(u.cont for u in p["units"])})
    rule = (f"one object per unit (schema column: {scol or 'none'}, object column: {ocol or 'none'}); "
            f"grouped by schema, then business group; objects too large are split between rows")
    return written, rule, "Schema", side_files


# ---------------------------------------------------------------- Markdown
def split_markdown(path, max_bytes, max_lines, outdir, stem):
    text = read_text(path)
    sections, cur, fence, chapter = [], {"chapter": "(start)", "title": "(start)", "lines": []}, False, "(start)"
    for ln in text.splitlines(keepends=True):
        if ln.lstrip().startswith(("```", "~~~")):
            fence = not fence
        m = None if fence else re.match(r"^(#{1,2})\s+(.*)", ln)
        if m:
            if cur["lines"]:
                sections.append(cur)
            if m.group(1) == "#":
                chapter = m.group(2).strip()
            cur = {"chapter": chapter, "title": m.group(2).strip(), "lines": []}
        cur["lines"].append(ln)
    if cur["lines"]:
        sections.append(cur)

    def sub_split(title, body):
        """Section too big: split at ### … headings first, then paragraphs/lines."""
        blocks, curb, fence = [], [], False
        for ln in body.splitlines(keepends=True):
            if ln.lstrip().startswith(("```", "~~~")):
                fence = not fence
            if not fence and re.match(r"^#{3,6}\s+", ln) and curb:
                blocks.append("".join(curb)); curb = []
            curb.append(ln)
        if curb:
            blocks.append("".join(curb))
        pieces = []
        for b in blocks:
            pieces += [b] if nbytes(b) <= max_bytes and nlines(b) <= max_lines else chunk_lines(b, max_bytes, max_lines)
        merged, acc = [], ""
        for p in pieces:                              # re-join small neighbours so parts are not tiny
            if acc and (nbytes(acc + p) > max_bytes or nlines(acc + p) > max_lines):
                merged.append(acc); acc = ""
            acc += p
        if acc:
            merged.append(acc)
        return [Unit(title, p, nbytes(p), nlines(p), cont=(i, len(merged))) for i, p in enumerate(merged, 1)]

    by = OrderedDict()
    for s in sections:
        body = "".join(s["lines"])
        if nbytes(body) <= max_bytes and nlines(body) <= max_lines:
            by.setdefault(s["chapter"], []).append(Unit(s["title"], body, nbytes(body), nlines(body)))
        else:
            by.setdefault(s["chapter"], []).extend(sub_split(s["title"], body))
    margin = 200                                      # room for the part header line
    parts = pack([(ch, ch, us) for ch, us in by.items()], max_bytes - margin, max_lines - 2)
    written = []
    for n, p in enumerate(parts, 1):
        fname = f"{stem}_part{n:03d}_{safe(p['boundary'])}.md"
        cont = [u for u in p["units"] if u.cont]
        head = (f"<!-- Part {n} of {len(parts)} of {os.path.basename(path)} · chapter: {p['boundary']}"
                + (" · continues a section split across parts" if cont else "") + " -->\n")
        with open(os.path.join(outdir, fname), "w", encoding="utf-8") as f:
            f.write(head + "".join(u.payload for u in p["units"]))
        labels = [u.label + (f" (part {u.cont[0]} of {u.cont[1]})" if u.cont else "") for u in p["units"]]
        written.append({"file": fname, "boundary": p["boundary"], "groups": [], "items": labels,
                        "continued": bool(cont)})
    return written, ("one section under a # or ## heading; parts never mix chapters; sections too large are "
                     "split at ### headings, then paragraphs, then lines"), "Chapter", []


# ---------------------------------------------------------------- JSON
def split_json(path, max_bytes, max_lines, outdir, stem):
    data = json.loads(read_text(path))
    key, items = None, None
    if isinstance(data, list):
        items = data
    elif isinstance(data, dict):
        lists = [k for k, v in data.items() if isinstance(v, list) and v and all(isinstance(x, dict) for x in v)]
        if lists:
            key = max(lists, key=lambda k: len(data[k]))
            items = data[key]
    if items is None:                                 # no list of items: treat as indented text
        text = json.dumps(data, ensure_ascii=False, indent=1)
        items, key = None, None
        pieces = chunk_lines(text, max_bytes - 200, max_lines - 2)
        written = []
        for n, p in enumerate(pieces, 1):
            fname = f"{stem}_part{n:03d}.txt"
            with open(os.path.join(outdir, fname), "w", encoding="utf-8") as f:
                f.write(f"<!-- Part {n} of {len(pieces)} of {os.path.basename(path)} (indented JSON text) -->\n" + p)
            written.append({"file": fname, "boundary": "", "groups": [], "items": [f"lines of part {n}"],
                            "continued": len(pieces) > 1})
        return written, "no list of items found: written as indented text and split between lines", "—", []
    units = []
    for i, it in enumerate(items):
        label = str((it.get("name") or it.get("job_name") or it.get("pipeline_name") or it.get("id") or f"item{i+1}")
                    if isinstance(it, dict) else f"item{i+1}")
        t = json.dumps(it, ensure_ascii=False, indent=1)
        units.append(Unit(label, it, nbytes(t) + 4, nlines(t) + 1))
    small = [u for u in units if u.size <= max_bytes - 400 and u.lines <= max_lines - 4]
    big = [u for u in units if u not in small]
    parts = pack([("all", "items", small)], max_bytes - 400, max_lines - 4)
    written = []
    n = 0
    for p in parts:
        n += 1
        fname = f"{stem}_part{n:03d}.json"
        its = [u.payload for u in p["units"]]
        out = its if key is None else {**{k: v for k, v in data.items() if k != key}, key: its}
        with open(os.path.join(outdir, fname), "w", encoding="utf-8") as f:
            json.dump(out, f, ensure_ascii=False, indent=1)
        written.append({"file": fname, "boundary": "", "groups": [], "items": [u.label for u in p["units"]],
                        "continued": False})
    for u in big:                                     # one item too large: indented text, split between lines
        pieces = chunk_lines(json.dumps(u.payload, ensure_ascii=False, indent=1), max_bytes - 200, max_lines - 2)
        for k, p in enumerate(pieces, 1):
            n += 1
            fname = f"{stem}_part{n:03d}_{safe(u.label)}.txt"
            with open(os.path.join(outdir, fname), "w", encoding="utf-8") as f:
                f.write(f"<!-- Item '{u.label}' of {os.path.basename(path)}, piece {k} of {len(pieces)} (indented JSON text) -->\n" + p)
            written.append({"file": fname, "boundary": "", "groups": [], "items": [f"{u.label} (part {k} of {len(pieces)})"],
                            "continued": True})
    return written, f"one item of the list{(' under key ' + key) if key else ''} per unit; items too large are split as text", "—", []


# ---------------------------------------------------------------- main entry
def split_file(path, max_kb=150, max_lines=2500, force=False):
    """Split one file. Returns a dict describing the result. Raises ValueError for unsupported files."""
    path = os.path.abspath(path)
    stem, ext = os.path.splitext(os.path.basename(path))
    ext = ext.lower()
    if ext not in SPLITTABLE:
        raise ValueError("only .csv, .md, .markdown, .txt and .json can be split; convert other formats first")
    outdir = path + ".parts"
    if os.path.exists(outdir):
        if not force:
            raise FileExistsError(f"{outdir} already exists (use --force to split again)")
        shutil.rmtree(outdir)
    os.makedirs(outdir)
    max_bytes = max_kb * 1024
    try:
        if ext == ".csv":
            written, rule, bword, side = split_csv(path, max_bytes, max_lines, outdir, stem)
        elif ext == ".json":
            try:
                written, rule, bword, side = split_json(path, max_bytes, max_lines, outdir, stem)
            except json.JSONDecodeError:
                written, rule, bword, side = split_markdown(path, max_bytes, max_lines, outdir, stem)
                rule = "not valid JSON: split as text. " + rule
        else:
            written, rule, bword, side = split_markdown(path, max_bytes, max_lines, outdir, stem)
    except Exception:
        shutil.rmtree(outdir, ignore_errors=True)
        raise

    # Index: short and readable (never larger than a part); object lookup kept in a separate CSV.
    idx = os.path.join(outdir, f"{stem}.index.md")
    with open(idx, "w", encoding="utf-8") as f:
        f.write(f"# Split index: {os.path.basename(path)}\n\n")
        f.write(f"- Original: `{os.path.basename(path)}` ({os.path.getsize(path)/1024/1024:.1f} MB), not changed; do not read it\n")
        f.write(f"- Parts: {len(written)} (each at most {max_kb} KB and {max_lines} lines)\n")
        f.write(f"- Unit rule: {rule}\n")
        if written and "objects" in written[0]:
            f.write(f"- Which part holds which object: search `{stem}.objects.csv` (do not read it whole)\n")
        if side:
            f.write(f"- Very large single cells moved to side files: {len(side)} (`{stem}_row…_col-….txt`)\n")
        f.write("\n| Part | KB | " + bword + " | Business groups | Contains (first items) | Continued |\n|---|---|---|---|---|---|\n")
        for w in written:
            items = w["items"]
            first = "; ".join(items[:5]) + (f" … (+{len(items)-5})" if len(items) > 5 else "")
            f.write(f"| {w['file']} | {os.path.getsize(os.path.join(outdir, w['file']))//1024} | {w['boundary']} | "
                    f"{', '.join(w['groups'])} | {first} | {'yes' if w['continued'] else ''} |\n")
    if written and "objects" in written[0]:
        with open(os.path.join(outdir, f"{stem}.objects.csv"), "w", newline="", encoding="utf-8") as f:
            wr = csv.writer(f); wr.writerow(["schema", "object", "part"])
            for w in written:
                for s, o in w["objects"]:
                    wr.writerow([s, o, w["file"]])
    st = os.stat(path)
    with open(os.path.join(outdir, ".split.json"), "w", encoding="utf-8") as f:
        json.dump({"original": os.path.basename(path), "size": st.st_size, "mtime": int(st.st_mtime),
                   "max_kb": max_kb, "max_lines": max_lines, "parts": [w["file"] for w in written] + side}, f, indent=1)
    return {"outdir": outdir, "index": idx, "parts": len(written), "side_files": len(side),
            "continued": sum(1 for w in written if w["continued"])}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file")
    ap.add_argument("--max-kb", type=int, default=150, help="largest part in KB (default 150)")
    ap.add_argument("--max-lines", type=int, default=2500, help="longest part in lines (default 2500)")
    ap.add_argument("--force", action="store_true", help="split again even if a .parts folder exists")
    a = ap.parse_args()
    try:
        r = split_file(a.file, a.max_kb, a.max_lines, a.force)
    except (ValueError, FileExistsError) as e:
        sys.exit(str(e))
    print(f"Split {os.path.basename(a.file)} into {r['parts']} parts in {r['outdir']}"
          + (f" ({r['continued']} continue a unit too large for one part)" if r["continued"] else ""))
    print(f"Index: {r['index']}")


if __name__ == "__main__":
    main()
