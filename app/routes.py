"""HTML routes and request processing for FitBuddy."""
from pathlib import Path
from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import ValidationError
from .database import get_all_plans, get_all_users, get_original_plan, get_user, save_plan, save_user, update_plan
from .gemini_flash_generator import generate_nutrition_tip_with_flash
from .gemini_generator import generate_workout_gemini
from .schemas import FeedbackRequest, UserInput
from .updated_plan import update_workout_plan

router = APIRouter()
templates = Jinja2Templates(directory=str(Path(__file__).resolve().parent.parent / "templates"))

def _error(request: Request, message: str, status_code: int = 400):
    return templates.TemplateResponse(request=request, name="index.html", context={"request": request, "error": message}, status_code=status_code)

@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(request=request, name="index.html", context={"request": request})

@router.post("/generate-workout", response_class=HTMLResponse)
def generate_workout(request: Request, username: str = Form(...), user_id: str = Form(...), age: int = Form(...), weight: float = Form(...), goal: str = Form(...), intensity: str = Form(...)):
    try:
        user_input = UserInput(username=username, user_id=user_id, age=age, weight=weight, goal=goal, intensity=intensity)
    except ValidationError as exc:
        return _error(request, exc.errors()[0]["msg"])
    try:
        data = user_input.model_dump()
        workout = generate_workout_gemini(
            username=user_input.username,
            age=user_input.age,
            weight=user_input.weight,
            goal=user_input.goal,
            intensity=user_input.intensity,
        )
        tip = generate_nutrition_tip_with_flash(user_input.goal)
        save_user(data)
        save_plan(user_input.user_id, workout, tip)
    except Exception as exc:
        return _error(request, str(exc), 503)
    return templates.TemplateResponse(request=request, name="result.html", context={"request": request, **data, "workout_plan": workout, "nutrition_tip": tip})

@router.post("/submit-feedback", response_class=HTMLResponse)
def submit_feedback(request: Request, user_id: str = Form(...), feedback: str = Form(...)):
    try:
        request_data = FeedbackRequest(user_id=user_id, feedback=feedback)
    except ValidationError as exc:
        return _error(request, exc.errors()[0]["msg"])
    user = get_user(request_data.user_id)
    plan = get_original_plan(request_data.user_id)
    if not user or not plan:
        return _error(request, "No saved plan was found for that User ID.", 404)
    try:
        revised = update_workout_plan(plan.original_workout, request_data.feedback)
        update_plan(request_data.user_id, revised, request_data.feedback)
    except Exception as exc:
        return _error(request, str(exc), 503)
    return templates.TemplateResponse(request=request, name="result.html", context={"request": request, "username": user.username, "user_id": user.user_id, "age": user.age, "weight": user.weight, "goal": user.goal, "intensity": user.intensity, "workout_plan": revised, "nutrition_tip": plan.nutrition_tip, "updated": True})

@router.get("/view-all-users", response_class=HTMLResponse)
def view_all_users(request: Request):
    plans_by_user = {}
    for plan in get_all_plans():
        plans_by_user.setdefault(plan.user_id, []).append(plan)
    return templates.TemplateResponse(request=request, name="all_users.html", context={"request": request, "users": get_all_users(), "plans_by_user": plans_by_user})
