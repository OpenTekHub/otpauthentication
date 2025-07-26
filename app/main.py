from fastapi import FastAPI
from app.routers import otp
from app.models.database import init_db

app = FastAPI()

@app.on_event("startup")
def startup():
    init_db()

app.include_router(otp.router)


