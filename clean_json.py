import json
from pathlib import Path

# --- Config ---
INPUT_FILE = "religious_texts.json"
OUTPUT_FILE = "religious_texts_clean.json"
MIN_TEXT_LENGTH = 5  # Minimum characters for a verse to be kept

# --- Load data ---
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

print(f"📥 Loaded {len(data)} entries from {INPUT_FILE}")

# --- Preprocess ---
seen = set()
cleaned_data = []

for entry in data:
    text = entry.get("text", "").strip()

    # Normalize whitespace (collapses multiple spaces/newlines to single space)
    text = " ".join(text.split())

    # Skip empty or too-short verses
    if not text or len(text) < MIN_TEXT_LENGTH:
        continue

    # Create a unique key for deduplication
    unique_key = f"{entry.get('religion','')}|{entry.get('ref','')}|{text}"
    if unique_key in seen:
        continue
    seen.add(unique_key)

    cleaned_data.append({
        "religion": entry.get("religion", "").strip(),
        "ref": entry.get("ref", "").strip(),
        "text": text
    })

print(f"✅ Cleaned: {len(cleaned_data)} entries (removed {len(data) - len(cleaned_data)})")

# --- Save cleaned file ---
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(cleaned_data, f, ensure_ascii=False, indent=2)

print(f"💾 Saved cleaned data to {OUTPUT_FILE}")
