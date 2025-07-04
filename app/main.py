from fastapi import FastAPI, Query
from app.auth import send_otp, verify_otp
from app.jwt import create_access_token

app = FastAPI()

@app.post("/send-otp")
def send_otp_route(phone: str = Query(...)):
    return send_otp(phone)

@app.post("/verify-otp")
def verify_otp_route(phone: str = Query(...), code: str = Query(...)):
    result = verify_otp(phone, code)
    if result["status"] == "approved":
        # ✅ OTP verified, generate token
        token = create_access_token({"phone": phone})
        return {"status": "approved", "access_token": token}
    return result