from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import models,schemas
from database import db_engine, get_database, ModelBase
from auth import hash_password,verify_password,create_access_token,verify_token

ModelBase.metadata.create_all(bind=db_engine)

app=FastAPI(title="Task Manager API",version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

def get_current_user(token:str,db:Session):
    email=verify_token(token)

    if email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

    user =db.query(models.User).filter(models.User.email==email).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return user 

# Authentication End points 

@app.post("/register",response_model=schemas.UserResponse,status_code=201)
def register(user_data:schemas.UserRegister,db:Session=Depends(get_database)):
    
    existing_email=db.query(models.User).filter(models.User.email==user_data.email).first()
    if existing_email:
        raise HTTPException(status_code=400,detail="Email already registered")
    
    existing_username=db.query(models.User).filter(models.User.username==user_data.username).first()
    if existing_username:
        raise HTTPException(status_code=400,detail="Username already taken")
    
    new_user=models.User(
        username=user_data.username,
        email=user_data.email,
        password=hash_password(user_data.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@app.post("/login",response_model=schemas.TokenResponse)
def login(user_data:schemas.UserLogin,db:Session=Depends(get_database)):

    user=db.query(models.User).filter(models.User.email==user_data.email).first()

    if not user or not verify_password(user_data.password,user.password):
        raise HTTPException(status_code=401,detail="Invalid email or password")
    
    token=create_access_token({"sub":user.email})

    return {"access_token":token,"token_type":"bearer"}


# Task Endpoints

@app.post("/tasks",response_model=schemas.TaskResponse,status_code=201)
def create_task(task_data:schemas.TaskCreate,token:str,db:Session=Depends(get_database)):
    current_user=get_current_user(token,db)

    new_task=models.Task(
        title=task_data.title,
        description=task_data.description,
        user_id=current_user.id
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task

@app.get("/tasks",response_model=list[schemas.TaskResponse])
def get_all_tasks(token:str,db:Session=Depends(get_database)):

    current_user=get_current_user(token,db)
    tasks=db.query(models.Task).filter(models.Task.user_id==current_user.id).all()
    return tasks

@app.get("/tasks/{task_id}",response_model=schemas.TaskResponse)
def get_task(task_id:int,token:str,db:Session=Depends(get_database)):

    current_user=get_current_user(token,db)
    task=db.query(models.Task).filter(
        models.Task.id==task_id,
        models.Task.user_id==current_user.id
    ).first()

    if not task:
        raise HTTPException(status_code=404,detail="Task not found")
    
    return task

@app.put("/tasks/{task_id}",response_model=schemas.TaskResponse)
def update_task(task_id:int,task_data:schemas.TaskUpdate,token:str,db:Session=Depends(get_database)):
    current_user=get_current_user(token,db)

    task=db.query(models.Task).filter(
        models.Task.id==task_id,
        models.Task.user_id==current_user.id
    ).first()

    if not task:
        raise HTTPException(status_code=404,detail="Task not found")
    
    task.completed=task_data.completed
    db.commit()
    db.refresh(task)

    return task

@app.delete("/tasks/{task_id}",status_code=204)
def delete_task(task_id:int,token:str,db:Session=Depends(get_database)):
    current_user=get_current_user(token,db)

    task=db.query(models.Task).filter(
        models.Task.id==task_id,
        models.Task.user_id==current_user.id
    ).first()

    if not task:
        raise HTTPException(status_code=404,detail="Task not found")
    
    db.delete(task)
    db.commit()

    return None

