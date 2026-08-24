-- Add evidence JSONB column to engagement_scores if it doesn't exist
ALTER TABLE engagement_scores ADD COLUMN IF NOT EXISTS evidence JSONB DEFAULT '[]'::jsonb;

-- Convert recommendation evidence to JSONB for better traceability
ALTER TABLE recommendations DROP COLUMN evidence;
ALTER TABLE recommendations ADD COLUMN evidence JSONB DEFAULT '[]'::jsonb;
ALTER TABLE recommendations ADD COLUMN evidence_block_id UUID REFERENCES documents(id) ON DELETE CASCADE;
ALTER TABLE recommendations ADD COLUMN evidence_page INTEGER;
