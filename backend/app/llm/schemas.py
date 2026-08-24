from pydantic import BaseModel
from typing import List, Optional

class GeminiRecommendation(BaseModel):
    category: str
    problem: str
    evidence: str
    recommendation: str
    rewrite: Optional[str] = None
    confidence: float

class GeminiAnalysis(BaseModel):
    summary: str
    strengths: List[str]
    recommendations: List[GeminiRecommendation]
