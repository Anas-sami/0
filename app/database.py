from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# مسار قاعدة البيانات المحلية (SQLite)
SQLALCHEMY_DATABASE_URL = "sqlite:///./inspection_data.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# دالة فتح وإغلاق جلسة قاعدة البيانات تلقائياً
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()