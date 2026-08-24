import { AnalysisResult } from './types';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export async function analyzeFile(file: File): Promise<{ analysis_id: string; status: string }> {
  const formData = new FormData();
  formData.append('file', file);

  const response = await fetch(`${API_BASE_URL}/api/analyze`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => null);
    throw new Error(errorData?.detail || `Failed to analyze file (Status: ${response.status})`);
  }

  return response.json();
}

export async function getAnalysis(analysisId: string): Promise<AnalysisResult> {
  const response = await fetch(`${API_BASE_URL}/api/analysis/${analysisId}`, {
    method: 'GET',
  });

  if (!response.ok) {
    if (response.status === 404) {
      throw new Error('Analysis not found');
    }
    const errorData = await response.json().catch(() => null);
    throw new Error(errorData?.detail || `Failed to fetch analysis (Status: ${response.status})`);
  }

  return response.json();
}

export interface LibraryAnalysis {
  id: string;
  filename: string;
  file_type: string;
  status: string;
  created_at: string | null;
  overall_score: number | null;
  recommendation_count: number;
}

export async function fetchAnalyses(): Promise<{ analyses: LibraryAnalysis[] }> {
  const response = await fetch(`${API_BASE_URL}/api/analyses`, {
    method: 'GET',
    // In next.js app router, cache is typically used, but we'll fetch dynamic here:
    cache: 'no-store'
  });

  if (!response.ok) {
    throw new Error(`Failed to fetch analyses (Status: ${response.status})`);
  }

  return response.json();
}
