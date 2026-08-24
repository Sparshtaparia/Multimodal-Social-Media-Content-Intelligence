from typing import Dict, Any, List
import re
from app.llm.schemas import GeminiRecommendation

def validate_gemini_recommendations(
    gemini_recs: List[GeminiRecommendation], 
    scores: Dict[str, Any], 
    evidence: List[Dict[str, Any]],
    content: str
) -> List[Dict[str, Any]]:
    """
    Validates Gemini recommendations against deterministic scores and evidence.
    Returns dictionaries ready to be inserted into the DB with 'supported' flag.
    """
    validated = []
    
    for rec in gemini_recs:
        supported = True
        
        # Check 5 - Confidence
        if not (0.0 <= rec.confidence <= 1.0):
            supported = False
            
        # Check 2 & 4 - Score consistency & Unsupported facts
        category_lower = rec.category.lower()
        if "cta" in category_lower:
            if scores.get("cta_score", 100) > 80 and "weak" in rec.problem.lower():
                supported = False # Contradicts strong deterministic CTA score
                
        if "hook" in category_lower:
            if scores.get("hook_score", 100) > 80 and "weak" in rec.problem.lower():
                supported = False
                
        # Check 3 - Content grounding (very basic check, could be improved)
        # If it claims a rewrite but the original text doesn't exist at all, we might be cautious.
        # But for now, we just enforce that if it cites direct evidence, the evidence string should somewhat exist.
        if len(rec.evidence) > 5 and rec.evidence not in content and rec.evidence.lower() not in content.lower():
            # Sometimes Gemini paraphrases evidence. If it's a completely fabricated quote, flag it.
            # We'll be lenient if it overlaps with deterministic evidence.
            found_in_deterministic = any(rec.evidence.lower() in str(e).lower() for e in evidence)
            if not found_in_deterministic:
                supported = False
                
        # Check 6 - Rewrite validation (Hallucinated facts/numbers)
        if rec.rewrite:
            # Find all numbers in the rewrite
            rewrite_numbers = re.findall(r'\b\d+\b', rec.rewrite)
            # Find all numbers in the source content
            content_numbers = re.findall(r'\b\d+\b', content)
            
            # If the rewrite introduces a number not in the content (and not a generic "1" or "2" perhaps, but let's be strict for now)
            for num in rewrite_numbers:
                if num not in content_numbers:
                    supported = False
                    break
                    
        validated.append({
            "category": rec.category,
            "source": "gemini",
            "priority": "medium", # AI recs default to medium unless mapped
            "problem": rec.problem,
            "evidence": rec.evidence,
            "recommendation": rec.recommendation,
            "rewrite": rec.rewrite,
            "confidence": rec.confidence,
            "supported": supported
        })
        
    return validated
