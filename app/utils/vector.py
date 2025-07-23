import pdfplumber
from sentence_transformers import SentenceTransformer
from app.db.mongo import save_document
from app.utils.embedder import get_embedding

async def embed_and_store(file, username):
    if file.filename.endswith(".pdf"):
        with pdfplumber.open(file.file) as pdf:
            content = "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())
    else:
        content = await file.read()
        content = content.decode("utf-8", errors="ignore")

    if not content.strip():
        return "No text extracted."

    embedding = get_embedding(content)
    save_document(username, content, embedding)
