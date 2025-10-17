from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# ---------- CREATE ----------
class UserCreate(BaseModel):
    username: str
    email: str
    role: str
    password: str
    profile_picture: Optional[str] = None


# ---------- LOGIN ----------
class UserLogin(BaseModel):
    username: str
    password: str


# ---------- TOKEN ----------
class Token(BaseModel):
    access_token: str
    token_type: str


# ---------- PUBLIC USER ----------
class UserPublic(BaseModel):
    id: int
    username: str
    email: str
    role: str
    profile_picture: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None  # ✅ FIXED




# ---------- UPDATE ----------
class UserUpdate(BaseModel):
    email: Optional[str] = None
    password: Optional[str] = None
    role: Optional[str] = None
