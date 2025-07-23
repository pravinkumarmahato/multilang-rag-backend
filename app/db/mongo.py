from pymongo import MongoClient
from app.core.config import MONGO_URL
from app.models.user import User
from app.utils.password_utils import get_password_hash
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from app.utils.embedder import get_embedding

client = MongoClient(MONGO_URL)
db = client["multilang-rag"]
users_col = db["users"]
chats_col = db["chats"]
docs_col = db["documents"]

print("Connected to MongoDB at", MONGO_URL)

def get_user_by_username(username):
    data = users_col.find_one({"username": username})
    return User(**data) if data else None

def get_user_by_email(email):
    data = users_col.find_one({"email": email})
    return User(**data) if data else None

def create_user(email, password, username):
    hashed = get_password_hash(password)
    users_col.insert_one({
        "username": username,
        "email": email,
        "hashed_password": hashed
        })

def save_chat_history(username, query, answer):
    chats_col.insert_one({"username": username, "query": query, "answer": answer})

def get_chat_history(username):
    return list(chats_col.find({"username": username}, {"_id": 0}))

def save_document(username, content, embedding):
    print(content, embedding)
    docs_col.insert_one({"username": username, "content": content, "embedding": embedding})
    print(docs_col)

def get_user_documents(username, query, top_k=3):
    query_embedding = np.array(get_embedding(query)).reshape(1, -1)
    all_docs = list(docs_col.find({"username": username}))
    if not all_docs:
        return []

    doc_embeddings = np.array([doc["embedding"] for doc in all_docs])
    similarities = cosine_similarity(query_embedding, doc_embeddings)[0]
    top_indices = similarities.argsort()[::-1][:top_k]
    return "\n\n".join([all_docs[i]["content"] for i in top_indices])