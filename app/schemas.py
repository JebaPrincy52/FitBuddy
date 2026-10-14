"""Validation schemas for FitBuddy."""
from pydantic import BaseModel, Field, field_validator

class UserInput(BaseModel):
    username: str = Field(min_length=1, max_length=120)
    user_id: str = Field(min_length=1, max_length=100)
    age: int = Field(ge=13, le=120)
    weight: float = Field(gt=0, le=500)
    goal: str = Field(min_length=2, max_length=120)
    intensity: str

    @field_validator("intensity")
    @classmethod
    def validate_intensity(cls, value: str) -> str:
        normalized = value.strip().lower()
        if normalized not in {"low", "medium", "high"}:
            raise ValueError("Intensity must be Low, Medium, or High.")
        return normalized

class FeedbackRequest(BaseModel):
    user_id: str = Field(min_length=1, max_length=100)
    feedback: str = Field(min_length=5, max_length=2000)
