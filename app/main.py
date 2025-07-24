from fastapi import APIRouter,FastAPI, Query
from app.auth import send_otp, verify_otp
from app.jwt import create_access_token
from app.routers import otp

app = FastAPI()
app.include_router(otp.router)


