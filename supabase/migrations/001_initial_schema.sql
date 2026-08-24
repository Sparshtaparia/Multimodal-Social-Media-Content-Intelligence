-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 1. documents table
CREATE TABLE documents (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    filename TEXT NOT NULL,
    file_type TEXT NOT NULL,
    file_size BIGINT NOT NULL,
    status TEXT NOT NULL,
    source_type TEXT,
    extraction_method TEXT,
    ocr_used BOOLEAN DEFAULT false,
    page_count INTEGER,
    processing_time_ms BIGINT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- 2. document_blocks table
CREATE TABLE document_blocks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    document_id UUID NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    page_number INTEGER,
    block_type TEXT,
    text TEXT,
    bbox JSONB,
    confidence FLOAT,
    source TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

CREATE INDEX idx_document_blocks_document_id ON document_blocks(document_id);

-- 3. metadata_profiles table
CREATE TABLE metadata_profiles (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    document_id UUID NOT NULL REFERENCES documents(id) ON DELETE CASCADE UNIQUE,
    language TEXT,
    content_type TEXT,
    word_count INTEGER,
    character_count INTEGER,
    sentence_count INTEGER,
    hashtag_count INTEGER,
    mention_count INTEGER,
    url_count INTEGER,
    emoji_count INTEGER,
    text_block_count INTEGER,
    image_block_count INTEGER,
    text_area_ratio FLOAT,
    image_area_ratio FLOAT,
    readability_score FLOAT,
    sentiment_score FLOAT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- 4. engagement_scores table
CREATE TABLE engagement_scores (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    document_id UUID NOT NULL REFERENCES documents(id) ON DELETE CASCADE UNIQUE,
    hook_score FLOAT,
    clarity_score FLOAT,
    specificity_score FLOAT,
    cta_score FLOAT,
    emotion_score FLOAT,
    interaction_score FLOAT,
    readability_score FLOAT,
    overall_score FLOAT,
    scoring_version TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- 5. recommendations table
CREATE TABLE recommendations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    document_id UUID NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    category TEXT NOT NULL,
    source TEXT NOT NULL, -- e.g., 'rule-based', 'gemini'
    problem TEXT,
    evidence TEXT,
    recommendation TEXT NOT NULL,
    rewrite TEXT,
    confidence FLOAT,
    supported BOOLEAN,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

CREATE INDEX idx_recommendations_document_id ON recommendations(document_id);

-- 6. processing_runs table
CREATE TABLE processing_runs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    document_id UUID NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    stage TEXT NOT NULL,
    status TEXT NOT NULL,
    message TEXT,
    started_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,
    completed_at TIMESTAMP WITH TIME ZONE
);

CREATE INDEX idx_processing_runs_document_id ON processing_runs(document_id);

-- Add layout fields to metadata_profiles
ALTER TABLE metadata_profiles ADD COLUMN IF NOT EXISTS hashtag_count INTEGER DEFAULT 0;
ALTER TABLE metadata_profiles ADD COLUMN IF NOT EXISTS mention_count INTEGER DEFAULT 0;
ALTER TABLE metadata_profiles ADD COLUMN IF NOT EXISTS url_count INTEGER DEFAULT 0;
ALTER TABLE metadata_profiles ADD COLUMN IF NOT EXISTS emoji_count INTEGER DEFAULT 0;
ALTER TABLE metadata_profiles ADD COLUMN IF NOT EXISTS text_block_count INTEGER DEFAULT 0;
ALTER TABLE metadata_profiles ADD COLUMN IF NOT EXISTS image_block_count INTEGER DEFAULT 0;
ALTER TABLE metadata_profiles ADD COLUMN IF NOT EXISTS text_area_ratio FLOAT DEFAULT 0.0;
ALTER TABLE metadata_profiles ADD COLUMN IF NOT EXISTS image_area_ratio FLOAT DEFAULT 0.0;
ALTER TABLE metadata_profiles ADD COLUMN IF NOT EXISTS readability_score FLOAT DEFAULT 0.0;
ALTER TABLE metadata_profiles ADD COLUMN IF NOT EXISTS sentiment_score FLOAT DEFAULT 0.0;

-- Create engagement_scores table
CREATE TABLE engagement_scores (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    document_id UUID REFERENCES documents(id) ON DELETE CASCADE,
    hook_score FLOAT,
    clarity_score FLOAT,
    specificity_score FLOAT,
    cta_score FLOAT,
    emotion_score FLOAT,
    interaction_score FLOAT,
    readability_score FLOAT,
    overall_score FLOAT,
    scoring_version TEXT DEFAULT '1.0',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
