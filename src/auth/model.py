from sqlmodel import Field, SQLModel


class AuthModel(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    cognito_id: str = Field(default=None, index=True, unique=True)
    name: str = Field(nullable=False, unique=False)
    email: str = Field(nullable=False, unique=True, index=True)
    password: str = Field(nullable=False)
