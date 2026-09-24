from sqlalchemy import Column, Integer, String, DateTime, Text, Float
from datetime import datetime
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(20), default="operator")
    created_at = Column(DateTime, default=datetime.utcnow)

class InspectionRecord(Base):
    __tablename__ = "inspection_records"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    notes = Column(Text, nullable=True)               # ملاحظات المفتش
    image_path = Column(String(255), nullable=False)
    status = Column(String(30), default="Pending")
    severity = Column(String(20), default="NORMAL")   # مستوى الخطورة من NLP
    ai_summary = Column(Text, nullable=True)
    detailed_report = Column(Text, nullable=True)     # التقرير الفني المولد
    confidence_score = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)