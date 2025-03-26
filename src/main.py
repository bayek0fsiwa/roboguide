from contextlib import asynccontextmanager
from fastapi import FastAPI
from guide import router as guide_router
from config import db


@asynccontextmanager
async def lifespan(app: FastAPI):
    db.init_db()
    # before app starts
    yield
    # clean up


app = FastAPI(lifespan=lifespan)

app.include_router(guide_router, prefix="/guide")


@app.get("/health", status_code=200)
async def health_check():
    return {"status": "OK"}
