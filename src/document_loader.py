from pathlib import Path

file_path = Path("data/raw/company_policy.txt")

text = file_path.read_text(encoding="utf-8")

print(text)