from typing import Dict, Any, List

from app.recommendations.rules import generate_rule_recommendations
from app.llm.client import call_gemini_recommendations
from app.agents.critic_agent import validate_gemini_recommendations

def deduplicate_and_rank(
    rule_recs: List[Dict[str, Any]], 
    ai_recs: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """
    Combines rule and AI recommendations.
    Deduplicates based on category/problem.
    If an AI rec matches a Rule rec category, we hybridize it to preserve the AI rewrite
    and insight, but keep the rule's authoritative priority and problem definition.
    """
    final_recs = []
    seen_categories = set()
    
    # Process rules first (they are authoritative)
    for rule in rule_recs:
        hybrid = dict(rule)
        category = rule["category"].lower()
        
        # Check if AI has a corresponding recommendation
        matching_ai = [a for a in ai_recs if a["supported"] and a["category"].lower() in category or category in a["category"].lower()]
        
        if matching_ai:
            best_ai = matching_ai[0]
            hybrid["source"] = "hybrid"
            # Enhance rule with AI insight/rewrite
            hybrid["recommendation"] = f"{rule['recommendation']} AI Insight: {best_ai['recommendation']}"
            hybrid["rewrite"] = best_ai.get("rewrite")
            hybrid["confidence"] = max(rule["confidence"], best_ai["confidence"])
            
            # Mark this category as covered
            seen_categories.add(best_ai["category"].lower())
            
        final_recs.append(hybrid)
        seen_categories.add(category)
        
    # Add any leftover supported AI recs that didn't match a rule
    for ai in ai_recs:
        if ai["supported"] and ai["category"].lower() not in seen_categories:
            final_recs.append(ai)
            seen_categories.add(ai["category"].lower())
            
    # Re-sort by priority: high > medium > low
    priority_order = {"high": 0, "medium": 1, "low": 2}
    final_recs.sort(key=lambda x: priority_order.get(x["priority"], 3))
    
    return final_recs[:5]

def generate_final_recommendations(
    metadata: Dict[str, Any],
    linguistic: Dict[str, Any],
    visual: Dict[str, Any],
    scores: Dict[str, Any],
    evidence: List[Dict[str, Any]],
    blocks: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    
    content = " ".join([b['text'] for b in blocks if b['block_type'] == 'text' and b['text']])
    
    rule_recs = generate_rule_recommendations(metadata, linguistic, visual, scores, evidence)
    
    profile_payload = {
        "content": content,
        "metadata": metadata,
        "linguistic": linguistic,
        "visual": visual,
        "engagement": scores,
        "evidence": evidence
    }
    
    gemini_analysis = call_gemini_recommendations(profile_payload)
    
    if gemini_analysis and gemini_analysis.recommendations:
        ai_recs = validate_gemini_recommendations(gemini_analysis.recommendations, scores, evidence, content)
    else:
        ai_recs = []
        
    return deduplicate_and_rank(rule_recs, ai_recs)
