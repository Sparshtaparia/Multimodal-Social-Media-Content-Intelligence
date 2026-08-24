import uuid
import time
import os
import traceback
from datetime import datetime
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.database import Document, ProcessingRun, DocumentBlock, MetadataProfile, EngagementScore

from app.agents.document_agent import process_document
from app.profiling.metadata import generate_metadata_profile
from app.profiling.linguistic import calculate_linguistic_features
from app.profiling.visual import generate_visual_profile
from app.profiling.engagement import calculate_engagement_scores

def update_run_stage(db: Session, document_id: uuid.UUID, stage: str, status: str, message: str = None):
    run = ProcessingRun(
        document_id=document_id,
        stage=stage,
        status=status,
        message=message,
        completed_at=datetime.utcnow() if status in ["COMPLETED", "FAILED"] else None
    )
    db.add(run)
    db.commit()

def run_pipeline(temp_file_path: str, document_id: uuid.UUID):
    db: Session = SessionLocal()
    start_time = time.time()
    
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        db.close()
        return

    try:
        update_run_stage(db, document_id, "VALIDATING", "COMPLETED", "Validation successful")
        document.status = "EXTRACTING"
        db.commit()
        
        # --- PHASE 2: EXTRACTION ---
        blocks, extraction_metadata = process_document(temp_file_path, document.file_type)
        
        # Save blocks to DB
        for b in blocks:
            db_block = DocumentBlock(
                document_id=document.id,
                page_number=b.get("page_number"),
                block_type=b.get("block_type"),
                text=b.get("text"),
                bbox=b.get("bbox"),
                confidence=b.get("confidence"),
                source=b.get("source")
            )
            db.add(db_block)
            
        # Update document with extraction metadata
        document.ocr_used = extraction_metadata.get("ocr_used", False)
        document.extraction_method = extraction_metadata.get("extraction_method")
        document.page_count = extraction_metadata.get("page_count")
        
        update_run_stage(db, document_id, "EXTRACTING", "COMPLETED")
        document.status = "PROFILING"
        db.commit()

        # --- PHASE 2/3: PROFILING (Linguistic, Metadata, Visual) ---
        metadata_profile_data = generate_metadata_profile(blocks, extraction_metadata)
        
        full_text = " ".join([b['text'] for b in blocks if b['block_type'] == 'text' and b['text']])
        linguistic_profile_data = calculate_linguistic_features(full_text)
        
        visual_profile_data = generate_visual_profile(blocks, extraction_metadata)
        
        db_profile = MetadataProfile(
            document_id=document.id,
            language=linguistic_profile_data.get("language"),
            content_type=metadata_profile_data.get("content_type"),
            word_count=linguistic_profile_data.get("word_count"),
            character_count=linguistic_profile_data.get("character_count"),
            sentence_count=linguistic_profile_data.get("sentence_count"),
            hashtag_count=metadata_profile_data.get("hashtag_count"),
            mention_count=metadata_profile_data.get("mention_count"),
            url_count=metadata_profile_data.get("url_count"),
            emoji_count=metadata_profile_data.get("emoji_count"),
            text_block_count=metadata_profile_data.get("text_block_count"),
            image_block_count=metadata_profile_data.get("image_block_count"),
            text_area_ratio=visual_profile_data.get("text_area_ratio"),
            image_area_ratio=visual_profile_data.get("image_area_ratio"),
            readability_score=linguistic_profile_data.get("readability_score"),
            sentiment_score=linguistic_profile_data.get("sentiment_score")
        )
        db.add(db_profile)
        
        update_run_stage(db, document_id, "PROFILING", "COMPLETED")
        document.status = "SCORING"
        db.commit()

        # --- PHASE 3: SCORING ---
        scores = calculate_engagement_scores(
            metadata=metadata_profile_data,
            linguistic=linguistic_profile_data,
            visual=visual_profile_data,
            blocks=blocks
        )
        
        db_score = EngagementScore(
            document_id=document.id,
            hook_score=scores.get("hook_score"),
            clarity_score=scores.get("clarity_score"),
            specificity_score=scores.get("specificity_score"),
            cta_score=scores.get("cta_score"),
            emotion_score=scores.get("emotion_score"),
            interaction_score=scores.get("interaction_score"),
            readability_score=scores.get("readability_score"),
            overall_score=scores.get("overall_score"),
            scoring_version=scores.get("scoring_version")
        )
        db.add(db_score)
        
        update_run_stage(db, document_id, "SCORING", "COMPLETED")
        document.status = "GENERATING_RECOMMENDATIONS"
        db.commit()

        # TODO: Implement Rule-based Recommendations & Gemini Enhancement
        update_run_stage(db, document_id, "GENERATING_RECOMMENDATIONS", "COMPLETED")

        # Finally, completed
        document.status = "COMPLETED"
        document.processing_time_ms = int((time.time() - start_time) * 1000)
        db.commit()

    except Exception as e:
        error_msg = str(e)
        document.status = "FAILED"
        update_run_stage(db, document_id, "ERROR", "FAILED", error_msg)
        db.commit()
        print(f"Pipeline failed for {document_id}: {traceback.format_exc()}")
    finally:
        # Cleanup temp file
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        db.close()
