from contextlib import asynccontextmanager
import pathlib
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from guide import router as guide_router
from config import db


BASE_DIR = pathlib.Path(__file__).cwd()
UPLOADS_DIR = BASE_DIR / "uploads"


@asynccontextmanager
async def lifespan(app: FastAPI):
    db.init_db()
    # before app starts
    yield
    # clean up


app = FastAPI(lifespan=lifespan)

app.include_router(guide_router, prefix="/guide", tags=["Guide"])


@app.get("/health", status_code=200)
async def health_check():
    return {"status": "OK"}


@app.get("/code/uploads/{media_name}")
async def imgs(req: Request):
    img_name = req.path_params["media_name"]
    img_path = f"{UPLOADS_DIR.name}/{img_name}"
    return FileResponse(img_path)
