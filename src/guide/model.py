from typing import Optional
from sqlmodel import SQLModel, Field


class GuideModel(SQLModel, table=True):
    __tablename__ = "guides"
    id: int = Field(default=None, primary_key=True)
    title: str = Field(nullable=False, index=True, unique=True)
    description: str = Field(nullable=False)
    author: str = Field(nullable=True)


class Guide(SQLModel, table=False):
    id: int
    title: str
    description: str
    author: Optional[str]

