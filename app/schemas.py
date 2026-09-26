from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    role: str
    created_at: datetime

    class Config:
        from_attributes = True

class InspectionResponse(BaseModel):
    id: int
    title: str
    notes: Optional[str] = None
    image_path: str
    status: str
    severity: Optional[str] = "NORMAL"
    ai_summary: Optional[str] = None
    detailed_report: Optional[str] = None
    confidence_score: Optional[float] = None
    created_at: datetime

    class Config:
        from_attributes = True
