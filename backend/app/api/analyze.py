import os
import shutil
import uuid
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from pathlib import Path

from app.db.session import get_db
from app.models.database import Document, ProcessingRun, DocumentBlock
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

@router.get("/analysis/{analysis_id}")
def get_analysis(analysis_id: uuid.UUID, db: Session = Depends(get_db)) -> dict: # We return dict but will be cast to Any or AnalysisResultSchema ideally
    document = db.query(Document).filter(Document.id == analysis_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Analysis not found")
        
    result = {
        "analysis_id": str(document.id),
        "status": document.status,
        "document": {
            "filename": document.filename,
            "file_type": document.file_type,
            "file_size": document.file_size,
            "page_count": document.page_count
        },
        "processing": {
            "ocr_used": document.ocr_used,
            "extraction_method": document.extraction_method,
            "processing_time_ms": document.processing_time_ms
        },
        "extracted_blocks": []
    }
    
    blocks = db.query(DocumentBlock).filter(DocumentBlock.document_id == analysis_id).all()
    for b in blocks:
        result["extracted_blocks"].append({
            "id": str(b.id),
            "page_number": b.page_number,
            "block_type": b.block_type,
            "text": b.text,
            "bbox": b.bbox,
            "confidence": b.confidence,
            "source": b.source
        })
    
    if document.metadata_profile:
        mp = document.metadata_profile
        result["content_profile"] = {
            "language": mp.language,
            "content_type": mp.content_type,
            "word_count": mp.word_count,
            "character_count": mp.character_count,
            "sentence_count": mp.sentence_count,
            "hashtag_count": mp.hashtag_count,
            "mention_count": mp.mention_count,
            "url_count": mp.url_count,
            "emoji_count": mp.emoji_count,
            "readability_score": mp.readability_score,
            "sentiment_score": mp.sentiment_score
        }
        result["visual_profile"] = {
            "text_block_count": mp.text_block_count,
            "image_block_count": mp.image_block_count,
            "text_area_ratio": mp.text_area_ratio,
            "image_area_ratio": mp.image_area_ratio
        }
        
    if document.engagement_score:
        es = document.engagement_score
        result["engagement"] = {
            "overall_score": es.overall_score,
            "scoring_version": es.scoring_version,
            "components": {
                "hook_score": es.hook_score,
                "clarity_score": es.clarity_score,
                "specificity_score": es.specificity_score,
                "cta_score": es.cta_score,
                "emotion_score": es.emotion_score,
                "interaction_score": es.interaction_score,
                "readability_score": es.readability_score
            },
            "evidence": es.evidence or []
        }
        
    if document.recommendations:
        recs = []
        for r in document.recommendations:
            recs.append({
                "category": r.category,
                "source": r.source,
                "priority": r.priority,
                "problem": r.problem,
                "recommendation": r.recommendation,
                "rewrite": r.rewrite,
                "confidence": r.confidence,
                "supported": r.supported,
                "evidence": r.evidence or [],
                "evidence_block_id": str(r.evidence_block_id) if r.evidence_block_id else None,
                "evidence_page": r.evidence_page
            })
        result["recommendations"] = recs
    
    return result

@router.get("/analysis/{analysis_id}/status")
def get_analysis_status(analysis_id: uuid.UUID, db: Session = Depends(get_db)):
    document = db.query(Document).filter(Document.id == analysis_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Analysis not found")
    
    return {"analysis_id": str(document.id), "status": document.status}
