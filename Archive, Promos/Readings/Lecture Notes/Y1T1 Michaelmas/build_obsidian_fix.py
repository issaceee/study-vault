#!/usr/bin/env python3
import re
from pathlib import Path

ROOT = Path.cwd()
BUILD = ROOT / "build"
BUILD.mkdir(exist_ok=True)

# regex to detect YAML frontmatter at start of a file: starts with --- on its own line
yaml_start = re.compile(r'^\s*---\s*$', re.MULTILINE)
yaml_end   = re.compile(r'^\s*---\s*$', re.MULTILINE)

def strip_leading_yaml(text):
    # If file begins with --- (possibly with leading whitespace/newlines), remove up to the next ---
    m = re.match(r'^\s*---\s*\n', text)
    if not m:
        return text
    # find the closing --- that ends the frontmatter
    # search after the first newline to avoid matching same line
    closing = yaml_end.search(text, m.end())
    if closing:
        return text[closing.end():].lstrip('\n')
    else:
        # no closing --- found: be conservative and return original (or remove from start to some limit)
        return text

merged_parts = []
files = sorted([p for p in ROOT.glob("*.md")])
if not files:
    print("No .md files found in this folder.")
    raise SystemExit(1)

for i, md in enumerate(files):
    txt = md.read_text(encoding='utf-8')
    txt = strip_leading_yaml(txt)
    # add file heading (optional) so it's clear where notes came from:
    merged_parts.append(f"\n\n<!-- file: {md.name} -->\n\n")
    merged_parts.append(txt)
    merged_parts.append("\n\n\\newpage\n\n")

merged_md = BUILD / "merged.md"
merged_md.write_text("".join(merged_parts), encoding='utf-8')
print("✔ rebuilt merged.md in ./build/ (YAML frontmatter stripped from each file)")

