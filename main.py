from fastapi import FastAPI
from sqlmodel import Field, Session, create_engine, select, SQLModel
from router.router import user

app = FastAPI()

app.include_router(user)