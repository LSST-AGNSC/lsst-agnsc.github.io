#!/usr/bin/env python3
"""Fill _data/files.yml with direct Google Drive links, using only the folder links in _data/drive.yml.

Each shared folder is listed through Drive's public "embedded folder view" (no API key needed; the
folder must be shared as "Anyone with the link"). File names are matched exactly against the keys
already present in _data/files.yml; keys are never added or removed, only their values filled in.
Run locally:  python3 tools/drive_links.py        (add --check to only report, without writing)
"""
import re, sys, pathlib, urllib.request, urllib.parse, html

ROOT = pathlib.Path(__file__).resolve().parent.parent
DRIVE = ROOT / "_data" / "drive.yml"
FILES = ROOT / "_data" / "files.yml"

def folder_id(link):
    link = link.strip().strip('"').strip("'")
    if not link: return None
    m = re.search(r'/folders/([A-Za-z0-9_-]+)', link) or re.search(r'[?&]id=([A-Za-z0-9_-]+)', link)
    return m.group(1) if m else (link if re.fullmatch(r'[A-Za-z0-9_-]{10,}', link) else None)

def list_folder(fid):
    """Return {file name: direct link} for a public folder."""
    url = f"https://drive.google.com/embeddedfolderview?id={fid}#list"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (lsst-agnsc.github.io link updater)"})
    page = urllib.request.urlopen(req, timeout=60).read().decode("utf-8", "replace")
    out = {}
    # entries look like: <div class="flip-entry" id="entry-<ID>"> ... <a href="https://drive.google.com/file/d/<ID>/view..."> ... <div class="flip-entry-title">NAME</div>
    for m in re.finditer(r'<div class="flip-entry" id="entry-([A-Za-z0-9_-]+)">(.*?)</div>\s*</div>\s*</a>', page, re.S):
        eid, chunk = m.group(1), m.group(2)
        t = re.search(r'flip-entry-title">(.*?)</div>', chunk, re.S)
        if t: out[html.unescape(re.sub(r'<[^>]+>', '', t.group(1))).strip()] = f"https://drive.google.com/file/d/{eid}/view"
    if not out:  # fallback: any file link followed by a title
        for m in re.finditer(r'file/d/([A-Za-z0-9_-]+)/view[^"]*"[^>]*>.*?flip-entry-title">(.*?)</div>', page, re.S):
            out[html.unescape(re.sub(r'<[^>]+>', '', m.group(2))).strip()] = f"https://drive.google.com/file/d/{m.group(1)}/view"
    return out

def main():
    check = "--check" in sys.argv
    drive = dict(re.findall(r'^(\w+):\s*"?([^"\n]*)"?\s*$', DRIVE.read_text(), re.M))
    text = FILES.read_text()
    # sections: "# Documents folder..." / "# Talks folder..."; keys inside each belong to that folder
    section = None; found = {}; missing = []; filled = 0
    for fname, link in (("documents", drive.get("documents", "")), ("talks", drive.get("talks", ""))):
        fid = folder_id(link)
        if not fid: print(f"{fname}: no folder link in _data/drive.yml, skipped"); continue
        try: found[fname] = list_folder(fid)
        except Exception as e: print(f"{fname}: could not list folder ({e})"); continue
        print(f"{fname}: {len(found[fname])} files found in the Drive folder")
    out = []
    for line in text.splitlines():
        m = re.match(r'^# (Documents|Talks) folder', line)
        if m: section = m.group(1).lower()
        k = re.match(r'^"([^"]+)": "([^"]*)"$', line)
        if k and section in found:
            name, cur = k.group(1), k.group(2)
            new = found[section].get(name)
            if new and new != cur:
                line = f'"{name}": "{new}"'; filled += 1
            elif not new and not cur:
                missing.append(f"{section}/{name}")
        out.append(line)
    if missing: print("not found in Drive (upload or rename to match):\n  " + "\n  ".join(missing))
    if check: print(f"would fill {filled} links"); return
    if filled:
        FILES.write_text("\n".join(out) + "\n"); print(f"filled {filled} links in _data/files.yml")
    else: print("nothing to change")

if __name__ == "__main__": main()
