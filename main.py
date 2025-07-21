from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
from routes import router

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Backend API",
    description="FastAPI backend with MySQL database",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this based on your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router, prefix="/api", tags=["authentication"])
# app.include_router(friend_request_router, prefix="/api", tags=["friends"])
# app.include_router(chat_router, prefix="/api", tags=["chat"])
# app.include_router(chatdata_router, prefix="/api", tags=["chatdata"])

@app.get("/")
async def root():
    return {"message": "Welcome to FastAPI Backend!"}

# @app.get("/health")
# async def health_check():
#     return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
