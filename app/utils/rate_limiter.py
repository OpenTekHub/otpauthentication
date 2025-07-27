import time
from fastapi import HTTPException, Request
from app.utils.redis_conn import redis_client

def get_client_ip(request: Request) -> str:
    if hasattr(request.client, "host"):
        return request.client.host
    return "unknown"

def check_otp_rate_limit(phone: str, client_ip: str, limit: int = 3, window: int = 300):
    try:
        key = f"otp_limit:{client_ip}:{phone}"
        current_count = redis_client.get(key)
        
        if current_count and int(current_count) >= limit:
            raise HTTPException(
                status_code=429,
                detail={"error": "Too many OTP requests. Please try again in 5 minutes."}
            )
        
        # Increment counter
        if current_count:
            redis_client.incr(key)
        else:
            redis_client.setex(key, window, 1)  # Set with expiry
            
    except HTTPException:
        raise
    except Exception as e:
        print(f"Rate limiter error: {e}")
