from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from app.core.security import get_current_user
from app.utils.vector import embed_and_store

router = APIRouter()

@router.post("/")
async def upload_doc(file: UploadFile = File(...), username: str = Depends(get_current_user)):
    await embed_and_store(file, username)
    return {"msg": "File uploaded and processed"}

