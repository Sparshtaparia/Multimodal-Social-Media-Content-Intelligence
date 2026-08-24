import os
import json
from google import genai
from pydantic import ValidationError
from typing import Dict, Any, Optional

from app.llm.schemas import GeminiAnalysis

def call_gemini_recommendations(profile_payload: Dict[str, Any]) -> Optional[GeminiAnalysis]:
    """
    Calls the Gemini model using google-genai to generate recommendations.
    Returns structured GeminiAnalysis or None if failed.
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Gemini API key not found. Skipping AI recommendations.")
        return None
        
    model_name = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")
    
    try:
        client = genai.Client(api_key=api_key)
        
        prompt = f"""
        You are a multimodal social media content critic. Analyze the following extracted content profile and evidence.
        Ground every recommendation in the supplied content profile and evidence. If sufficient evidence does not exist, do not make the claim.
        DO NOT invent facts, statistics, metrics, or engagement performance.
        DO NOT override deterministic scores.
        
        Profile Payload:
        {json.dumps(profile_payload, indent=2)}
        """
        
        # We enforce structured output using Pydantic schema in the Google GenAI SDK
        response = client.models.generate_content(
            model=model_name,
            contents=prompt,
            config=genai.types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=GeminiAnalysis,
                temperature=0.2, # keep it deterministic
            )
        )
        
        # Parse the structured response back to Pydantic object
        if response.text:
            return GeminiAnalysis.model_validate_json(response.text)
            
    except Exception as e:
        print(f"Gemini API failure: {str(e)}")
        
    return None
