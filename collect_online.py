import requests
import json
import time
religious_texts = []

# --- Fetch Quran (Yusuf Ali) ---
quran_url = "https://api.alquran.cloud/v1/quran/en.yusufali"
quran_data = requests.get(quran_url).json()

for surah in quran_data["data"]["surahs"]:
    for ayah in surah["ayahs"]:
        religious_texts.append({
            "religion": "Islam",
            "ref": f"Quran {surah['number']}:{ayah['numberInSurah']}",
            "text": ayah["text"]
        })

print(f"✅ Quran loaded: {len(quran_data['data']['surahs'])} surahs, {len([t for t in religious_texts if t['religion']=='Islam'])} ayahs")

def fetch_bible_chapter(book, chapter, retries=3):
    url = f"https://bible-api.com/{book}%20{chapter}?translation=kjv"
    for attempt in range(retries):
        try:
            resp = requests.get(url, timeout=10)

            if resp.status_code != 200:
                print(f"⚠️ {book} {chapter} - HTTP {resp.status_code}")
                time.sleep(2)
                continue

            # Check if response is JSON
            if "application/json" not in resp.headers.get("Content-Type", ""):
                print(f"⚠️ {book} {chapter} - Not JSON, got {resp.headers.get('Content-Type')}")
                time.sleep(2)
                continue

            data = resp.json()
            if "verses" in data:
                return data["verses"]

            print(f"⚠️ {book} {chapter} - No verses found")
            return None

        except requests.exceptions.RequestException as e:
            print(f"⚠️ Error fetching {book} {chapter}: {e}")
            time.sleep(2)

    print(f"❌ Failed after {retries} retries for {book} {chapter}")
    return None


# Example usage
books_and_chapters = {
    "John": 21,
    "Matthew": 28,
    "Genesis": 50
}

for book, num_chapters in books_and_chapters.items():
    for chapter in range(1, num_chapters + 1):
        verses = fetch_bible_chapter(book, chapter)
        if verses:
            for verse in verses:
                religious_texts.append({
                    "religion": "Christianity",
                    "ref": f"{verse['book_name']} {verse['chapter']}:{verse['verse']}",
                    "text": verse["text"].strip()
                })
        time.sleep(0.5)  # avoid hitting rate limits

print(f"✅ Bible loaded: {len([t for t in religious_texts if t['religion']=='Christianity'])} verses")

# --- Fetch Tanakh (JPS 1917) from Sefaria ---
tanakh_books = {
    "Genesis": 50,
    "Exodus": 40
}

for book, num_chapters in tanakh_books.items():
    for chapter in range(1, num_chapters + 1):
        tanakh_url = f"https://www.sefaria.org/api/texts/{book}.{chapter}?lang=english&version=The%20Holy%20Scriptures%20by%20JPS%201917"
        resp = requests.get(tanakh_url)
        data = resp.json()

        if isinstance(data["text"], list):
            for verse_num, verse_text in enumerate(data["text"], start=1):
                if verse_text.strip():
                    religious_texts.append({
                        "religion": "Judaism",
                        "ref": f"{book} {chapter}:{verse_num}",
                        "text": verse_text.strip()
                    })
        time.sleep(0.5)  # avoid rate limit

print(f"✅ Tanakh loaded: {len([t for t in religious_texts if t['religion']=='Judaism'])} verses")

# --- Save to file ---
with open("religious_texts.json", "w", encoding="utf-8") as f:
    json.dump(religious_texts, f, ensure_ascii=False, indent=2)

print(f" Saved all texts to religious_texts.json (total {len(religious_texts)} entries)")
