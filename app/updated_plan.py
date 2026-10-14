"""Gemini Pro feedback-based plan updates."""
from .gemini_generator import _generate

def update_workout_plan(original_plan: str, feedback: str) -> str:
    prompt = f"""Revise this 7-day workout plan using the user's feedback.
ORIGINAL PLAN:
{original_plan}
USER FEEDBACK:
{feedback}
Return a complete revised plan with exactly seven labeled days. Preserve useful details, apply the feedback clearly,
and keep warm-ups, exercise sets/reps or durations, rest guidance, and cooldown/recovery guidance. Do not diagnose or
make medical claims."""
    return _generate(prompt)
