from pydantic import BaseModel, Field

class OTPRequest(BaseModel):
    phone: str = Field(..., example="+91551234567")

class OTPVerifyRequest(BaseModel):
    phone: str = Field(..., example="+91551234567")
    code: str = Field(..., example="123456")
