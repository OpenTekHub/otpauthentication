from fastapi import HTTPException
from twilio.rest import Client
from app.config import settings

client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

def send_otp(phone: str):
    try:
        verification = (
            client.verify.v2.services(settings.TWILIO_VERIFY_SERVICE_SID)
                  .verifications
                  .create(to=phone, channel="sms")
        )
        return {"status": verification.status}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def verify_otp(phone: str, code: str):
    try:
        verification_check = (
            client.verify
                  .services(settings.TWILIO_VERIFY_SERVICE_SID)
                  .verification_checks
                  .create(to=phone, code=code)
        )
        return {"status": verification_check.status}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))