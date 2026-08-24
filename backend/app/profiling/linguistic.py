import textstat
import re
from typing import Dict, Any, List

def calculate_linguistic_features(text: str) -> Dict[str, Any]:
    """
    Calculates linguistic features like readability, word count, sentence count.
    """
    if not text.strip():
        return {
            "word_count": 0,
            "character_count": 0,
            "sentence_count": 0,
            "readability_score": 0.0,
            "sentiment_score": 0.0,
            "question_count": 0,
            "exclamation_count": 0,
            "first_person_ratio": 0.0,
            "second_person_ratio": 0.0,
            "language": "unknown"
        }

    word_count = textstat.lexicon_count(text, removepunct=True)
    sentence_count = textstat.sentence_count(text)
    character_count = textstat.char_count(text)
    
    # Readability: Flesch Reading Ease (higher is easier)
    # We can normalize it or just store the raw score
    try:
        readability_score = textstat.flesch_reading_ease(text)
    except:
        readability_score = 0.0
        
    question_count = text.count("?")
    exclamation_count = text.count("!")
    
    # Simple heuristics for pronouns instead of heavy NLP for now
    first_person_words = {"i", "me", "my", "mine", "we", "us", "our", "ours"}
    second_person_words = {"you", "your", "yours"}
    
    words = re.findall(r'\b\w+\b', text.lower())
    
    fp_count = sum(1 for w in words if w in first_person_words)
    sp_count = sum(1 for w in words if w in second_person_words)
    
    fp_ratio = fp_count / word_count if word_count > 0 else 0.0
    sp_ratio = sp_count / word_count if word_count > 0 else 0.0
    
    # Sentiment heuristic (positive/negative words)
    # For a real implementation, we could use a lightweight sentiment dictionary or TextBlob
    # Here, we leave it at 0.0 as a baseline or use a very basic heuristic.
    
    return {
        "word_count": word_count,
        "character_count": character_count,
        "sentence_count": sentence_count,
        "readability_score": readability_score,
        "sentiment_score": 0.0, # Placeholder
        "question_count": question_count,
        "exclamation_count": exclamation_count,
        "first_person_ratio": round(fp_ratio, 4),
        "second_person_ratio": round(sp_ratio, 4),
        "language": "en" # Default heuristic for now
    }
