import os
import shutil
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User, InspectionRecord
from app.schemas import UserCreate, UserResponse, InspectionResponse
from app.ai_engine import VisionEngine
from app.nlp_engine import NLPEngine
from app.security import hash_password, validate_image_file

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

vision_engine = VisionEngine()
nlp_engine = NLPEngine()

@router.get("/health", tags=["General"])
def health_check():
    return {"status": "online", "message": "Inspection API is functioning normally"}

@router.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED, tags=["Users"])
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username is already registered")
    
    # تأمين كلمة المرور بالتشفير المملح بدلاً من النص الصريح
    secured_hash = hash_password(user.password)
    new_user = User(username=user.username, hashed_password=secured_hash)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/inspections/upload", response_model=InspectionResponse, status_code=status.HTTP_201_CREATED, tags=["Inspections"])
def upload_and_inspect_image(
    title: str = Form(...),
    notes: str = Form(""),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # الحماية: التحقق من الامتداد وحجم الملف قبل الحفظ
    file_bytes = file.file.read()
    validate_image_file(file.filename, len(file_bytes))
    file.file.seek(0)

    # حفظ الملف
    safe_filename = os.path.basename(file.filename)
    file_location = os.path.join(UPLOAD_DIR, safe_filename)
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # التحليل البصري
    try:
        vision_result = vision_engine.analyze_image(file_location)
        current_status = "Processed"
        summary = vision_result["summary"]
        confidence = vision_result["confidence_score"]
    except Exception as e:
        current_status = "Failed"
        summary = f"Vision Error: {str(e)}"
        confidence = 0.0

    # تقرير معالجة اللغة الطبيعية والخطورة
    nlp_result = nlp_engine.generate_audit_report(
        title=title,
        notes=notes,
        detected_objects=summary,
        confidence=confidence
    )

    record = InspectionRecord(
        title=title,
        notes=notes,
        image_path=file_location,
        status=current_status,
        severity=nlp_result["severity"],
        ai_summary=summary,
        detailed_report=nlp_result["detailed_report"],
        confidence_score=confidence
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

@router.get("/inspections", response_model=list[InspectionResponse], tags=["Inspections"])
def get_all_inspections(db: Session = Depends(get_db)):
    return db.query(InspectionRecord).all()
