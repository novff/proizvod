from pydantic import BaseModel, EmailStr, Field
class RegisterIn(BaseModel):
    email: EmailStr
    full_name: str = Field(min_length=2, max_length=160)
    password: str = Field(min_length=10, max_length=128)
class LoginIn(BaseModel):
    email: EmailStr
    password: str
class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
class UserOut(BaseModel):
    id: int; email: EmailStr; full_name: str; role: str; is_active: bool
    model_config = {"from_attributes": True}
