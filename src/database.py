from sqlalchemy import create_engine, DateTime, func
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column

from typing import List
from datetime import datetime

from pydantic import BaseModel, ConfigDict

# Database config
DATABASE_URL = 'sqlite:///src/database.db'

engine = create_engine(
    DATABASE_URL,
    connect_args={'check_same_thread': False}
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

# Dependencie for get the session of the db
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Database models
class PostDB(Base):
    __tablename__ = 'posts'
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str]
    content: Mapped[str]
    category: Mapped[str]
    tags: Mapped[List[str]]
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now(), 
        onupdate=func.now()
    )


# Pydantic schemas
class Post(BaseModel):
    title: str
    content: str
    category: str
    tags: List[str]

class PostResponse(Post):
    id: int
    created_at: datetime
    updated_at: datetime
        
    model_config = ConfigDict(from_attributes=True)