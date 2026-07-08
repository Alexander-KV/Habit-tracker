from fastapi import FastAPI, HTTPException
from schemas import TaskCreate   , TaskOut

app = FastAPI()

@app.get("/")
def root():
    return {"message": "API works"}

tasks = []
next_id = 1

@app.post("/tasks", response_model=TaskOut)
def create_task(task: TaskCreate):
    global next_id

    new_task = {
        "id": next_id,
        "title": task.title,
        "description": task.description,
        "completed": False,
    }

    tasks.append(new_task)
    next_id += 1

    return new_task

@app.get("/tasks")
def get_tasks():
    return tasks

@app.get("/tasks/{task_id}")
async def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")

@app.put("/tasks/{task_id}", response_model=TaskOut)
async def update_task(task_id: int, updated_task: TaskCreate):
    for task in tasks:
        if task["id"] == task_id:
            if task["title"] == updated_task.title:
                if task["description"] == updated_task.description:

                        return task
    raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)


            return {"message": "Task deleted"}
    raise HTTPException(status_code=404, detail="Task not found")


