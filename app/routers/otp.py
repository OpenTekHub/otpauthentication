from fastapi import APIRouter, Query
from app.jwt import create_access_token
from app.auth import verify_otp, send_otp
router = APIRouter(prefix="/otp", tags=["Otp"])

@router.post("/send-otp")
def send_otp_route(phone: str = Query(...)):
    return send_otp(phone)

@router.post("/verify-otp")
def verify_otp_route(phone: str = Query(...), code: str = Query(...)):
    result = verify_otp(phone, code)
    if result["status"] == "approved":
        # ✅ OTP verified, generate token
        token = create_access_token({"phone": phone})
        return {"status": "approved", "access_token": token}
    return result