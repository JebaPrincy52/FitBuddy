"""Gemini Pro workout generation."""
import os

class GeminiConfigurationError(RuntimeError):
    pass

def _generate(prompt: str) -> str:
    api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise GeminiConfigurationError("Gemini is not configured. Add GOOGLE_API_KEY to your .env file and try again.")
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        # The model remains configurable as GEMINI_PRO_MODEL. The default Flash
        # fallback is intentional: many free-tier accounts have zero Pro quota.
        model = genai.GenerativeModel(os.getenv("GEMINI_PRO_MODEL", "gemini-3.8-flash"))
        response = model.generate_content(prompt)
        text = getattr(response, "text", None)
        if not text:
            raise RuntimeError("Gemini returned an empty response.")
        return text.strip()
    except GeminiConfigurationError:
        raise
    except Exception as exc:
        raise RuntimeError(f"Gemini workout generation failed: {exc}") from exc

def generate_workout_gemini(username: str, age: int, weight: float, goal: str, intensity: str) -> str:
    prompt = f"""You are a careful fitness programming assistant. Create a personalized 7-day workout plan.
User: {username}; age: {age}; weight: {weight} kg; goal: {goal}; intensity: {intensity}.
Return readable plain text with exactly seven labeled days. For every day include a focus, a 5-10 minute warm-up,
main exercises with sets and repetitions or duration, rest guidance, and cooldown/recovery guidance. Include rest or
active-recovery days where appropriate. Do not diagnose, prescribe, or claim medical certainty. Keep the plan practical."""
    return _generate(prompt)
