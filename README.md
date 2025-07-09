#Local RAG Q&A System (FastAPI + Ollama + FAISS)

This project is a Retrieval-Augmented Generation (RAG) backend that combines semantic search with a local language model to answer user queries based on custom documents.

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/swapfM/local-rag-api.git
cd backend/
```

### 2. Install Python Dependencies

Ensure you're using Python 3.9–3.11:

```bash
pip install -r requirements.txt
```

### 3. Install and Run Ollama

Install from [https://ollama.com/download](https://ollama.com/download)

Then pull and run the mistral:

```bash
ollama run mistral
```

This will keep the LLM running locally on `http://localhost:11434`.

### 4. Prepare Your Documents

Put your `.pdf` or `.docx` files inside the `app/reference_docs` directory.

Then run:

```bash
python parse_doc.py
```

This will chunk, embed, and store your documents in `app/vector_store/`.

### 5. Start the API Server

```bash
uvicorn main:app --reload
```
