from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.auth import router as auth_router
from app.api.chat import router as chat_router
from app.api.upload import router as upload_router

app = FastAPI(title="Multilingual RAG")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(chat_router, prefix="/chat", tags=["Chat"])
app.include_router(upload_router, prefix="/upload", tags=["Upload"])

@app.get("/")
def read_root():
    return {"msg": "Multilingual RAG backend running"}