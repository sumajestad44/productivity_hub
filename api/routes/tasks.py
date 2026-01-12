from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..db import get_db
from .. import models

router = APIRouter()

@router.get("")
def list_tasks(db: Session = Depends(get_db)):
    tasks = db.query(models.Task).all()
    return tasks
from .. import schemas

@router.post("", response_model=schemas.TaskResponse)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    new_task = models.Task(**task.dict())
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

@router.patch("/{task_id}", response_model=schemas.TaskResponse)
def complete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        return {"error": "Task not found"}
    task.status = "done"
    db.commit()
    db.refresh(task)
    return task

@router.get("/pending")
def list_pending_tasks(db: Session = Depends(get_db)):
    tasks = db.query(models.Task).filter(models.Task.status == "pending").all()
    return tasks

@router.get("/done")
def list_done_tasks(db: Session = Depends(get_db)):
	tasks = db.query(models.Task).filter(models.Task.status == "done").all()
	return tasks

@router.delete("/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
	task = db.query(models.Task).filter(models.Task.id == task_id).first()
	if not task:
		return {"error": "Task not found"}
	db.delete(task)
	db.commit()
	return {"message": "Task deleted successfully"}

