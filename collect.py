import requests
import json
import re
from pathlib import Path

religious_texts = []

# ------------------
# 1. Quran (Tanzil.net, Pickthall translation)
# ------------------
quran_url = "https://tanzil.net/trans/en.pickthall"
quran_resp = requests.get(quran_url)
quran_text = quran_resp.text.strip().split("\n")

for idx, line in enumerate(quran_text):
    # Format: 1|1|In the name of Allah, the Beneficent, the Merciful.
    parts = line.split("|", 2)
    if len(parts) == 3:
        surah, ayah, verse = parts
        religious_texts.append({
            "religion": "Islam",
            "ref": f"{surah}:{ayah}",
            "text": verse.strip()
        })
print(f"✅ Quran loaded: {len([t for t in religious_texts if t['religion']=='Islam'])} verses")


# ------------------
# 2. Bible (KJV from Project Gutenberg)
# ------------------
bible_url = "https://www.gutenberg.org/cache/epub/10/pg10.txt"
bible_resp = requests.get(bible_url)
bible_raw = bible_resp.text

# Remove Project Gutenberg header/footer
bible_raw = bible_raw.split("*** START OF THIS PROJECT GUTENBERG EBOOK")[1]
bible_raw = bible_raw.split("*** END OF THIS PROJECT GUTENBERG EBOOK")[0]

# Regex to match "Book Chapter:Verse text"
pattern = re.compile(r"^([1-3]?\s?[A-Za-z]+)\s(\d+):(\d+)\s(.+)$", re.MULTILINE)

for match in pattern.finditer(bible_raw):
    book, chapter, verse, text = match.groups()
    religious_texts.append({
        "religion": "Christianity",
        "ref": f"{book} {chapter}:{verse}",
        "text": text.strip()
    })
print(f"✅ Bible loaded: {len([t for t in religious_texts if t['religion']=='Christianity'])} verses")


# ------------------
# 3. Torah (from Sefaria JSON dump)
# ------------------
torah_url = "https://www.sefaria.org/download/torah.json"  # Replace with actual JSON dump URL
torah_resp = requests.get(torah_url)
torah_data = torah_resp.json()

# Flatten Torah structure (Book → Chapter → Verse)
for book in torah_data["books"]:
    for chapter_idx, chapter in enumerate(book["text"], start=1):
        for verse_idx, verse in enumerate(chapter, start=1):
            if verse.strip():
                religious_texts.append({
                    "religion": "Judaism",
                    "ref": f"{book['title']} {chapter_idx}:{verse_idx}",
                    "text": verse.strip()
                })
print(f"✅ Torah loaded: {len([t for t in religious_texts if t['religion']=='Judaism'])} verses")


# ------------------
# Save all texts locally
# ------------------
Path("data").mkdir(exist_ok=True)
with open("data/religious_texts.json", "w", encoding="utf-8") as f:
    json.dump(religious_texts, f, ensure_ascii=False, indent=2)

print(f"💾 Saved {len(religious_texts)} total verses to data/religious_texts.json")
