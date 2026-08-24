export interface DocumentInfo {
  filename: string;
  file_type: string;
  file_size: number;
  page_count?: number;
}

export interface ProcessingInfo {
  ocr_used: boolean;
  extraction_method?: string;
  processing_time_ms?: number;
}

export interface ContentProfile {
  language?: string;
  content_type?: string;
  word_count?: number;
  character_count?: number;
  sentence_count?: number;
  hashtag_count?: number;
  mention_count?: number;
  url_count?: number;
  emoji_count?: number;
  readability_score?: number;
  sentiment_score?: number;
}

export interface VisualProfile {
  text_block_count?: number;
  image_block_count?: number;
  text_area_ratio?: number;
  image_area_ratio?: number;
}

export interface Evidence {
  signal: string;
  value?: string | number;
  impact: string;
  block_id?: string;
  page?: number;
  bbox?: number[];
  source?: string;
  text?: string;
}

export interface EngagementComponents {
  hook_score: number;
  clarity_score: number;
  specificity_score: number;
  cta_score: number;
  emotion_score: number;
  interaction_score: number;
  readability_score: number;
}

export interface Engagement {
  overall_score: number;
  scoring_version: string;
  components: EngagementComponents;
  evidence: Evidence[];
}

export interface Recommendation {
  category: string;
  source: string;
  priority: string;
  problem: string;
  recommendation: string;
  rewrite?: string;
  confidence: number;
  supported: boolean;
  evidence: Evidence[];
  evidence_block_id?: string;
  evidence_page?: number;
}

export interface ExtractedBlock {
  id: string;
  page_number?: number;
  block_type: string;
  text?: string;
  confidence?: number;
  source?: string;
}

export interface AnalysisResult {
  analysis_id: string;
  status: string;
  document: DocumentInfo;
  processing: ProcessingInfo;
  content_profile?: ContentProfile;
  visual_profile?: VisualProfile;
  engagement?: Engagement;
  recommendations?: Recommendation[];
  extracted_blocks?: ExtractedBlock[];
}
