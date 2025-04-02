from sqlmodel import SQLModel, Field


class AuthModel(SQLModel, table=True):
    __tablename__ = "auth"
    id: int = Field(default=None, primary_key=True)
    username: str = Field(nullable=False, index=True, unique=True)
    email: str = Field(nullable=False, unique=True, index=True)
    password: str = Field(nullable=False)


class Auth(SQLModel, table=False):
    id: int
    username: str
    email: str
