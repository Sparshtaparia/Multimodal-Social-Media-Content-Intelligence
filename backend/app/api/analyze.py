import os
import shutil
import uuid
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from pathlib import Path

from app.db.session import get_db
from app.models.database import Document, ProcessingRun
from app.models.schemas import AnalyzeResponseSchema, DocumentResponseSchema
from app.pipeline.orchestrator import run_pipeline

router = APIRouter()

TEMP_UPLOAD_DIR = Path("temp_uploads")
TEMP_UPLOAD_DIR.mkdir(exist_ok=True)
MAX_FILE_SIZE_MB = int(os.getenv("MAX_FILE_SIZE_MB", 10))

ALLOWED_EXTENSIONS = {".pdf", ".png", ".jpg", ".jpeg", ".webp"}
ALLOWED_MIMETYPES = {
    "application/pdf",
    "image/png",
    "image/jpeg",
    "image/webp"
}

@router.post("/analyze", response_model=AnalyzeResponseSchema)
async def analyze_file(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # Validate file extension
    ext = Path(file.filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"Unsupported file extension. Allowed: {', '.join(ALLOWED_EXTENSIONS)}")

    # Validate mime type
    if file.content_type not in ALLOWED_MIMETYPES:
        raise HTTPException(status_code=400, detail="Unsupported MIME type.")

    # Read and validate size
    file_bytes = await file.read()
    file_size = len(file_bytes)
    if file_size > MAX_FILE_SIZE_MB * 1024 * 1024:
        raise HTTPException(status_code=400, detail=f"File exceeds maximum size of {MAX_FILE_SIZE_MB}MB.")
    
    if file_size == 0:
        raise HTTPException(status_code=400, detail="File is empty.")

    # Create temporary file
    temp_file_path = TEMP_UPLOAD_DIR / f"{uuid.uuid4()}{ext}"
    with open(temp_file_path, "wb") as buffer:
        buffer.write(file_bytes)

    # Determine type
    file_type = "pdf" if ext == ".pdf" else "image"

    # Create DB entry
    db_document = Document(
        filename=file.filename,
        file_type=file_type,
        file_size=file_size,
        status="UPLOADING"
    )
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    
    # Add initial processing run
    run = ProcessingRun(
        document_id=db_document.id,
        stage="UPLOAD",
        status="COMPLETED",
        message="File uploaded successfully"
    )
    db.add(run)
    
    # Update status to next phase
    db_document.status = "VALIDATING"
    db.commit()

    # Start background task for the pipeline
    background_tasks.add_task(run_pipeline, str(temp_file_path), db_document.id)

    return AnalyzeResponseSchema(
        analysis_id=str(db_document.id),
        status="PROCESSING"
    )

@router.get("/analysis/{analysis_id}", response_model=DocumentResponseSchema)
def get_analysis(analysis_id: uuid.UUID, db: Session = Depends(get_db)):
    document = db.query(Document).filter(Document.id == analysis_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Analysis not found")
    
    return document

@router.get("/analysis/{analysis_id}/status")
def get_analysis_status(analysis_id: uuid.UUID, db: Session = Depends(get_db)):
    document = db.query(Document).filter(Document.id == analysis_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Analysis not found")
    
    return {"analysis_id": str(document.id), "status": document.status}
