import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, BigInteger, Boolean, Float, ForeignKey, DateTime, JSON
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship

from app.db.session import Base

class Document(Base):
    __tablename__ = "documents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    filename = Column(String, nullable=False)
    file_type = Column(String, nullable=False)
    file_size = Column(BigInteger, nullable=False)
    status = Column(String, nullable=False)
    source_type = Column(String)
    extraction_method = Column(String)
    ocr_used = Column(Boolean, default=False)
    page_count = Column(Integer)
    processing_time_ms = Column(BigInteger)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    blocks = relationship("DocumentBlock", back_populates="document", cascade="all, delete-orphan")
    metadata_profile = relationship("MetadataProfile", back_populates="document", uselist=False, cascade="all, delete-orphan")
    engagement_score = relationship("EngagementScore", back_populates="document", uselist=False, cascade="all, delete-orphan")
    recommendations = relationship("Recommendation", back_populates="document", cascade="all, delete-orphan")
    processing_runs = relationship("ProcessingRun", back_populates="document", cascade="all, delete-orphan")

class DocumentBlock(Base):
    __tablename__ = "document_blocks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_id = Column(UUID(as_uuid=True), ForeignKey("documents.id", ondelete="CASCADE"), nullable=False)
    page_number = Column(Integer)
    block_type = Column(String)
    text = Column(String)
    bbox = Column(JSONB) # Or JSON if sqlite fallback is needed
    confidence = Column(Float)
    source = Column(String)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)

    document = relationship("Document", back_populates="blocks")

class MetadataProfile(Base):
    __tablename__ = "metadata_profiles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_id = Column(UUID(as_uuid=True), ForeignKey('documents.id', ondelete='CASCADE'), unique=True)
    
    language = Column(String)
    content_type = Column(String)
    
    # Linguistic
    word_count = Column(Integer)
    character_count = Column(Integer)
    sentence_count = Column(Integer)
    
    # Heuristic counts
    hashtag_count = Column(Integer, default=0)
    mention_count = Column(Integer, default=0)
    url_count = Column(Integer, default=0)
    emoji_count = Column(Integer, default=0)
    
    # Layout
    text_block_count = Column(Integer, default=0)
    image_block_count = Column(Integer, default=0)
    text_area_ratio = Column(Float, default=0.0)
    image_area_ratio = Column(Float, default=0.0)
    
    # Scores
    readability_score = Column(Float, default=0.0)
    sentiment_score = Column(Float, default=0.0)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)

    document = relationship("Document", back_populates="metadata_profile")

class EngagementScore(Base):
    __tablename__ = "engagement_scores"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_id = Column(UUID(as_uuid=True), ForeignKey('documents.id', ondelete='CASCADE'), unique=True)
    
    hook_score = Column(Float)
    clarity_score = Column(Float)
    specificity_score = Column(Float)
    cta_score = Column(Float)
    emotion_score = Column(Float)
    interaction_score = Column(Float)
    readability_score = Column(Float)
    overall_score = Column(Float)
    scoring_version = Column(String, default="1.0")
    
    # Store evidence objects referencing DocumentBlocks
    evidence = Column(JSONB)
    
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)

    document = relationship("Document", back_populates="engagement_score")

class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_id = Column(UUID(as_uuid=True), ForeignKey("documents.id", ondelete="CASCADE"), nullable=False)
    
    category = Column(String, nullable=False)
    source = Column(String, nullable=False)
    priority = Column(String, nullable=False, default="medium")
    problem = Column(String)
    
    # JSON array of evidence items or single JSON object mapping to block UUID
    evidence = Column(JSONB)
    evidence_block_id = Column(UUID(as_uuid=True), ForeignKey("documents.id", ondelete="CASCADE"))
    evidence_page = Column(Integer)
    
    recommendation = Column(String, nullable=False)
    rewrite = Column(String)
    confidence = Column(Float)
    supported = Column(Boolean)
    
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)

    document = relationship("Document", back_populates="recommendations")

class ProcessingRun(Base):
    __tablename__ = "processing_runs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_id = Column(UUID(as_uuid=True), ForeignKey("documents.id", ondelete="CASCADE"), nullable=False)
    stage = Column(String, nullable=False)
    status = Column(String, nullable=False)
    message = Column(String)
    started_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    completed_at = Column(DateTime(timezone=True))

    document = relationship("Document", back_populates="processing_runs")



