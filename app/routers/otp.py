from fastapi import APIRouter, status , Depends
from app.jwt import create_access_token
from app.auth import verify_otp, send_otp
from app.models.database import get_user_by_phone, create_user, get_db
from app.schemas.otp_schemas import OTPRequest, OTPVerifyRequest
from app.schemas.user_schemas import UserCreate
from sqlalchemy.orm import Session

router = APIRouter(prefix="/otp", tags=["Otp"])

@router.post("/send-otp", status_code= status.HTTP_202_ACCEPTED)
def send_otp_route(data : OTPRequest):
    return send_otp(data.phone)

@router.post("/verify-otp", status_code=status.HTTP_200_OK)
def verify_otp_route(data: OTPVerifyRequest, db: Session = Depends(get_db)):
    result = verify_otp(data.phone, data.code)

    if result["status"] == "approved":
        existing_user = get_user_by_phone(db,data.phone)
        
        if existing_user:
            token = create_access_token({"phone": data.phone, "user_id": existing_user.id})
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

@router.post("/register",status_code=status.HTTP_201_CREATED)
def register_user(data: UserCreate, db: Session = Depends(get_db)):
    try:
        existing_user = get_user_by_phone(db,data.phone_number)
        if existing_user:
            return {"status": "error", "message": "User already exists with this phone number"}
        
        new_user = create_user(db,
            phone_number=data.phone_number,
            name=data.name,
            email=data.email
        )
        
        token = create_access_token({"phone": str(data.phone_number), "user_id": new_user.id})
        
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