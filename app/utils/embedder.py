from app.core.config import GEMINI_API_KEY
from langchain_google_genai import GoogleGenerativeAIEmbeddings

def get_embedding(texts: str):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001",google_api_key=GEMINI_API_KEY)    
    return embeddings.embed_query(texts)
