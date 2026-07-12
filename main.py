from fastapi import FastAPI, HTTPException, Depends
from schemas import TaskCreate   , TaskOut
from contextlib import asynccontextmanager
from database import engine, Base, get_db
from models import Task as TaskModel

import time
from sqlalchemy.exc import OperationalError

from typing import List
from sqlalchemy.orm import Session

@asynccontextmanager
async def lifespan(app: FastAPI):
    for attempt in range(5):
        try:
            Base.metadata.create_all(bind=engine)
            break
        except OperationalError as e:
            print(f"Попытка {attempt + 1} не удалась: {e}")
            time.sleep(2)
    else:
        raise RuntimeError("Не удалось подключиться к БД после 5 попыток")
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/")
def root():
    return {"message": "API works"}



@app.post("/tasks", response_model=TaskOut)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    new_task = TaskModel(title=task.title, description=task.description)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


@app.get("/tasks", response_model=List[TaskOut])
def get_tasks(db: Session = Depends(get_db)):
    return db.query(TaskModel).all()

@app.get("/tasks/{task_id}", response_model=TaskOut)
async def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.put("/tasks/{task_id}", response_model=TaskOut)
async def update_task(task_id: int, updated_task: TaskCreate, db: Session = Depends(get_db)):
    task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    task.title = updated_task.title
    task.description = updated_task.description
    db.commit()
    db.refresh(task)
    return task

@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return {"message": "Task deleted"}


