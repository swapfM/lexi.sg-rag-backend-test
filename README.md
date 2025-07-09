#Local RAG Q&A System (FastAPI + Ollama + FAISS)

This project is a Retrieval-Augmented Generation (RAG) backend that combines semantic search with a local language model to answer user queries based on custom documents.

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/local-rag-api.git
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

## Testing API and Sample Input/Output

### Endpoint: `POST /query`

**Request:**

```
POST http://localhost:8000/query
Content-Type: application/json
```

**Body:**

```json
{
  "query": "Is an insurance company liable to pay compensation if a transport vehicle involved in an accident was being used without a valid permit?"
}
```

**Response:**

```json
{
    "answer": " Based on the context provided, it appears that an insurance company may not be obliged to pay compensation if a transport vehicle involved in an accident was being used without a valid permit. This is inferred from case [2] where the court ruled that the insurance company was not liable to indemnify the insured because the vehicle did not have the permit on the date of the accident"
    "citations": [
        {
            "text": "to the Rule can be applied. It is a statutory liability created without which the claimant should not get any amount under that count. Compensation on account of accident arising...",
            "source": "Darshan Vs State of Punjab (Tyre Burst Claim Payable).pdf"
        },
        {
            "text": "was not obliged to indemnify the insured. That apart, a stand was taken that the vehicle did not have the permit on the date of the accident."
            "source": "Amrit Paul Singh v. TATA AIG (SC NO ROUTE Permit insurance Co. Recover from Owner).docx"
        }
    ],

}
```
