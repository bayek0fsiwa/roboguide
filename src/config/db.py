from sqlmodel import Session, SQLModel, create_engine

from .configs import settings

DATABASE_URL = settings.DATABASE_URL

if DATABASE_URL == "":
    raise NotImplementedError("DATABASE_URL needs to be set.")

engine = create_engine(DATABASE_URL)


def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
