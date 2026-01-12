from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import get_db
from .. import models, schemas

router = APIRouter()

@router.get("")
def list_activities(db: Session = Depends(get_db)):
	activities = db.query(models.Activity).all()
	return activities

@router.post("", response_model=schemas.ActivityResponse)
def create_activity(activity: schemas.ActivityCreate, db: Session = Depends(get_db)):
	# Creamos la actividad
	new_activity = models.Activity(**activity.model_dump())
	db.add(new_activity)
	db.commit()
	db.refresh(new_activity)
	return new_activity

@router.get("/{activity_id}", response_model=schemas.ActivityResponse)
def get_activity(activity_id: int, db: Session = Depends(get_db)):
	activity = (db.query(models.Activity).filter(models.Activity.id == activity_id).first())
	if activity is None:
		raise HTTPException(status_code=404, detail="Activity not found")
	return activity

@router.delete("/{activity_id}")
def delete_activity(activity_id: int, db: Session = Depends(get_db)):
	activity = (db.query(models.Activity).filter(models.Activity.id == activity_id).first())
	if activity is None:
		raise HTTPException(status_code=404, detail="Activity not found")
	
	db.delete(activity)
	db.commit()
	return {"message": "Activity deleted"}

@router.put("{activity_id}", response_model=schemas.ActivityResponse)
def mod_activity(activity_id: int, activity_data: schemas.ActivityCreate, db: Session = Depends(get_db)):
	activity = (db.query(models.Activity).filter(models.Activity.id == activity_id).first())
	if activity is None:
		raise HTTPException(status_code=404, detail="Activity not found")
	#Actualizando campos
	for field, value in activity_data.model_dump().items():
		setattr(activity, field, value)

	db.commit()
	db.refresh(activity)
	
	return activity
	
@router.patch("/{activity_id}", response_model=schemas.ActivityResponse)
def patch_activity(
    activity_id: int,
    activity_data: schemas.ActivityCreate,
    db: Session = Depends(get_db)
):
    activity = db.query(models.Activity).filter(
        models.Activity.id == activity_id
    ).first()

    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")

	#La única diferencia con PUT se encuentra en la siguiente línea
    for field, value in activity_data.model_dump(exclude_unset=True).items():
        setattr(activity, field, value)

    db.commit()
    db.refresh(activity)
    return activity
