from time import perf_counter
from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.entities import User
router=APIRouter(prefix="/api/metrics",tags=["Эксплуатационные характеристики"])
@router.get("/database")
def database_metrics(db: Session=Depends(get_db), user: User=Depends(get_current_user)):
    started=perf_counter(); db.execute(text("SELECT 1")); elapsed=(perf_counter()-started)*1000
    return {"database":"available","probe":"SELECT 1","response_time_ms":round(elapsed,3)}
@router.get("/summary")
def summary(db: Session=Depends(get_db), user: User=Depends(get_current_user)):
    started=perf_counter(); users=db.query(User).count(); elapsed=(perf_counter()-started)*1000
    return {"users_count":users,"query_time_ms":round(elapsed,3),"measurement":"single local request; not a load-test result"}
