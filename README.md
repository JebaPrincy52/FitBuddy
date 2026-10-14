# FitBuddy - AI Fitness Plan Generator

FitBuddy is a modular FastAPI application that uses Google's Gemini models to generate a seven-day workout plan, a concise nutrition/recovery tip, and feedback-based plan revisions. It uses Jinja2 templates for the interface and SQLAlchemy with SQLite for persistence.

## Setup

```powershell
python -m venv fitbuddy-env
.\fitbuddy-env\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Put a valid Google AI Studio key in `.env` as `GOOGLE_API_KEY`. The default workout and nutrition model is `gemini-3.8-flash`, which is more likely to have free-tier quota. Accounts with Pro access can set `GEMINI_PRO_MODEL=gemini-3.1-pro-preview`. If your account has different access, set the model variables to supported IDs. The app reports configuration or API errors and does not fabricate a plan.

## Run

```powershell
uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000, the admin view at `/view-all-users`, or interactive API docs at `/docs`. The SQLite database is created automatically as `fitbuddy.db` on startup.

## Project structure

`app/main.py` starts FastAPI; `app/routes.py` handles the documented routes; `app/database.py` owns SQLAlchemy persistence; `app/schemas.py` validates forms; `gemini_generator.py`, `gemini_flash_generator.py`, and `updated_plan.py` isolate Gemini responsibilities. HTML lives in `templates/`, styling and the fitness-themed SVG background in `static/`.

## Safety note

FitBuddy provides general fitness guidance, not medical advice. Users should adapt activity to their abilities and consult a qualified professional when appropriate.
