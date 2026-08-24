import re
from typing import List, Dict, Any

CTA_KEYWORDS = {
    "learn more", "try now", "sign up", "comment", "share", "follow", 
    "subscribe", "download", "get started", "visit", "buy now", 
    "click here", "read more"
}

def extract_hashtags(text: str) -> int:
    return len(re.findall(r"#\w+", text))

def extract_mentions(text: str) -> int:
    return len(re.findall(r"@\w+", text))

def extract_urls(text: str) -> int:
    # basic regex for urls
    return len(re.findall(r"(https?://[^\s]+)", text))

def extract_emojis(text: str) -> int:
    # very rough heuristic for emojis or just skip for now, but python demo:
    # A true emoji count requires emoji package, we'll try a unicode range heuristic
    emoji_pattern = re.compile(r"[\U00010000-\U0010ffff]", flags=re.UNICODE)
    return len(emoji_pattern.findall(text))

def detect_cta(text: str) -> bool:
    lower_text = text.lower()
    for kw in CTA_KEYWORDS:
        if kw in lower_text:
            return True
    return False

def generate_metadata_profile(blocks: List[Dict[str, Any]], extraction_metadata: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generates basic metadata profile (counts and structural detection).
    """
    full_text = " ".join([b['text'] for b in blocks if b['block_type'] == 'text' and b['text']])
    
    text_blocks = [b for b in blocks if b['block_type'] == 'text']
    image_blocks = [b for b in blocks if b['block_type'] == 'image']
    
    hashtag_count = extract_hashtags(full_text)
    mention_count = extract_mentions(full_text)
    url_count = extract_urls(full_text)
    emoji_count = extract_emojis(full_text)
    
    # We will determine the "Content Type" simply by rules for now, or leave it to Gemini later.
    # For now, default to "Unknown" or simple heuristics.
    content_type = "Promotional" if detect_cta(full_text) else "Informational"
    
    profile = {
        "content_type": content_type,
        "hashtag_count": hashtag_count,
        "mention_count": mention_count,
        "url_count": url_count,
        "emoji_count": emoji_count,
        "text_block_count": len(text_blocks),
        "image_block_count": len(image_blocks),
        "text_area_ratio": 0.0, # to be calculated by visual agent if needed
        "image_area_ratio": 0.0,
    }
    
    return profile
