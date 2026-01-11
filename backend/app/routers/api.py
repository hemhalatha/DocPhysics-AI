from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import FileResponse, JSONResponse
import shutil
import os
import uuid
from app.services.docx_service import extract_text_from_docx, apply_journal_formatting
from app.services.ai_service import ai_service
from app.core.config import settings

router = APIRouter()

# Ensure directories exist
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
os.makedirs(settings.PROCESSED_DIR, exist_ok=True)

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    # 1. Save File
    file_id = str(uuid.uuid4())
    filename = f"{file_id}_{file.filename}"
    file_path = os.path.join(settings.UPLOAD_DIR, filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    # 2. Extract Text
    try:
        text_content = extract_text_from_docx(file_path)
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": f"Error reading DOCX: {str(e)}"})

    # 3. Analyze with AI
    analysis_result = ai_service.analyze_document(text_content)
    
    # 4. Apply Formatting
    processed_filename = f"formatted_{filename}"
    processed_path = os.path.join(settings.PROCESSED_DIR, processed_filename)
    
    apply_journal_formatting(file_path, processed_path, analysis_result)
    
    return {
        "file_id": file_id,
        "original_filename": file.filename,
        "analysis": analysis_result,
        "download_url": f"/download/{processed_filename}"
    }

@router.get("/download/{filename}")
async def download_file(filename: str):
    file_path = os.path.join(settings.PROCESSED_DIR, filename)
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document', filename=filename)
    return JSONResponse(status_code=404, content={"message": "File not found"})
