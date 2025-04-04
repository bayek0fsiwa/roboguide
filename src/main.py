from contextlib import asynccontextmanager
import pathlib
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from guide import router as guide_router
from auth.controller import router as auth_router
from config import db


BASE_DIR = pathlib.Path(__file__).cwd()
UPLOADS_DIR = BASE_DIR / "uploads"


@asynccontextmanager
async def lifespan(app: FastAPI):
    db.init_db()
    yield


app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost:9000",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(guide_router, prefix="/guide", tags=["Guide"])
app.include_router(auth_router, prefix="/auth", tags=["Auth"])


@app.get("/health", status_code=200)
async def health_check():
    return {"status": "OK"}


@app.get("/code/uploads/{media_name}")
async def imgs(req: Request):
    img_name = req.path_params["media_name"]
    img_path = f"{UPLOADS_DIR.name}/{img_name}"
    return FileResponse(img_path)
