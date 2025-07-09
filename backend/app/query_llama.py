"""
Retrieval-Augmented Generation (RAG) Query System using ollama

This module implements a complete RAG pipeline for legal question answering.
It combines document retrieval with language model generation to provide
contextually grounded answers with proper citations.

"""

from app.rag import retrieve_chunks
from sentence_transformers import SentenceTransformer
import ollama

model = SentenceTransformer("all-MiniLM-L6-v2")


def query_rag(query: str, top_k: int = 3):

    chunks = retrieve_chunks(query, k=top_k)

    context = ""
    citations = []

    for idx, chunk in enumerate(chunks):

        words = chunk["text"].split()
        short_text = " ".join(words[:30]) + ("..." if len(words) > 30 else "")

        context += f"[{idx+1}] From {chunk['source']}:\n{short_text}\n\n"

        citations.append(
            {
                "text": short_text,
                "source": chunk["source"],
            }
        )

    prompt = f"""Use the context below to answer the legal question. Include citations like [1], [2].

Context:
{context}
Question: {query}
Answer:"""

    response = ollama.chat(
        model="mistral",
        messages=[{"role": "user", "content": prompt}],
    )
    answer = response["message"]["content"]

    return answer, citations
