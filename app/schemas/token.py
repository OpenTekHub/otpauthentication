from pydantic import BaseModel, Field

class Token(BaseModel):
    status: str = Field(..., example="approved")
    access_token: str = Field(..., example="eyJhbGciOiJI...")
    token_type: str = Field("bearer", example="bearer")
