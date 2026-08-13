# ---------- IMPORTS ----------
# Built-in
from typing import Annotated

# FastAPI
from fastapi import FastAPI, Depends, HTTPException, status

# SQLAlchemy
from sqlalchemy.orm import Session
from sqlalchemy import select

# Pydantic
from pydantic import BaseModel

# Local
from database import get_db, engine, SessionLocal, Base
from database import PostCreate, PostResponse, PostDB

# Creating the tables in the DB
Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get('/')
def root():
    return 'Welcome to the API of your personal blog!'


@app.post('/posts', response_model=PostResponse)
def create_post(
    post: PostCreate,
    db: Session = Depends(get_db),
):
    new_post = PostDB(**post.model_dump())
    
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return new_post


@app.put('/posts/{post_id}')
def update_post(
    post_id: int,
    updated_post: PostCreate,
    db: Session = Depends(get_db)
):
    actual_post = db.execute(select(PostDB).where(PostDB.id == post_id)).scalars().one_or_none()
    if not actual_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='The post was not found'
        )
    
    data_updated_post = updated_post.model_dump(exclude_unset=True)
    
    for key, value in data_updated_post.items():
        setattr(actual_post, key, value)
    
    db.commit()
    db.refresh(actual_post)
    
    return actual_post


@app.delete('/posts/{post_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    post_id: int,
    db: Session = Depends(get_db)
):
    actual_post = db.execute(select(PostDB).where(PostDB.id == post_id)).scalars().one_or_none()
    if not actual_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='The post was not found'
        )
    
    db.delete(actual_post)
    db.commit()