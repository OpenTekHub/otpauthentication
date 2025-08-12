import time
from fastapi import HTTPException
from twilio.rest import Client
from app.config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_VERIFY_SERVICE_SID

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

last_otp_times = {}
COOLDOWN_PERIOD = 30

def send_otp(phone: str):
    current_time = time.time()
    last_sent_time = last_otp_times.get(phone)
    if last_sent_time and current_time - last_sent_time < COOLDOWN_PERIOD:
        wait_time = int(COOLDOWN_PERIOD - (current_time - last_sent_time))
        raise HTTPException(
            status_code=429,
            detail=f"OTP already sent. Please wait {wait_time} more seconds before retrying."
        )
    
    try:
        verification = client.verify.services(TWILIO_VERIFY_SERVICE_SID).verifications.create(
            to=phone, channel="sms"
        )
        last_otp_times[phone] = current_time
        return {"status": verification.status}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def verify_otp(phone: str, code: str):
    try:
        verification_check = client.verify.services(TWILIO_VERIFY_SERVICE_SID).verification_checks.create(
            to=phone, code=code
        )
        return {"status": verification_check.status}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))