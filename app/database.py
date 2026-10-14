"""SQLite persistence for FitBuddy users and workout plans."""
from datetime import datetime
from pathlib import Path
from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship, sessionmaker

BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_URL = f"sqlite:///{BASE_DIR / 'fitbuddy.db'}"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    username: Mapped[str] = mapped_column(String(120))
    age: Mapped[int] = mapped_column(Integer)
    weight: Mapped[float] = mapped_column(Float)
    goal: Mapped[str] = mapped_column(String(120))
    intensity: Mapped[str] = mapped_column(String(20))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    plans: Mapped[list["Plan"]] = relationship(back_populates="user", cascade="all, delete-orphan")

class Plan(Base):
    __tablename__ = "plans"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.user_id"), index=True)
    original_workout: Mapped[str] = mapped_column(Text)
    nutrition_tip: Mapped[str] = mapped_column(Text)
    updated_workout: Mapped[str | None] = mapped_column(Text, nullable=True)
    feedback: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    user: Mapped[User] = relationship(back_populates="plans")

def init_db() -> None:
    Base.metadata.create_all(bind=engine)

def save_user(data: dict) -> User:
    with SessionLocal() as session:
        user = session.query(User).filter_by(user_id=data["user_id"]).first()
        if user is None:
            user = User(**data)
            session.add(user)
        else:
            for key, value in data.items():
                setattr(user, key, value)
        session.commit()
        session.refresh(user)
        return user

def save_plan(user_id: str, workout: str, nutrition_tip: str) -> Plan:
    with SessionLocal() as session:
        plan = Plan(user_id=user_id, original_workout=workout, nutrition_tip=nutrition_tip)
        session.add(plan)
        session.commit()
        session.refresh(plan)
        return plan

def get_user(user_id: str) -> User | None:
    with SessionLocal() as session:
        return session.query(User).filter_by(user_id=user_id).first()

def get_original_plan(user_id: str) -> Plan | None:
    with SessionLocal() as session:
        return session.query(Plan).filter_by(user_id=user_id).order_by(Plan.created_at.desc()).first()

def update_plan(user_id: str, updated_workout: str, feedback: str) -> Plan | None:
    with SessionLocal() as session:
        plan = session.query(Plan).filter_by(user_id=user_id).order_by(Plan.created_at.desc()).first()
        if plan is None:
            return None
        plan.updated_workout = updated_workout
        plan.feedback = feedback
        plan.updated_at = datetime.utcnow()
        session.commit()
        session.refresh(plan)
        return plan

def get_all_users() -> list[User]:
    with SessionLocal() as session:
        return session.query(User).order_by(User.created_at.desc()).all()

def get_all_plans() -> list[Plan]:
    with SessionLocal() as session:
        return session.query(Plan).order_by(Plan.created_at.desc()).all()
