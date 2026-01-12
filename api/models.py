from sqlalchemy import Column, Integer, String, Date, DateTime, Boolean
from .db import Base

# ---------- SQLAlchemy MODELS (BD) ----------

class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    duration = Column(Integer, nullable=False)
    activity_date = Column(Date, nullable=True)


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    due_date = Column(Date, nullable=True)
    priority = Column(String, nullable=True)
    status = Column(String, default="pending")


class Reminder(Base):
    __tablename__ = "reminders"

    id = Column(Integer, primary_key=True, index=True)
    message = Column(String, nullable=False)
    remind_at = Column(DateTime, nullable=False)
    completed = Column(Boolean, default=False)
