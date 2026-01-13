from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import date, datetime

class TaskBase(BaseModel):
	title: str
	description: str | None = None

class TaskCreate(TaskBase):
	title: str
	description: Optional[str] = None
	due_date: date | None = None
	priority: Optional[str] = None

class TaskResponse(TaskBase):
	id: int

	class Config:
		orm_mode = True

class ActivityBase(BaseModel):
	name: str
	category: str
	duration: int

class ActivityCreate(ActivityBase):
	activity_date: date | None = None


class ActivityResponse(ActivityBase):
	id: int
	activity_date: date | None = None

	model_config = ConfigDict(from_attributes=True)

class ReminderBase(BaseModel):
	message: str
	remind_at: datetime
	completed: bool = False

class ReminderCreate(ReminderBase):
	pass

class ReminderUpdate(BaseModel):
	message: Optional[str] = None
	remind_at: Optional[datetime] = None
	completed: Optional[bool] = None


class ReminderResponse(ReminderBase):
	id: int
	completed: bool

	model_config = ConfigDict(from_attributes=True)
