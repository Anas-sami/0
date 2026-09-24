import uvicorn
from fastapi import FastAPI
from app.database import engine, Base
from app.routes import router

# إنشاء الجداول في قاعدة البيانات تلقائياً
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Secure AI Inspection Platform",
    description="Backend API foundation for AI processing, security validation, and cloud deployment",
    version="1.0.0"
)

app.include_router(router)

# كود التشغيل المباشر
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)