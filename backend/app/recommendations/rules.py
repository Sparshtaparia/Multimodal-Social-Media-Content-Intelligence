from typing import Dict, Any, List

def generate_rule_recommendations(
    metadata: Dict[str, Any],
    linguistic: Dict[str, Any],
    visual: Dict[str, Any],
    scores: Dict[str, Any],
    evidence: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    
    recommendations = []
    
    def get_priority(score: float) -> str:
        if score < 40:
            return "high"
        elif score < 60:
            return "medium"
        return "low"
        
    def find_evidence(signal_keywords: List[str]) -> str:
        for ev in evidence:
            for kw in signal_keywords:
                if kw in ev.get("signal", ""):
                    val = ev.get("value")
                    return f"{ev['signal']}: {val}" if val else ev['signal']
        return "No direct evidence found"

    # Weak CTA
    cta_score = scores.get("cta_score", 100)
    if cta_score < 50:
        recommendations.append({
            "category": "CTA",
            "source": "rule",
            "priority": get_priority(cta_score),
            "problem": "CTA is weak or missing.",
            "evidence": find_evidence(["cta", "missing_cta"]),
            "recommendation": "Strengthen the call-to-action by making the desired user action more specific and compelling.",
            "rewrite": None,
            "confidence": 1.0,
            "supported": True
        })

    # Low Interaction
    interaction_score = scores.get("interaction_score", 100)
    if interaction_score < 50:
        recommendations.append({
            "category": "Interaction",
            "source": "rule",
            "priority": get_priority(interaction_score),
            "problem": "Low interaction potential.",
            "evidence": find_evidence(["questions", "direct_audience"]),
            "recommendation": "Add a question, opinion prompt, or explicit participation trigger.",
            "rewrite": None,
            "confidence": 1.0,
            "supported": True
        })

    # Weak Hook
    hook_score = scores.get("hook_score", 100)
    if hook_score < 50:
        recommendations.append({
            "category": "Hook",
            "source": "rule",
            "priority": get_priority(hook_score),
            "problem": "Opening hook is weak.",
            "evidence": find_evidence(["opening", "headline"]),
            "recommendation": "Strengthen the opening with a more specific, audience-oriented, or curiosity-driven hook.",
            "rewrite": None,
            "confidence": 1.0,
            "supported": True
        })

    # Low Specificity
    specificity_score = scores.get("specificity_score", 100)
    if specificity_score < 50:
        recommendations.append({
            "category": "Specificity",
            "source": "rule",
            "priority": get_priority(specificity_score),
            "problem": "Content lacks specificity.",
            "evidence": find_evidence(["specificity", "numerical", "claims"]),
            "recommendation": "Replace generic claims with concrete numbers, outcomes, examples, or measurable benefits where appropriate.",
            "rewrite": None,
            "confidence": 1.0,
            "supported": True
        })

    # Low Clarity
    clarity_score = scores.get("clarity_score", 100)
    if clarity_score < 50:
        recommendations.append({
            "category": "Clarity",
            "source": "rule",
            "priority": get_priority(clarity_score),
            "problem": "Content is difficult to read or dense.",
            "evidence": find_evidence(["readability", "density"]),
            "recommendation": "Simplify sentence structure and make the main value proposition easier to understand.",
            "rewrite": None,
            "confidence": 1.0,
            "supported": True
        })

    # Weak Readability
    readability_score = scores.get("readability_score", 100)
    if readability_score < 50:
        recommendations.append({
            "category": "Readability",
            "source": "rule",
            "priority": get_priority(readability_score),
            "problem": "Readability score is low.",
            "evidence": find_evidence(["readability"]),
            "recommendation": "Reduce unnecessary complexity and improve sentence readability.",
            "rewrite": None,
            "confidence": 1.0,
            "supported": True
        })

    # Sort by priority: high > medium > low
    priority_order = {"high": 0, "medium": 1, "low": 2}
    recommendations.sort(key=lambda x: priority_order.get(x["priority"], 3))
    
    return recommendations[:5] # Limit to 5
