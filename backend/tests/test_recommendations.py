import pytest
from unittest.mock import patch
from app.recommendations.rules import generate_rule_recommendations
from app.agents.recommendation_agent import generate_final_recommendations
from app.llm.schemas import GeminiAnalysis, GeminiRecommendation

def test_weak_cta_generates_recommendation():
    scores = {"cta_score": 40}
    recs = generate_rule_recommendations({}, {}, {}, scores, [])
    assert any(r["category"] == "CTA" and "weak" in r["problem"].lower() for r in recs)

def test_low_interaction_generates_recommendation():
    scores = {"interaction_score": 30}
    recs = generate_rule_recommendations({}, {}, {}, scores, [])
    assert any(r["category"] == "Interaction" for r in recs)

def test_recommendation_priority_is_deterministic():
    scores = {"cta_score": 30, "hook_score": 45, "clarity_score": 80}
    recs = generate_rule_recommendations({}, {}, {}, scores, [])
    
    # CTA should be high, Hook medium, Clarity low/omitted (since >50 is omitted in our rules, but if it were there...)
    # We only generate recs for scores < 50
    assert len(recs) == 2
    assert recs[0]["category"] == "CTA"
    assert recs[0]["priority"] == "high"
    assert recs[1]["category"] == "Hook"
    assert recs[1]["priority"] == "medium"

@patch('app.agents.recommendation_agent.call_gemini_recommendations')
def test_valid_gemini_response(mock_gemini):
    mock_gemini.return_value = GeminiAnalysis(
        summary="A summary", strengths=[], recommendations=[
            GeminiRecommendation(
                category="CTA", problem="CTA is weak", evidence="Learn more", 
                recommendation="Be specific", rewrite="Buy now", confidence=0.9
            )
        ]
    )
    
    scores = {"cta_score": 40} # Rule will trigger CTA as well
    recs = generate_final_recommendations({}, {}, {}, scores, [{"signal": "cta", "value": "Learn more"}], [{"block_type": "text", "text": "Learn more"}])
    
    # Should hybridize
    assert any(r["source"] == "hybrid" and r["category"] == "CTA" for r in recs)

@patch('app.agents.recommendation_agent.call_gemini_recommendations')
def test_gemini_failure_falls_back_to_rules(mock_gemini):
    mock_gemini.return_value = None
    
    scores = {"cta_score": 40}
    recs = generate_final_recommendations({}, {}, {}, scores, [], [])
    
    assert any(r["source"] == "rule" and r["category"] == "CTA" for r in recs)
    assert not any(r["source"] == "gemini" for r in recs)

@patch('app.agents.recommendation_agent.call_gemini_recommendations')
def test_critic_rejects_unsupported_facts(mock_gemini):
    mock_gemini.return_value = GeminiAnalysis(
        summary="A summary", strengths=[], recommendations=[
            GeminiRecommendation(
                category="CTA", problem="CTA is weak", evidence="Some totally fake quote", 
                recommendation="Be specific", rewrite="Buy now", confidence=0.9
            )
        ]
    )
    
    # Empty content, so evidence doesn't match
    scores = {"cta_score": 90} # Also contradicts score
    recs = generate_final_recommendations({}, {}, {}, scores, [], [])
    
    # Should not be in final recs because it's unsupported
    assert not any(r["source"] == "gemini" and r["category"] == "CTA" for r in recs)
