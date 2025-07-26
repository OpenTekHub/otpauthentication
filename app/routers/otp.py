from fastapi import APIRouter, Query
from app.jwt import create_access_token
from app.auth import verify_otp, send_otp
from app.models.database import get_user_by_phone, create_user

router = APIRouter(prefix="/otp", tags=["Otp"])

@router.post("/send-otp")
def send_otp_route(phone: str = Query(...)):
    return send_otp(phone)

@router.post("/verify-otp")
def verify_otp_route(phone: str = Query(...), code: str = Query(...)):
    result = verify_otp(phone, code)

    if result["status"] == "approved":
        existing_user = get_user_by_phone(phone)
        
        if existing_user:
            token = create_access_token({"phone": phone, "user_id": existing_user.id})
            return {
                "status": "approved",
                "access_token": token,
                "message": f"Welcome back, {existing_user.name}!",
                "user_exists": True,
                "user": {
                    "id": existing_user.id,
                    "phone_number": existing_user.phone_number,
                    "name": existing_user.name,
                    "email": existing_user.email
                }
            }
        else:
            return {
                "status": "approved",
                "message": "OTP verified. Please provide your name and email to complete registration.",
                "user_exists": False
            }
    
    return {
        "status": result["status"],
        "message": result.get("message", "OTP verification failed"),
        "user_exists": False
    }

@router.post("/register")
def register_user(phone_number: str, name: str, email: str):
    try:
        existing_user = get_user_by_phone(phone_number)
        if existing_user:
            return {"status": "error", "message": "User already exists with this phone number"}
        
        new_user = create_user(
            phone_number=phone_number,
            name=name,
            email=email
        )
        
        token = create_access_token({"phone": str(phone_number), "user_id": new_user.id})
        
        return {
            "status": "registered",
            "access_token": token,
            "message": f"Welcome {new_user.name}! Your account has been created successfully.",
            "user": {
                "id": new_user.id,
                "phone_number": new_user.phone_number,
                "name": new_user.name,
                "email": new_user.email
            }
        }
        
    except Exception as e:
        return {"status": "error", "message": f"Failed to register user: {str(e)}"}