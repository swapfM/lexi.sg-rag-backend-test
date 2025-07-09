"""
Document Text Extraction and Chunking part. Chain ID is also saved.

Functions:
    extract_text_from_docx(path): Extract text from Word documents
    extract_text_from_pdf(path): Extract text from PDF documents
    extract_text(path): Universal text extraction based on file extension
    chunk_text(text, doc_name, chunk_size, overlap, page_number): Split text into chunks

"""

from docx import Document
import fitz
import os


def extract_text_from_docx(path):
    doc = Document(path)
    return "\n".join(p.text.strip() for p in doc.paragraphs if p.text.strip())


def extract_text_from_pdf(path):
    doc = fitz.open(path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text


def extract_text(path):
    ext = os.path.splitext(path)[1].lower()
    print(ext)
    if ext in [".docx", ".doc"]:
        return extract_text_from_docx(path)
    elif ext in [".pdf", ".PDF"]:
        return extract_text_from_pdf(path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")


def chunk_text(text, doc_name, chunk_size=300, overlap=50, page_number=None):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk_words = words[i : i + chunk_size]
        chunk_text = " ".join(chunk_words)
        meta = {
            "source": doc_name,
            "chunk_id": i // (chunk_size - overlap),
            "text": chunk_text,
        }
        if page_number is not None:
            meta["page"] = page_number
        chunks.append((chunk_text, meta))
    return chunks
