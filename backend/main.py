from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import db_engine, ModelBase
from routers import auth_routes, task_routes

ModelBase.metadata.create_all(bind=db_engine)

app = FastAPI(title="Task Manager API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_routes.router)
app.include_router(task_routes.router)