import faiss
import json
from sentence_transformers import SentenceTransformer

# Load FAISS index
index = faiss.read_index("religious_texts.index")

# Load metadata (JSON instead of pickle)
with open("religious_texts_meta.json", "r", encoding="utf-8") as f:
    metadata = json.load(f)

# Load the same embedding model
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# Example query
query = "wine and alcohol"
query_vector = model.encode([query])

# Search
k = 5
distances, indices = index.search(query_vector, k)

# Show results
for idx, score in zip(indices[0], distances[0]):
    verse = metadata[idx]
    print(f"{verse['religion']} | {verse['ref']} ({score:.4f})\n{verse['text']}\n")
