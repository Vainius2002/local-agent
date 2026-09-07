from fastapi import FastAPI
from app.routes import ask
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.include_router(ask.router)

app.mount("/static", StaticFiles(directory="app/static"), name="static")




