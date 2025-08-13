# step6_augment.py
import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from collections import defaultdict
import textwrap

# Paths (adjust if different)
INDEX_PATH = "religious_texts.index"
META_PATH = "religious_texts_meta.json"   # your JSON metadata saved earlier
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

# Load resources
index = faiss.read_index(INDEX_PATH)
with open(META_PATH, "r", encoding="utf-8") as f:
    metadata = json.load(f)

model = SentenceTransformer(MODEL_NAME)  # same model used to build index

# ---- Helpers ----
def retrieve_top_k(query, k=60):
    """Return list of dicts: [{'idx', 'score', 'religion','ref','text'}, ...] sorted best->worst."""
    q_emb = model.encode([query], convert_to_numpy=True)
    distances, indices = index.search(q_emb, k)
    results = []
    for dist, idx in zip(distances[0], indices[0]):
        if idx < 0:
            continue
        item = metadata[int(idx)]
        results.append({
            "idx": int(idx),
            "score": float(dist),    # lower = more similar for L2 index
            "religion": item.get("religion", "Unknown"),
            "ref": item.get("ref", ""),
            "text": item.get("text", "")
        })
    return results

def group_by_religion(results, per_religion=3, religions_order=None):
    """Return ordered dict of religion -> list of top passages (by earliest best score)."""
    if religions_order is None:
        # Preferred display order:
        religions_order = ["Islam", "Christianity", "Judaism"]
    grouped = {r: [] for r in religions_order}
    # iterate results in ascending score (best first)
    for r in sorted(results, key=lambda x: x["score"]):
        rel = r["religion"]
        if rel not in grouped:
            grouped.setdefault(rel, [])
        if len(grouped[rel]) < per_religion:
            grouped[rel].append(r)
    # remove religions with empty lists
    grouped = {k: v for k, v in grouped.items() if v}
    return grouped

def format_passage(p):
    return f'{p["ref"]} — "{p["text"]}"'

def build_prompt(query, grouped_passages, per_religion, max_chars=3500):
    """
    Build a nicely formatted prompt for the LLM.
    If over max_chars, the top-level loop will reduce per_religion and retry.
    """
    header = textwrap.dedent(f"""
    User question: "{query}"

    You are an objective, scholarly assistant. Use ONLY the passages listed below (with their citations) to:
      1. Provide a short neutral summary of what each religion's passages say (1-4 sentences each).
      2. List clear "Similarities" (bullet points).
      3. List clear "Differences" (bullet points).
      4. Add short "Context/Notes" if relevant (translation or historical notes).
    Keep language neutral, avoid theological judgment, and always cite verse references inline (e.g., Quran 2:255).

    Passages (grouped by religion):
    """).strip() + "\n\n"

    body_parts = []
    for religion, passages in grouped_passages.items():
        block = [f"--- {religion} ---"]
        for p in passages:
            block.append(format_passage(p))
        body_parts.append("\n".join(block))

    body = "\n\n".join(body_parts)
    footer = textwrap.dedent("""

    Answer format (use headings):
    ### Per-Religion Summaries
    ### Similarities
    - ...
    ### Differences
    - ...
    ### Notes / Citations
    - List sources again if needed.
    """).strip()

    prompt = "\n\n".join([header, body, footer])
    # simple length check:
    if len(prompt) > max_chars:
        return None, len(prompt)
    return prompt, len(prompt)

def make_augmented_prompt(query, k=60, per_religion=3, max_chars=3500):
    # 1) retrieve
    results = retrieve_top_k(query, k=k)
    # 2) try grouping and building prompt, reduce per_religion if prompt too big
    for per in range(per_religion, 0, -1):
        grouped = group_by_religion(results, per_religion=per)
        prompt, plen = build_prompt(query, grouped, per, max_chars=max_chars)
        if prompt is not None:
            return prompt, grouped, plen
    # fallback: include just the single best passage overall
    best = results[0:1]
    grouped = group_by_religion(best, per_religion=1)
    prompt, plen = build_prompt(query, grouped, per_religion=1, max_chars=max_chars*2)
    return prompt, grouped, plen

# ---- Example usage ----
if __name__ == "__main__":
    user_query = "What do these scriptures say about forgiveness?"
    prompt, grouped, plen = make_augmented_prompt(user_query, k=90, per_religion=3, max_chars=4000)

    if prompt is None:
        print("❌ Couldn't build prompt within size limit.")
    else:
        print("=== Prompt length:", plen)
        print("=== Grouped passages (counts):", {r: len(ps) for r, ps in grouped.items()})
        print("\n--- BEGIN PROMPT ---\n")
        print(prompt[:2000])   # print the first 2000 chars for preview
        # Optionally save to file:
        with open("augmented_prompt.txt", "w", encoding="utf-8") as f:
            f.write(prompt)
        print("\n(Full prompt saved to augmented_prompt.txt)")
