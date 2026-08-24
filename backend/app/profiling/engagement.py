from typing import Dict, Any, List

def calculate_engagement_scores(metadata: Dict[str, Any], linguistic: Dict[str, Any], visual: Dict[str, Any], blocks: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Calculates deterministic heuristic engagement potential scores.
    Each score is normalized to 0-100.
    """
    evidence = []

    # --- 1. Hook Score ---
    # Based on first sentence, question presence, and headline position
    hook_score = 50.0
    first_sentence_length = 0
    if blocks:
        text_blocks = [b for b in blocks if b['block_type'] == 'text']
        if text_blocks:
            first_block = text_blocks[0]['text']
            first_sentence_length = len(first_block.split())
            if "?" in first_block:
                hook_score += 20
                evidence.append({"signal": "question_in_hook", "value": first_block[:50], "impact": "positive"})
            
            if first_sentence_length > 0 and first_sentence_length <= 15:
                hook_score += 15
                evidence.append({"signal": "punchy_opening", "value": f"{first_sentence_length} words", "impact": "positive"})
            elif first_sentence_length > 25:
                hook_score -= 10
                evidence.append({"signal": "long_opening", "value": f"{first_sentence_length} words", "impact": "negative"})
                
    if visual.get("headline_detected"):
        hook_score += 15
        evidence.append({"signal": "clear_headline", "impact": "positive"})
        
    hook_score = max(0, min(100, hook_score))

    # --- 2. Specificity Score ---
    # Based on numbers, percentages, etc. (we can heuristically count digits in the text)
    specificity_score = 40.0
    full_text = " ".join([b['text'] for b in blocks if b['block_type'] == 'text' and b['text']])
    digit_count = sum(c.isdigit() for c in full_text)
    if digit_count > 0:
        specificity_score += min(digit_count * 5, 40)
        evidence.append({"signal": "numerical_specificity", "value": f"{digit_count} digits detected", "impact": "positive"})
    
    # Check for specific symbols
    if "%" in full_text or "$" in full_text:
        specificity_score += 20
        evidence.append({"signal": "measurable_claims", "value": "Percentages or currency symbols detected", "impact": "positive"})
        
    specificity_score = max(0, min(100, specificity_score))

    # --- 3. CTA Score ---
    cta_score = 30.0
    if metadata.get("content_type") == "Promotional": # We set this to true if CTA keywords were found in Phase 2
        cta_score += 50.0
        evidence.append({"signal": "cta_keywords_detected", "impact": "positive"})
    else:
        evidence.append({"signal": "missing_cta", "impact": "negative"})
        
    cta_score = max(0, min(100, cta_score))

    # --- 4. Emotion Score ---
    # We map sentiment and exclamation points to a rough emotional activation score
    emotion_score = 40.0
    if linguistic.get("exclamation_count", 0) > 0:
        emotion_score += min(linguistic["exclamation_count"] * 10, 30)
        evidence.append({"signal": "exclamations", "value": linguistic["exclamation_count"], "impact": "positive"})
        
    # High negative or high positive sentiment indicates emotion
    sentiment = linguistic.get("sentiment_score", 0.0)
    if abs(sentiment) > 0.5:
        emotion_score += 30
        evidence.append({"signal": "strong_sentiment", "value": sentiment, "impact": "positive"})
        
    emotion_score = max(0, min(100, emotion_score))

    # --- 5. Interaction Score ---
    interaction_score = 30.0
    if linguistic.get("question_count", 0) > 0:
        interaction_score += 40
        evidence.append({"signal": "questions_asked", "value": linguistic["question_count"], "impact": "positive"})
    if linguistic.get("second_person_ratio", 0) > 0.01:
        interaction_score += 30
        evidence.append({"signal": "direct_audience_address", "value": linguistic["second_person_ratio"], "impact": "positive"})
        
    interaction_score = max(0, min(100, interaction_score))

    # --- 6. Clarity Score ---
    clarity_score = 50.0
    readability = linguistic.get("readability_score", 0)
    # Flesch reading ease: 60-70 is plain english, >70 is easy, <30 is very difficult
    if readability > 60:
        clarity_score += 30
        evidence.append({"signal": "good_readability", "value": readability, "impact": "positive"})
    elif readability > 0 and readability < 40:
        clarity_score -= 20
        evidence.append({"signal": "poor_readability", "value": readability, "impact": "negative"})
        
    if visual.get("text_density", 0) > 0.8:
        clarity_score -= 15
        evidence.append({"signal": "high_text_density", "impact": "negative"})
        
    clarity_score = max(0, min(100, clarity_score))
    
    # --- Overall Engagement Potential Score ---
    eps = (
        0.20 * hook_score +
        0.15 * clarity_score +
        0.15 * specificity_score +
        0.15 * emotion_score +
        0.20 * interaction_score +
        0.15 * cta_score
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
        "scoring_version": "1.0",
        "evidence": evidence
    }
