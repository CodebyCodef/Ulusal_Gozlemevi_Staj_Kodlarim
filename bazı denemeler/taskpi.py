from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

tasks = []

class Task(BaseModel):
    id: int
    title: str
    is_completed: bool = False

tasks: List[Task] = [
    Task(id=1, title="Deneme Çöz", is_completed=False),
    Task(id=2, title="Kitap OKU", is_completed=True),
]

@app.get("/api/tasks")
def get_tasks():
    """Tüm görevleri listele"""
    return {"tasks": tasks}

@app.put("/api/task/{task_id}")
def update(task_id: int, task: Task):
    """Görevi güncelle"""
    for t in tasks:
        if t.id == task_id:
            t.title = task.title
            t.is_completed = task.is_completed
            return {"message": "Task updated successfully", "task": t}
    return {"message": "Task not found"}, 404


@app.post("/api/task")
def create(task: Task):
    """Yeni görev ekle"""
    task.id = len(tasks) + 1  # ID otomatik oluştur
    tasks.append(task)
    return {"message": "Task created successfully", "task": task}