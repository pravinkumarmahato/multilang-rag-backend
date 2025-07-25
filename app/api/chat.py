from fastapi import APIRouter, Depends
from app.models.schemas import ChatRequest, ChatResponse
from app.core.security import get_current_user
from app.db.mongo import save_chat_history, get_chat_history, get_user_documents
from app.utils.gemini import call_gemini

router = APIRouter()

@router.post("/", response_model=ChatResponse)
def chat(request: ChatRequest, username: str = Depends(get_current_user)):
    documents = get_user_documents(username, request.query)
    answer = call_gemini(request.query, documents)
    save_chat_history(username, request.query, answer)
    return ChatResponse(answer=answer)

@router.get("/history")
def history(username: str = Depends(get_current_user)):
    return get_chat_history(username)