from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import models
from .database import engine
from .routers import requests, simulate

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Raahat API", version="0.1.0")

# the dashboard runs on a dev server during the prototype, so any origin is fine for now
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(simulate.router)
app.include_router(requests.router)
