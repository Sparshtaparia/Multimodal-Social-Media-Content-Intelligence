from typing import Dict, Any, List
import re

SCORING_VERSION = "1.1"

WEIGHTS = {
    "hook": 0.20,
    "clarity": 0.15,
    "specificity": 0.15,
    "emotion": 0.15,
    "interaction": 0.20,
    "cta": 0.15,
}

CTA_KEYWORDS = [
    "buy", "subscribe", "link in bio", "sign up", "learn more",
    "try it today", "get started", "download now", "book a demo",
    "explore", "discover", "join us", "shop now", "start free",
    "read more", "see how it works", "check it out", "get yours",
    "contact us", "swipe up", "visit our website", "try a simpler workflow"
]

def calculate_engagement_scores(metadata: Dict[str, Any], linguistic: Dict[str, Any], visual: Dict[str, Any], blocks: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Calculates deterministic heuristic engagement potential scores.
    Each score is normalized to 0-100.
    """
    evidence = []

    # Helper for provenance consistency
    def create_prov(b: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "block_id": b.get("id"),
            "page": b.get("page_number"),
            "bbox": b.get("bbox"),
            "source": b.get("source"),
            "text": b.get("text", "")[:100]  # snippet
        }

    # --- 1. Hook Score ---
    hook_score = 50.0
    text_blocks = [b for b in blocks if b.get('block_type') == 'text' and len(b.get('text', '').split()) > 0]
    
    # Identify headline/hook block (heuristically: first block with >3 words, or just the first text block)
    hook_block_data = None
    for b in text_blocks:
        if len(b.get('text', '').split()) > 3:
            hook_block_data = b
            break
    if not hook_block_data and text_blocks:
        hook_block_data = text_blocks[0]
        
    first_sentence_length = 0
    if hook_block_data:
        hook_text = hook_block_data.get('text', '')
        first_sentence_length = len(hook_text.split())
        block_prov = create_prov(hook_block_data)
        
        if "?" in hook_text:
            hook_score += 20
            evidence.append({"signal": "question_in_hook", "value": hook_text[:50], "impact": "positive", **block_prov})
        
        if 0 < first_sentence_length <= 15:
            hook_score += 15
            evidence.append({"signal": "punchy_opening", "value": f"{first_sentence_length} words", "impact": "positive", **block_prov})
        elif first_sentence_length > 25:
            hook_score -= 10
            evidence.append({"signal": "long_opening", "value": f"{first_sentence_length} words", "impact": "negative", **block_prov})

    if visual.get("headline_detected"):
        hook_score += 15
        evidence.append({"signal": "clear_headline", "impact": "positive", "scope": "document"})
        
    hook_score = max(0, min(100, hook_score))

    # --- 2. Specificity Score ---
    specificity_score = 40.0
    full_text = ""
    numerical_claims = 0
    spec_block_prov = {}
    
    for b in text_blocks:
        text = b.get('text', '')
        full_text += text + " "
        # Find numbers, percentages, or currency
        matches = re.findall(r'\b\d+(?:\.\d+)?%?\b|\$[\d\.]+', text)
        if matches:
            numerical_claims += len(matches)
            if not spec_block_prov:
                spec_block_prov = create_prov(b)

    if numerical_claims > 0:
        specificity_score += min(numerical_claims * 10, 40)
        evidence.append({"signal": "numerical_specificity", "value": f"{numerical_claims} numerical claims detected", "impact": "positive", **spec_block_prov})
    
    if "%" in full_text or "$" in full_text:
        specificity_score += 20
        # If we didn't get block prov from regex above, we just attach document scope
        prov = spec_block_prov if spec_block_prov else {"scope": "document"}
        evidence.append({"signal": "measurable_claims", "value": "Percentages or currency symbols detected", "impact": "positive", **prov})
        
    specificity_score = max(0, min(100, specificity_score))
    
    # --- 3. CTA Score ---
    cta_score = 30.0
    cta_block_prov = {}
    
    # Try to find a block with a CTA keyword
    cta_found = False
    for b in text_blocks:
        text_lower = b.get('text', '').lower()
        if any(kw in text_lower for kw in CTA_KEYWORDS):
            cta_block_prov = create_prov(b)
            cta_found = True
            break
            
    if cta_found:
        cta_score += 50.0
        evidence.append({"signal": "cta_keywords_detected", "impact": "positive", **cta_block_prov})
    else:
        evidence.append({"signal": "missing_cta", "impact": "negative", "scope": "document"})
        
    cta_score = max(0, min(100, cta_score))

    # --- 4. Emotional Activation Signals ---
    emotion_score = 40.0
    if linguistic.get("exclamation_count", 0) > 0:
        emotion_score += min(linguistic["exclamation_count"] * 10, 30)
        evidence.append({"signal": "exclamations", "value": linguistic["exclamation_count"], "impact": "positive", "scope": "document"})
        
    # Removed placeholder sentiment logic as it is hardcoded to 0.0 currently
    # sentiment = linguistic.get("sentiment_score", 0.0)
    # if abs(sentiment) > 0.5:
    #     emotion_score += 30
    #     evidence.append({"signal": "strong_sentiment", "value": sentiment, "impact": "positive", "scope": "document"})
        
    emotion_score = max(0, min(100, emotion_score))

    # --- 5. Interaction Score ---
    interaction_score = 30.0
    if linguistic.get("question_count", 0) > 0:
        interaction_score += 40
        evidence.append({"signal": "questions_asked", "value": linguistic["question_count"], "impact": "positive", "scope": "document"})
    if linguistic.get("second_person_ratio", 0) > 0.01:
        interaction_score += 30
        evidence.append({"signal": "direct_audience_address", "value": linguistic["second_person_ratio"], "impact": "positive", "scope": "document"})
        
    interaction_score = max(0, min(100, interaction_score))

    # --- 6. Clarity Score ---
    clarity_score = 50.0
    readability = linguistic.get("readability_score", 0)
    if readability > 60:
        clarity_score += 30
        evidence.append({"signal": "good_readability", "value": readability, "impact": "positive", "scope": "document"})
    elif readability > 0 and readability < 40:
        clarity_score -= 20
        evidence.append({"signal": "poor_readability", "value": readability, "impact": "negative", "scope": "document"})
        
    if visual.get("text_density", 0) > 0.8:
        clarity_score -= 15
        evidence.append({"signal": "high_text_density", "impact": "negative", "scope": "document"})
        
    clarity_score = max(0, min(100, clarity_score))
    
    # --- Overall Engagement Potential Score ---
    eps = (
        WEIGHTS["hook"] * hook_score +
        WEIGHTS["clarity"] * clarity_score +
        WEIGHTS["specificity"] * specificity_score +
        WEIGHTS["emotion"] * emotion_score +
        WEIGHTS["interaction"] * interaction_score +
        WEIGHTS["cta"] * cta_score
    )
    
    eps = round(max(0, min(100, eps)), 2)

    return {
        "hook_score": round(hook_score, 2),
        "clarity_score": round(clarity_score, 2),
        "specificity_score": round(specificity_score, 2),
        "cta_score": round(cta_score, 2),
        "emotion_score": round(emotion_score, 2),
        "interaction_score": round(interaction_score, 2),
        "readability_score": round(readability, 2),
        "overall_score": eps,
        "scoring_version": SCORING_VERSION,
        "evidence": evidence
    }
