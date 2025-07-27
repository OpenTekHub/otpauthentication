from fastapi import APIRouter, Query, Request, Depends
from app.jwt import create_access_token, verify_token
from app.auth import verify_otp, send_otp
from app.models.database import get_user_by_phone, create_user
from app.utils.rate_limiter import check_otp_rate_limit, get_client_ip

router = APIRouter(prefix="/otp", tags=["Otp"])

@router.post("/send-otp")
def send_otp_route(request: Request, phone: str = Query(...)):
    # Simple rate limiting: 3 OTP requests per 5 minutes
    client_ip = get_client_ip(request)
    check_otp_rate_limit(phone, client_ip, limit=5, window=300)
    
    return send_otp(phone)

@router.post("/verify-otp")
def verify_otp_route(request: Request, phone: str = Query(...), code: str = Query(...)):
    # Simple rate limiting: 5 verify attempts per 5 minutes
    client_ip = get_client_ip(request)
    check_otp_rate_limit(phone, client_ip, limit=8, window=300)
    
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
                }
            }
        else:
            registration_token = create_access_token({"phone": phone})
            return {
                "status": "approved",
                "message": "OTP verified. Please provide your name and email to complete registration.",
                "user_exists": False,
                "registration_token": registration_token
            }
    
    return {
        "status": result["status"],
        "message": result.get("message", "OTP verification failed"),
        "user_exists": False
    }

@router.post("/register", summary="Register new user", description="Requires Authorization header with registration token from OTP verification")
def register_user(name: str, email: str, payload: dict = Depends(verify_token)):
    try:
        phone_number = payload.get("phone")
        user_id = payload.get("user_id")
        
        if not phone_number:
            return {"status": "error", "message": "Invalid registration token"}
        
        # Check if token has user_id - existing users cannot register again - prevent registered user adding another users using their token
        if user_id:
            return {"status": "error", "message": "User already registered. Cannot register again."}
        
        existing_user = get_user_by_phone(phone_number)
        if existing_user:
            return {"status": "error", "message": "User already exists with this phone number"}
        
        new_user = create_user(
            phone_number=phone_number,
            name=name,
            email=email
        )
        
        return {
            "status": "registered",
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