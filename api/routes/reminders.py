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

@router.put("/{reminder_id}", response_model=schemas.ReminderResponse)
def update_reminder(reminder_id: int, reminder_data: schemas.ReminderCreate, db: Session = Depends(get_db)):
	reminder = db.query(models.Reminder).filter(models.Reminder.id == reminder_id).first()

	if reminder is None:
		raise HTTPException(status_code=404, detail="Reminder not found")

	reminder.message = reminder_data.message
	reminder.remind_at = reminder_data.remind_at
	reminder.completed = reminder_data.completed

	db.commit()
	db.refresh(reminder)
	return reminder

@router.patch("/{reminder_id}", response_model=schemas.ReminderResponse)
def patch_reminder(reminder_id: int, reminder_data: schemas.ReminderUpdate, db: Session = Depends(get_db)):
	reminder = db.query(models.Reminder).filter(models.Reminder.id == reminder_id).first()

	if reminder is None:
		raise HTTPException(status_code=404, detail="Reminder not found")

	update_data = reminder_data.model_dump(exclude_unset=True)

	for field, value in update_data.items():
		setattr(reminder, field, value)

	db.commit()
	db.refresh(reminder)
	return reminder

@router.delete("/{reminder_id}")
def delete_reminder(reminder_id: int, db: Session = Depends(get_db)):
	reminder = db.query(models.Reminder).filter(models.Reminder.id == reminder_id).first()

	if reminder is None:
		raise HTTPException(status_code=404, detail="Reminder not found")

	db.delete(reminder)
	db.commit()

	return {"detail": "Reminder deleted"}

