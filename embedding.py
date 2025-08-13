from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import json

# Load local embedding model
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# Load dataset
with open("religious_texts_clean.json", "r", encoding="utf-8") as f:
    texts = json.load(f)

verse_texts = [entry["text"] for entry in texts]

# Generate embeddings locally
embeddings = model.encode(verse_texts, convert_to_numpy=True)

# Build FAISS index
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

faiss.write_index(index, "religious_texts.index")

# Save metadata
with open("religious_texts_meta.json", "w", encoding="utf-8") as f:
    json.dump(texts, f, ensure_ascii=False, indent=2)

print(f"✅ Stored {len(verse_texts)} verses in FAISS index locally")
