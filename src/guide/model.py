from sqlmodel import SQLModel, Field

from auth.model import Auth


class GuideModel(SQLModel, table=True):
    __tablename__ = "guides"
    id: int = Field(default=None, primary_key=True)
    title: str = Field(nullable=False, index=True, unique=True)
    description: str = Field(nullable=False)
    img: str = Field(nullable=False, default=None)
    author: str = Field(nullable=False, foreign_key="auth.cognito_id")


class Guide(SQLModel, table=False):
    id: int
    title: str
    description: str
    img: str
    author: str
