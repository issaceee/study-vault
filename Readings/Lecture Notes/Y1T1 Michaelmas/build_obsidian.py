import re
from pathlib import Path

# current folder = your Obsidian notes folder
ROOT = Path.cwd()
BUILD = ROOT / "build"
BUILD.mkdir(exist_ok=True)

pattern = re.compile(r'\[\[([^|\]]+)(?:\|([^]]+))?\]\]')

merged_lines = []

for md in sorted(ROOT.glob("*.md")):
    text = md.read_text(encoding="utf-8")

    # convert [[Page]] and [[Page|Alias]] to markdown links
    def repl(m):
        target = m.group(1)
        label = m.group(2) or target
        return f"[{label}]({target.replace(' ', '%20')}.md)"

    text = pattern.sub(repl, text)

    # remove YAML frontmatter except for first file
    if merged_lines:
        if text.lstrip().startswith("---"):
            parts = text.split("---", 2)
            if len(parts) == 3:
                text = parts[2]

    merged_lines.append(text)
    merged_lines.append("\n\n\\newpage\n\n")

merged_md = BUILD / "merged.md"
merged_md.write_text("".join(merged_lines), encoding="utf-8")

print("✔ merged.md created in ./build/")

