# ---------- IMPORTS ----------
# Built-in
from typing import Annotated

# FastAPI
from fastapi import FastAPI, Depends, HTTPException

# SQLAlchemy
from sqlalchemy.orm import Session

# Pydantic
from pydantic import BaseModel

# Local
from database import get_db, engine, SessionLocal, Base
from database import Post, PostResponse

# Creating the tables in the DB
Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get('/')
def root():
    return 'Welcome to the API of your personal blog!'


@app.post('/posts')
def create_post(
    post: Post,
    db: Session = Depends(get_db),
):
    ...