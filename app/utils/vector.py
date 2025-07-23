from langchain.document_loaders import PyPDFLoader
from app.db.mongo import save_document
from app.utils.embedder import get_embedding
import tempfile

async def embed_and_store(file, username):
    # Write uploaded file to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        contents = await file.read()
        tmp.write(contents)
        tmp_path = tmp.name  # Get the temp file path

    pdf_loader = PyPDFLoader(tmp_path)
    pages = pdf_loader.load_and_split()
    context = "\n\n".join(str(p.page_content) for p in pages)
    embedding = get_embedding(context)
    save_document(username, context, embedding)
