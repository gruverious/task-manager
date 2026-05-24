from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import models, schemas
from database import get_database
from auth import verify_token

router = APIRouter()

def get_current_user(token: str, db: Session):
    email = verify_token(token)

    if email is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user = db.query(models.User).filter(models.User.email == email).first()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user


@router.post("/tasks", response_model=schemas.TaskResponse, status_code=201)
def create_task(task_data: schemas.TaskCreate, token: str, db: Session = Depends(get_database)):
    current_user = get_current_user(token, db)

    new_task = models.Task(
        title=task_data.title,
        description=task_data.description,
        user_id=current_user.id
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task


@router.get("/tasks", response_model=list[schemas.TaskResponse])
def get_all_tasks(
    token: str,
    completed: Optional[bool] = Query(None, description="Filter by completion status"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=50, description="Tasks per page"),
    db: Session = Depends(get_database)
):
    current_user = get_current_user(token, db)

    query = db.query(models.Task).filter(models.Task.user_id == current_user.id)

    if completed is not None:
        query = query.filter(models.Task.completed == completed)

    offset = (page - 1) * limit
    tasks = query.offset(offset).limit(limit).all()

    return tasks


@router.get("/tasks/{task_id}", response_model=schemas.TaskResponse)
def get_task(task_id: int, token: str, db: Session = Depends(get_database)):
    current_user = get_current_user(token, db)

    task = db.query(models.Task).filter(
        models.Task.id == task_id,
        models.Task.user_id == current_user.id
    ).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return task


@router.put("/tasks/{task_id}", response_model=schemas.TaskResponse)
def update_task(task_id: int, task_data: schemas.TaskUpdate, token: str, db: Session = Depends(get_database)):
    current_user = get_current_user(token, db)

    task = db.query(models.Task).filter(
        models.Task.id == task_id,
        models.Task.user_id == current_user.id
    ).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task.completed = task_data.completed
    db.commit()
    db.refresh(task)

    return task


@router.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int, token: str, db: Session = Depends(get_database)):
    current_user = get_current_user(token, db)

    task = db.query(models.Task).filter(
        models.Task.id == task_id,
        models.Task.user_id == current_user.id
    ).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()

    return None