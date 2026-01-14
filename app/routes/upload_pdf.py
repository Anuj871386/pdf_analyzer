from fastapi import APIRouter, UploadFile, File, Depends
from app.auth import get_current_user


router = APIRouter()

@router.post("/upload-pdf")
async def upload_pdf(
    file: UploadFile = File(...),
    user=Depends(get_current_user)
):
    if file.content_type != "application/pdf":
        return {"error": "Only PDF files allowed"}

    return {
        "filename": file.filename,
        "uploaded_by": user["username"],
        "status": "PDF uploaded successfully"
    }

