import pytest
from app.profiling.engagement import calculate_engagement_scores
from app.profiling.visual import generate_visual_profile

def test_visual_profile_bbox_area():
    blocks = [
        {"block_type": "text", "bbox": [10, 10, 110, 110]},  # 100x100 = 10000
        {"block_type": "image", "bbox": [0, 0, 200, 50]}     # 200x50 = 10000
    ]
    meta = {"page_width": 500, "page_height": 500} # 250000 area
    vp = generate_visual_profile(blocks, meta)
    
    assert vp["text_area"] == 10000.0
    assert vp["image_area"] == 10000.0
    assert vp["text_area_ratio"] == 0.04
    assert vp["text_density"] == 0.04
    assert vp["headline_detected"] is True  # Top 20% since y0=10 < 100

def test_engagement_strong_cta_increases_cta_score():
    blocks_no_cta = [{"block_type": "text", "text": "This is a post."}]
    scores_no_cta = calculate_engagement_scores(
        metadata={"content_type": "Informational"}, 
        linguistic={}, 
        visual={}, 
        blocks=blocks_no_cta
    )
    
    blocks_cta = [{"block_type": "text", "text": "This is a post. Buy now!"}]
    scores_cta = calculate_engagement_scores(
        metadata={"content_type": "Promotional"}, 
        linguistic={}, 
        visual={}, 
        blocks=blocks_cta
    )
    
    assert scores_cta["cta_score"] > scores_no_cta["cta_score"]

def test_question_increases_interaction_score():
    blocks = [{"block_type": "text", "text": "Do you like tests?"}]
    scores_no_q = calculate_engagement_scores(
        metadata={}, linguistic={"question_count": 0}, visual={}, blocks=blocks
    )
    
    scores_q = calculate_engagement_scores(
        metadata={}, linguistic={"question_count": 1}, visual={}, blocks=blocks
    )
    
    assert scores_q["interaction_score"] > scores_no_q["interaction_score"]
    
def test_specific_numbers_increase_specificity():
    blocks_no_num = [{"block_type": "text", "text": "This is a great product."}]
    scores_no_num = calculate_engagement_scores(metadata={}, linguistic={}, visual={}, blocks=blocks_no_num)
    
    blocks_num = [{"block_type": "text", "text": "This is 100% a great product."}]
    scores_num = calculate_engagement_scores(metadata={}, linguistic={}, visual={}, blocks=blocks_num)
    
    assert scores_num["specificity_score"] > scores_no_num["specificity_score"]

def test_readability_affects_clarity():
    blocks = [{"block_type": "text", "text": "text"}]
    scores_hard = calculate_engagement_scores(metadata={}, linguistic={"readability_score": 20}, visual={}, blocks=blocks)
    scores_easy = calculate_engagement_scores(metadata={}, linguistic={"readability_score": 80}, visual={}, blocks=blocks)
    
    assert scores_easy["clarity_score"] > scores_hard["clarity_score"]

def test_overall_score_is_normalized_and_deterministic():
    blocks = [{"block_type": "text", "text": "Buy now for 50% off! Do you want it?"}]
    ling = {"question_count": 1, "exclamation_count": 1, "readability_score": 65}
    meta = {"content_type": "Promotional"}
    vis = {"headline_detected": True, "text_density": 0.1}
    
    scores1 = calculate_engagement_scores(meta, ling, vis, blocks)
    scores2 = calculate_engagement_scores(meta, ling, vis, blocks)
    
    # Deterministic
    assert scores1 == scores2
    
    # Normalized bounds
    for k, v in scores1.items():
        if k.endswith("_score"):
            assert 0 <= v <= 100
            
    # Traceable evidence
    assert "evidence" in scores1
    assert len(scores1["evidence"]) > 0
