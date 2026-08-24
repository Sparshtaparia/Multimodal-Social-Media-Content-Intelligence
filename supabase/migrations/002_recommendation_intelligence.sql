-- Create recommendations table
CREATE TABLE recommendations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    document_id UUID REFERENCES documents(id) ON DELETE CASCADE,
    category TEXT NOT NULL,
    source TEXT NOT NULL, -- 'rule', 'gemini', 'hybrid'
    priority TEXT NOT NULL, -- 'high', 'medium', 'low'
    problem TEXT NOT NULL,
    evidence TEXT NOT NULL,
    recommendation TEXT NOT NULL,
    rewrite TEXT,
    confidence FLOAT NOT NULL,
    supported BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
