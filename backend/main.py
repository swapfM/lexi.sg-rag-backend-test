from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from app.query_llama import query_rag
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/files", StaticFiles(directory="app/reference_docs"), name="files")


class Query(BaseModel):
    query: str


@app.post("/query")
def query_legal_llm(payload: Query):
    query = payload.query

    answer, citations = query_rag(query)

    return {
        "answer": answer,
        "citations": citations,
    }
