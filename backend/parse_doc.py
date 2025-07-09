import os, json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from app.utils import (
    chunk_text,
    extract_text,
)

model = SentenceTransformer("all-MiniLM-L6-v2")
texts, metadatas = [], []

for file in os.listdir("app/reference_docs"):
    full_path = f"app/reference_docs/{file}"
    print(f"Processing {file}")

    if file.endswith(".pdf"):
        import fitz

        pdf = fitz.open(full_path)
        for page_number, page in enumerate(pdf, start=1):
            text = page.get_text()
            chunks = chunk_text(text, file, page_number=page_number)
            for chunk, meta in chunks:
                texts.append(chunk)
                metadatas.append(meta)
    else:

        text = extract_text(full_path)
        chunks = chunk_text(text, file)
        for chunk, meta in chunks:
            texts.append(chunk)
            metadatas.append(meta)

for i, t in enumerate(texts):
    if not isinstance(t, str):
        texts = [str(t) for t in texts]


embeddings = model.encode(texts)
dimension = embeddings[0].shape[0]
index = faiss.IndexFlatL2(dimension)
index.add(np.array(embeddings))


faiss.write_index(index, "app/vector_store/index.faiss")
with open("app/vector_store/metadata.json", "w") as f:
    json.dump(metadatas, f)

print(" Documents indexed successfully.")
