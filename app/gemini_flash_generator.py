"""Gemini Flash nutrition and recovery tips."""
import os
from .gemini_generator import GeminiConfigurationError

def generate_nutrition_tip_with_flash(goal: str) -> str:
    api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise GeminiConfigurationError("Gemini is not configured. Add GOOGLE_API_KEY to your .env file and try again.")
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(os.getenv("GEMINI_FLASH_MODEL", "gemini-3.8-flash"))
        response = model.generate_content(f"Give one concise, practical nutrition or recovery tip for a person whose fitness goal is {goal}. Use 2-4 sentences, avoid medical claims, and do not provide a full meal plan.")
        text = getattr(response, "text", None)
        if not text:
            raise RuntimeError("Gemini returned an empty response.")
        return text.strip()
    except GeminiConfigurationError:
        raise
    except Exception as exc:
        raise RuntimeError(f"Gemini nutrition generation failed: {exc}") from exc
