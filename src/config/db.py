from decouple import config as decouple_config
from sqlmodel import Session, SQLModel, create_engine

DATABASE_URL = decouple_config("DATABASE_URL", default="")

if DATABASE_URL == "":
    raise NotImplementedError("DATABASE_URL needs to be set.")

engine = create_engine(DATABASE_URL)


def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
