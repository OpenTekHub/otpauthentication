from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from database import execute_query
from twilio_service import twilio_service
from typing import List, Optional
import random
import os
from datetime import datetime, timedelta

router = APIRouter()

# Pydantic models for OTP authentication
class PhoneNumberRequest(BaseModel):
    phone_number: str

class OTPVerificationRequest(BaseModel):
    phone_number: str
    otp: str

class UserResponse(BaseModel):
    id: int
    phone_number: str
    is_verified: bool
    created_at: str

class OTPResponse(BaseModel):
    message: str
    expires_in_minutes: int

# OTP Authentication Routes

@router.post("/send-otp", response_model=OTPResponse)
async def send_otp(request: PhoneNumberRequest):
    """Send OTP to phone number"""
    phone_number = request.phone_number.strip()
    
    # Validate phone number (basic validation)
    if len(phone_number) < 10:
        raise HTTPException(status_code=400, detail="Invalid phone number")
    
    # Generate 6-digit OTP
    otp = str(random.randint(100000, 999999))
    
    # Set OTP expiration (5 minutes from now)
    expires_at = datetime.now() + timedelta(minutes=5)
    
    try:
        # Check if user already exists
        check_user_query = "SELECT id FROM users WHERE phone_number = %s"
        existing_user = execute_query(check_user_query, (phone_number,))
        
        if existing_user:
            # Update existing user's OTP
            update_otp_query = """
                UPDATE users 
                SET otp = %s, otp_expires_at = %s, otp_verified = FALSE 
                WHERE phone_number = %s
            """
            execute_query(update_otp_query, (otp, expires_at, phone_number))
        else:
            # Create new user with OTP
            insert_user_query = """
                INSERT INTO users (phone_number, otp, otp_expires_at, otp_verified) 
                VALUES (%s, %s, %s, %s)
            """
            execute_query(insert_user_query, (phone_number, otp, expires_at, False))
        
        # Send SMS via Twilio
        sms_sent = twilio_service.send_otp_sms(phone_number, otp)
        
        if not sms_sent:
            # For development - log OTP to console
            print(f"SMS failed - OTP for {phone_number}: {otp}")
            return OTPResponse(
                message="OTP sent successfully (development mode)",
                expires_in_minutes=5
            )
        
        return OTPResponse(
            message="OTP sent successfully",
            expires_in_minutes=5
        )
        
    except Exception as e:
        print(f"Error sending OTP: {e}")
        raise HTTPException(status_code=500, detail="Failed to send OTP")

@router.post("/verify-otp")
async def verify_otp(request: OTPVerificationRequest):
    """Verify OTP and login user"""
    phone_number = request.phone_number.strip()
    otp = request.otp.strip()
    
    if len(otp) < 4:
        raise HTTPException(status_code=400, detail="Invalid OTP")
    
    try:
        # Get user with OTP details
        query = """
            SELECT id, phone_number, otp, otp_expires_at, otp_verified 
            FROM users 
            WHERE phone_number = %s
        """
        user_data = execute_query(query, (phone_number,))
        
        if not user_data:
            raise HTTPException(status_code=404, detail="User not found")
        
        user = user_data[0]
        
        # Check if OTP has expired
        if datetime.now() > user['otp_expires_at']:
            raise HTTPException(status_code=400, detail="OTP has expired")
        
        # Verify OTP
        if user['otp'] != otp:
            raise HTTPException(status_code=400, detail="Invalid OTP")
        
        # Mark OTP as verified
        update_query = """
            UPDATE users 
            SET otp_verified = TRUE, is_verified = TRUE, otp = NULL 
            WHERE phone_number = %s
        """
        execute_query(update_query, (phone_number,))
        
        return {
            "message": "OTP verified successfully",
            "user_id": user['id'],
            "phone_number": phone_number,
            "is_verified": True
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error verifying OTP: {e}")
        raise HTTPException(status_code=500, detail="Failed to verify OTP")

@router.post("/login")
async def login_user(request: PhoneNumberRequest):
    """Login user (after OTP verification)"""
    phone_number = request.phone_number.strip()
    
    try:
        # Check if user exists and is verified
        query = """
            SELECT id, phone_number, is_verified, created_at 
            FROM users 
            WHERE phone_number = %s AND is_verified = TRUE
        """
        user_data = execute_query(query, (phone_number,))
        
        if not user_data:
            raise HTTPException(
                status_code=401, 
                detail="User not found or not verified. Please complete OTP verification first."
            )
        
        user = user_data[0]
        
        return {
            "message": "Login successful",
            "user": {
                "id": user['id'],
                "phone_number": user['phone_number'],
                "is_verified": user['is_verified'],
                "created_at": str(user['created_at'])
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error during login: {e}")
        raise HTTPException(status_code=500, detail="Login failed")

