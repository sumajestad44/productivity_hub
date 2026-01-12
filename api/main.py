from fastapi import FastAPI
from .db import Base, engine
from . import models
from .routes import activities, tasks, reminders

# Crear tablas (por si no existen)
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(activities.router, prefix="/activities", tags=["Activities"])
app.include_router(tasks.router, prefix="/tasks", tags=["Tasks"])
app.include_router(reminders.router, prefix="/reminders", tags=["Reminders"])
