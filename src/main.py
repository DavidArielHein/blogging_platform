# ---------- IMPORTS ----------
# Built-in
from typing import Annotated

# FastAPI
from fastapi import FastAPI, Depends, HTTPException, status

# SQLAlchemy
from sqlalchemy.orm import Session
from sqlalchemy import select, or_

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


# Get one post
@app.get('/posts/{post_id}', response_model=PostResponse)
def get_post(
    post_id: int,
    db: Session = Depends(get_db)
):
    post = db.execute(select(PostDB).where(PostDB.id == post_id)).scalars().one_or_none()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='The post was not found'
        )
    
    return post


# Get all posts
@app.get('/posts')
def get_all_posts(
    term: str | None = None,
    db: Session = Depends(get_db)
):
    if term:
        stmt = select(PostDB).where(
            PostDB.title.ilike(f'%{term}%') |
            PostDB.content.ilike(f'%{term}%') |
            PostDB.category.ilike(f'%{term}%')
        )
    else:
        stmt = select(PostDB)
    
    posts = db.scalars(stmt).all()
    if not posts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='No posts were found. Try another filter'
        )
    
    return posts


# Create a post
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


# Update a post
@app.put('/posts/{post_id}', response_model=PostResponse)
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


# Delete a post
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