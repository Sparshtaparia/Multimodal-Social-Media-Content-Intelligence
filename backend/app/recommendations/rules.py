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
        
    def find_evidence(signal_keywords: List[str]) -> Dict[str, Any]:
        for ev in evidence:
            for kw in signal_keywords:
                if kw in ev.get("signal", ""):
                    return ev
        return {}

    # Helper to format rule recs
    def add_rule_rec(category, score, problem, recommendation, keywords):
        ev_dict = find_evidence(keywords)
        val = ev_dict.get("value")
        ev_str = f"{ev_dict['signal']}: {val}" if val else ev_dict.get('signal', 'No direct evidence found')
        
        recommendations.append({
            "category": category,
            "source": "rule",
            "priority": get_priority(score),
            "problem": problem,
            "evidence": ev_str,
            "evidence_json": [ev_dict] if ev_dict else [],
            "evidence_block_id": ev_dict.get("block_id"),
            "evidence_page": ev_dict.get("page"),
            "recommendation": recommendation,
            "rewrite": None,
            "confidence": 1.0,
            "supported": True
        })

    # Weak CTA
    cta_score = scores.get("cta_score", 100)
    if cta_score < 50:
        add_rule_rec("CTA", cta_score, "CTA is weak or missing.", "Strengthen the call-to-action by making the desired user action more specific and compelling.", ["cta", "missing_cta"])

    # Low Interaction
    interaction_score = scores.get("interaction_score", 100)
    if interaction_score < 50:
        add_rule_rec("Interaction", interaction_score, "Low interaction potential.", "Add a question, opinion prompt, or explicit participation trigger.", ["questions", "direct_audience"])

    # Weak Hook
    hook_score = scores.get("hook_score", 100)
    if hook_score < 50:
        add_rule_rec("Hook", hook_score, "Opening hook is weak.", "Strengthen the opening with a more specific, audience-oriented, or curiosity-driven hook.", ["opening", "headline"])

    # Low Specificity
    specificity_score = scores.get("specificity_score", 100)
    if specificity_score < 50:
        add_rule_rec("Specificity", specificity_score, "Content lacks specificity.", "Replace generic claims with concrete numbers, outcomes, examples, or measurable benefits where appropriate.", ["specificity", "numerical", "claims"])

    # Low Clarity
    clarity_score = scores.get("clarity_score", 100)
    if clarity_score < 50:
        add_rule_rec("Clarity", clarity_score, "Content is difficult to read or dense.", "Simplify sentence structure and make the main value proposition easier to understand.", ["readability", "density"])

    # Weak Readability
    readability_score = scores.get("readability_score", 100)
    if readability_score < 50:
        add_rule_rec("Readability", readability_score, "Readability score is low.", "Reduce unnecessary complexity and improve sentence readability.", ["readability"])

    # Sort by priority: high > medium > low
    priority_order = {"high": 0, "medium": 1, "low": 2}
    recommendations.sort(key=lambda x: priority_order.get(x["priority"], 3))
    
    return recommendations[:5] # Limit to 5
