import pytest
from unittest.mock import patch
import uuid
from app.agents.critic_agent import validate_gemini_recommendations
from app.llm.schemas import GeminiRecommendation
from app.profiling.engagement import calculate_engagement_scores

def test_evidence_contains_block_provenance():
    # Test engagement engine attaches block provenance
    blocks = [
        {"id": "b1", "block_type": "text", "text": "Are you struggling with productivity? We can help.", "page_number": 1, "bbox": [0,0,10,10], "source": "native_pdf"},
        {"id": "b2", "block_type": "text", "text": "Save 10 hours a week.", "page_number": 1, "bbox": [0,10,10,20], "source": "native_pdf"}
    ]
    
    scores = calculate_engagement_scores({}, {}, {}, blocks)
    
    # Check that hook score evidence points to b1
    hook_evidence = [e for e in scores["evidence"] if "hook" in e["signal"] or "opening" in e["signal"]]
    assert hook_evidence, "Expected hook evidence"
    
    for ev in hook_evidence:
        assert "block_id" in ev
        assert ev["block_id"] == "b1"
        assert ev["page"] == 1
        assert "bbox" in ev
        
    # Check that specificity points to b2
    spec_evidence = [e for e in scores["evidence"] if e["signal"] == "numerical_specificity"]
    assert spec_evidence, "Expected specificity evidence"
    assert spec_evidence[0]["block_id"] == "b2"


def test_gemini_rewrite_cannot_introduce_unsupported_numbers():
    # Test critic rejects hallucinations
    content = "Improve productivity with our AI platform."
    
    # Introduce a hallucinated 10
    recs = [
        GeminiRecommendation(
            category="CTA", problem="Weak", evidence="Improve productivity", 
            recommendation="Be specific", rewrite="Improve productivity by 10 hours every week.", confidence=0.9
        )
    ]
    
    validated = validate_gemini_recommendations(recs, {"cta_score": 30}, [], content)
    
    assert len(validated) == 1
    assert not validated[0]["supported"] # Should be False because 10 is hallucinated


def test_unsupported_rewrite_is_filtered_and_not_supported():
    content = "Save 5 hours a week."
    
    # Valid number
    recs = [
        GeminiRecommendation(
            category="CTA", problem="Weak", evidence="Save 5 hours", 
            recommendation="Be specific", rewrite="Save 5 hours every single week!", confidence=0.9
        )
    ]
    
    validated = validate_gemini_recommendations(recs, {"cta_score": 30}, [], content)
    assert validated[0]["supported"] # 5 is in the content


@patch('app.agents.recommendation_agent.call_gemini_recommendations')
def test_hybrid_recommendations_are_deduplicated(mock_gemini):
    # This was already tested in test_recommendations.py but we verify it's hybrid
    from app.agents.recommendation_agent import deduplicate_and_rank
    
    rule_recs = [
        {"category": "CTA", "priority": "high", "problem": "Weak", "recommendation": "Strengthen CTA", "confidence": 1.0}
    ]
    
    ai_recs = [
        {"category": "CTA", "priority": "medium", "problem": "Weak", "recommendation": "Use strong verbs", "rewrite": "Buy now", "confidence": 0.8, "supported": True}
    ]
    
    merged = deduplicate_and_rank(rule_recs, ai_recs)
    assert len(merged) == 1
    assert merged[0]["source"] == "hybrid"
    assert "Use strong verbs" in merged[0]["recommendation"]
