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
