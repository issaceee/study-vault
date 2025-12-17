
#!/usr/bin/env python3
from pathlib import Path

p = Path("build/merged.md")
if not p.exists():
    print("Error: build/merged.md not found")
    raise SystemExit(1)

lines = p.read_text(encoding='utf-8').splitlines()
out_lines = []
in_code = False
in_yaml = False

for line in lines:
    if line.strip().startswith("```"):
        in_code = not in_code
        if not in_yaml:
            out_lines.append(line)
        continue

    if in_code:
        out_lines.append(line)
        continue

    if not in_yaml and line.strip() == '---':
        in_yaml = True
        continue
    if in_yaml and line.strip() == '---':
        in_yaml = False
        continue

    if in_yaml:
        continue

    out_lines.append(line)

backup = p.with_name("merged.backup.md")
backup.write_text("\n".join(lines), encoding='utf-8')
p.write_text("\n".join(out_lines), encoding='utf-8')

print(f"Wrote cleaned merged.md (backup at {backup})")
