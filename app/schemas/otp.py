from pydantic import BaseModel, Field

class OTPRequest(BaseModel):
    phone: str = Field(..., example="+91551234567")

class OTPResponse(BaseModel):
    status: str = Field(..., example="pending")
