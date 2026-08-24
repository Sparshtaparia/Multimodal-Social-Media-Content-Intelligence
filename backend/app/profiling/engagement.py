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
            first_block_data = text_blocks[0]
            first_block = first_block_data.get('text', '')
            first_sentence_length = len(first_block.split())
            
            block_provenance = {
                "block_id": first_block_data.get("id"),
                "page": first_block_data.get("page_number"),
                "bbox": first_block_data.get("bbox"),
                "source": first_block_data.get("source"),
                "text": first_block
            }
            
            if "?" in first_block:
                hook_score += 20
                evidence.append({"signal": "question_in_hook", "value": first_block[:50], "impact": "positive", **block_provenance})
            
            if first_sentence_length > 0 and first_sentence_length <= 15:
                hook_score += 15
                evidence.append({"signal": "punchy_opening", "value": f"{first_sentence_length} words", "impact": "positive", **block_provenance})
            elif first_sentence_length > 25:
                hook_score -= 10
                evidence.append({"signal": "long_opening", "value": f"{first_sentence_length} words", "impact": "negative", **block_provenance})
                
                
    if visual.get("headline_detected"):
        hook_score += 15
        evidence.append({"signal": "clear_headline", "impact": "positive"})
        
    hook_score = max(0, min(100, hook_score))

    # --- 2. Specificity Score ---
    # Based on numbers, percentages, etc. (we can heuristically count digits in the text)
    specificity_score = 40.0
    full_text = ""
    digit_count = 0
    spec_block_prov = {}
    for b in blocks:
        if b['block_type'] == 'text' and b.get('text'):
            full_text += b['text'] + " "
            if any(c.isdigit() for c in b['text']):
                digit_count += sum(c.isdigit() for c in b['text'])
                if not spec_block_prov:
                    spec_block_prov = {
                        "block_id": b.get("id"), "page": b.get("page_number"),
                        "bbox": b.get("bbox"), "source": b.get("source"), "text": b.get("text")
                    }

    if digit_count > 0:
        specificity_score += min(digit_count * 5, 40)
        evidence.append({"signal": "numerical_specificity", "value": f"{digit_count} digits detected", "impact": "positive", **spec_block_prov})
    
    # Check for specific symbols
    if "%" in full_text or "$" in full_text:
        specificity_score += 20
        evidence.append({"signal": "measurable_claims", "value": "Percentages or currency symbols detected", "impact": "positive", **spec_block_prov})
        
    # --- 3. CTA Score ---
    cta_score = 30.0
    
    # Find the block where CTA keywords are present
    cta_block_prov = {}
    if metadata.get("content_type") == "Promotional": # We set this to true if CTA keywords were found in Phase 2
        cta_score += 50.0
        # Try to find a block with a CTA keyword
        for b in blocks:
            if b['block_type'] == 'text' and b.get('text'):
                if any(kw in b['text'].lower() for kw in ["buy", "subscribe", "link in bio", "sign up", "learn more"]):
                    cta_block_prov = {
                        "block_id": b.get("id"), "page": b.get("page_number"),
                        "bbox": b.get("bbox"), "source": b.get("source"), "text": b.get("text")
                    }
                    break
        evidence.append({"signal": "cta_keywords_detected", "impact": "positive", **cta_block_prov})
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
