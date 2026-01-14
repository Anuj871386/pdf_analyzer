from fastapi import FastAPI, UploadFile, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, UploadFile, File
import shutil, os
from app.auth import router as auth_router
from app.routes.upload_pdf import router as upload_router

from app.auth import authenticate, create_token
from .pdf_utils import extract_text
from .gemini import analyze_text

os.makedirs("uploads", exist_ok=True)
os.makedirs("responses", exist_ok=True)

app = FastAPI()
oauth2 = OAuth2PasswordBearer(tokenUrl="login")
app.include_router(auth_router)
app.include_router(upload_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_headers=["*"],
    allow_methods=["*"]
)

@app.post("/login")
def login(data: dict):
    if authenticate(data["username"], data["password"]):
        token = create_token()
        return {
            "access_token": token,
            "token_type": "bearer"
        }
    raise HTTPException(status_code=401, detail="Invalid credentials")


@app.post("/upload")
def upload(file: UploadFile, token: str = Depends(oauth2)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(400, "PDF only")

    path = f"uploads/{file.filename}"
    with open(path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    text = extract_text(path)
    if not text.strip():
        raise HTTPException(
            status_code=400,
            detail="No readable text found in PDF (possibly scanned image-based PDF)"
    )
    response = analyze_text(text)

    out = f"responses/{file.filename}.txt"
    with open(out, "w", encoding="utf-8") as f:
        f.write(response)

    print(response)
    return {"status": "success", "output": out}


@app.post("/analyze-pdf")
async def analyze_pdf(file: UploadFile = File(...)):
    content = await file.read()

    extracted_text = f"PDF size: {len(content)} bytes"

    return {
        "message": "PDF uploaded successfully",
        "text": extracted_text
    }

