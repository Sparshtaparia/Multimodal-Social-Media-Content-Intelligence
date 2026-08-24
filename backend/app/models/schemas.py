from pydantic import BaseModel, ConfigDict
from typing import List, Optional, Any
from datetime import datetime
from uuid import UUID

class DocumentBlockSchema(BaseModel):
    id: UUID
    page_number: Optional[int] = None
    block_type: Optional[str] = None
    text: Optional[str] = None
    bbox: Optional[Any] = None
    confidence: Optional[float] = None
    source: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

class MetadataProfileSchema(BaseModel):
    id: UUID
    language: Optional[str] = None
    content_type: Optional[str] = None
    word_count: Optional[int] = None
    character_count: Optional[int] = None
    sentence_count: Optional[int] = None
    hashtag_count: Optional[int] = None
    mention_count: Optional[int] = None
    url_count: Optional[int] = None
    emoji_count: Optional[int] = None
    text_block_count: Optional[int] = None
    image_block_count: Optional[int] = None
    text_area_ratio: Optional[float] = None
    image_area_ratio: Optional[float] = None
    readability_score: Optional[float] = None
    sentiment_score: Optional[float] = None
    model_config = ConfigDict(from_attributes=True)

class EngagementScoreSchema(BaseModel):
    id: UUID
    hook_score: Optional[float] = None
    clarity_score: Optional[float] = None
    specificity_score: Optional[float] = None
    cta_score: Optional[float] = None
    emotion_score: Optional[float] = None
    interaction_score: Optional[float] = None
    readability_score: Optional[float] = None
    overall_score: Optional[float] = None
    scoring_version: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

class RecommendationSchema(BaseModel):
    id: UUID
    category: str
    source: str
    problem: Optional[str] = None
    evidence: Optional[str] = None
    recommendation_text: str
    rewrite: Optional[str] = None
    confidence: Optional[float] = None
    supported: Optional[bool] = None
    model_config = ConfigDict(from_attributes=True)

class ProcessingRunSchema(BaseModel):
    id: UUID
    stage: str
    status: str
    message: Optional[str] = None
    started_at: datetime
    completed_at: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)

class DocumentResponseSchema(BaseModel):
    id: UUID
    filename: str
    file_type: str
    file_size: int
    status: str
    source_type: Optional[str] = None
    extraction_method: Optional[str] = None
    ocr_used: Optional[bool] = None
    page_count: Optional[int] = None
    processing_time_ms: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    
    blocks: List[DocumentBlockSchema] = []
    metadata_profile: Optional[MetadataProfileSchema] = None
    engagement_score: Optional[EngagementScoreSchema] = None
    recommendations: List[RecommendationSchema] = []
    processing_runs: List[ProcessingRunSchema] = []
    
    model_config = ConfigDict(from_attributes=True)

class AnalyzeResponseSchema(BaseModel):
    analysis_id: str
    status: str
