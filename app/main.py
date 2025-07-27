from fastapi import FastAPI
from app.routers import otp
from app.models.database import init_db
from app.utils.redis_conn import test_redis_connection

app = FastAPI()

@app.on_event("startup")
def startup():
    init_db()
    
    if test_redis_connection():
        print(" Redis connection successful!")
    else:
        print("Redis connection failed - rate limiting may not work")

app.include_router(otp.router)


