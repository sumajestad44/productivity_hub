from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import get_db
from .. import models, schemas

router = APIRouter()

@router.get("")
def list_reminders(db: Session = Depends(get_db)):
    reminders = db.query(models.Reminder).all()
    return reminders

@router.post("", response_model=schemas.ReminderResponse)
def create_reminder(reminder: schemas.ReminderCreate, db: Session = Depends(get_db)):
	new_reminder = models.Reminder(**reminder.model_dump())
	db.add(new_reminder)
	db.commit()
	db.refresh(new_reminder)
	return new_reminder

@router.get("/{reminder_id}")
def get_reminder(reminder_id: int, db: Session = Depends(get_db)):
	reminder = db.query(models.Reminder).filter(models.Reminder.id == reminder_id).first()
	if reminder is None:
		raise HTTPException(status_code=404, detail="Reminder not found")
	return reminder
