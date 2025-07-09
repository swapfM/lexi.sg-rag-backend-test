"""
Vector Search and Chunks Retrieval system.

This module implements a semantic search system using FAISS (Facebook AI Similarity Search)
for efficient similarity search over document embeddings. It loads a pre-built FAISS index
and corresponding metadata to enable fast retrieval of relevant text chunks based on
semantic similarity to user queries.

"""

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import json

faiss_index = faiss.read_index("app/vector_store/index.faiss")
with open("app/vector_store/metadata.json", "r", encoding="utf-8") as f:
    metadatas = json.load(f)

model = SentenceTransformer("all-MiniLM-L6-v2")


def retrieve_chunks(query: str, k: int = 5):
    query_embedding = model.encode([query], normalize_embeddings=True)
    query_embedding = np.array(query_embedding).astype("float32")

    D, I = faiss_index.search(query_embedding, k)

    results = []
    for idx, score in zip(I[0], D[0]):
        if idx < len(metadatas):
            meta = metadatas[idx]
            meta["score"] = float(score)

            words = meta["text"].split()
            meta["short_text"] = " ".join(words[:30]) + (
                "..." if len(words) > 30 else ""
            )

            results.append(meta)
    return results
