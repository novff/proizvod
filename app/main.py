from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from sqlalchemy import text
from app.core.config import settings
from app.db.session import Base, engine, SessionLocal
from app.models.entities import User, SoftwareComponent
from app.core.security import hash_password
from app.api import auth, components, tickets, metrics

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    db=SessionLocal()
    try:
        if not db.query(User).filter_by(email=settings.admin_email.lower()).first():
            db.add(User(email=settings.admin_email.lower(), full_name="Администратор системы", password_hash=hash_password(settings.admin_password), role="admin"))
            db.commit()
        if db.query(SoftwareComponent).count()==0:
            db.add_all([SoftwareComponent(name="FastAPI",version="0.115",vendor="FastAPI",description="Серверный веб-фреймворк"), SoftwareComponent(name="PostgreSQL",version="16",vendor="PostgreSQL Global Development Group",description="Реляционная СУБД"), SoftwareComponent(name="Docker Engine",version="27",vendor="Docker",description="Среда контейнеризации")]); db.commit()
    finally: db.close()
    yield

app=FastAPI(title=settings.app_name,version="1.0.0",description="Учебная система сопровождения программных компонентов и заявок",lifespan=lifespan)
app.include_router(auth.router); app.include_router(components.router); app.include_router(tickets.router); app.include_router(metrics.router)
@app.get("/",tags=["Система"])
def root(): return {"name":settings.app_name,"docs":"/docs","health":"/health"}
@app.get("/health",tags=["Система"])
def health():
    try:
        with engine.connect() as conn: conn.execute(text("SELECT 1"))
        return {"status":"ok","database":"ok"}
    except Exception:
        return JSONResponse(status_code=503,content={"status":"degraded","database":"unavailable"})
