import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from app.database import engine, Base
from app.routes import router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Secure AI-Powered Automated Visual Inspection System",
    description="Enterprise API with Deep Learning, NLP Auditing, and Security Hardening",
    version="1.0.0"
)

@app.get("/", response_class=HTMLResponse, tags=["Dashboard"])
def serve_dashboard():
    template_path = os.path.join("app", "templates", "index.html")
    with open(template_path, "r", encoding="utf-8") as f:
        return f.read()

app.include_router(router)
