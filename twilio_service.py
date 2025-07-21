from twilio.rest import Client
import os
from dotenv import load_dotenv

load_dotenv()

class TwilioService:
    def __init__(self):
        self.account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        self.auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        self.from_phone = os.getenv("TWILIO_PHONE_NUMBER")
        
        if not all([self.account_sid, self.auth_token, self.from_phone]):
            print("Warning: Twilio credentials not found in environment variables")
            self.client = None
        else:
            self.client = Client(self.account_sid, self.auth_token)
    
    def send_otp_sms(self, to_phone: str, otp: str) -> bool:
        """Send OTP via SMS using Twilio"""
        if not self.client:
            print(f"Twilio not configured. OTP for {to_phone}: {otp}")
            return False
        
        try:
            # Ensure phone number is in E.164 format
            if not to_phone.startswith('+'):
                to_phone = f"+91{to_phone}"  # Assuming Indian numbers, adjust as needed
            
            message = self.client.messages.create(
                body=f"Your verification code is: {otp}. This code will expire in 5 minutes.",
                from_=self.from_phone,
                to=to_phone
            )
            
            print(f"SMS sent successfully. SID: {message.sid}")
            return True
            
        except Exception as e:
            print(f"Error sending SMS: {e}")
            return False
    
    def send_welcome_sms(self, to_phone: str) -> bool:
        """Send welcome message after successful verification"""
        if not self.client:
            print(f"Twilio not configured. Welcome message for {to_phone}")
            return False
        
        try:
            if not to_phone.startswith('+'):
                to_phone = f"+91{to_phone}"
            
            message = self.client.messages.create(
                body="Welcome! Your phone number has been successfully verified.",
                from_=self.from_phone,
                to=to_phone
            )
            
            print(f"Welcome SMS sent successfully. SID: {message.sid}")
            return True
            
        except Exception as e:
            print(f"Error sending welcome SMS: {e}")
            return False

# Global Twilio service instance
twilio_service = TwilioService()
