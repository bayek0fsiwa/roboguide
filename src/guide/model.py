from sqlmodel import Field, SQLModel


class GuideModel(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    title: str = Field(nullable=False, index=True, unique=True)
    description: str = Field(nullable=False)
    img: str = Field(nullable=False, default=None)
    author: str | None = Field(
        default=None,
        nullable=False,
        foreign_key="authmodel.cognito_id",
        ondelete="CASCADE",
    )


class Guide(SQLModel, table=False):
    id: int
    title: str
    description: str
    img: str
    author: str
