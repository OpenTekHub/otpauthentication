from fastapi import APIRouter, status, Query
from app.auth import send_otp, verify_otp
from app.jwt import create_access_token
from app.schemas.otp import OTPRequest, OTPResponse
from app.schemas.token import Token

router = APIRouter(prefix="/otp", tags=["Otp"])

@router.post("/send-otp", response_model=OTPResponse, status_code=status.HTTP_202_ACCEPTED)
def send_otp_route(data: OTPRequest):
    """Trigger SMS OTP via Twilio Verify."""
    return send_otp(data.phone)

@router.post("/verify-otp", response_model=Token, status_code=status.HTTP_200_OK )
def verify_otp_route(phone: str = Query(..., example="+15551234567"), code: str = Query(..., example="123456")):
    """Verify SMS OTP and issue JWT token if approved."""
    result = verify_otp(phone, code)
    if result["status"] == "approved":
        token = create_access_token({"phone": phone})
        return {"status": "approved", "access_token": token, "token_type": "bearer"}
    return {"status": result["status"], "access_token": "", "token_type": "bearer"}

