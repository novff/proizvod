from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.entities import ServiceTicket, SoftwareComponent, AuditLog, User
from app.schemas.ticket import TicketIn, TicketOut, TicketStatusIn
from app.api.deps import get_current_user, require_admin
router=APIRouter(prefix="/api/tickets", tags=["Заявки на обслуживание"])
@router.get("", response_model=list[TicketOut])
def list_tickets(status: str | None=None, limit: int=Query(100,ge=1,le=200), db: Session=Depends(get_db), user: User=Depends(get_current_user)):
    q=db.query(ServiceTicket)
    if user.role != "admin": q=q.filter(ServiceTicket.creator_id==user.id)
    if status: q=q.filter(ServiceTicket.status==status)
    return q.order_by(ServiceTicket.created_at.desc()).limit(limit).all()
@router.post("", response_model=TicketOut, status_code=201)
def create_ticket(data: TicketIn, db: Session=Depends(get_db), user: User=Depends(get_current_user)):
    if data.component_id and not db.get(SoftwareComponent,data.component_id): raise HTTPException(404,"Компонент не найден")
    if data.priority not in {"low","normal","high","critical"}: raise HTTPException(422,"Недопустимый приоритет")
    item=ServiceTicket(**data.model_dump(),creator_id=user.id); db.add(item); db.commit(); db.refresh(item)
    db.add(AuditLog(user_id=user.id,action="create",entity="ticket",entity_id=item.id)); db.commit(); return item
@router.patch("/{ticket_id}/status", response_model=TicketOut)
def update_status(ticket_id: int, data: TicketStatusIn, db: Session=Depends(get_db), user: User=Depends(require_admin)):
    if data.status not in {"new","in_progress","resolved","closed"}: raise HTTPException(422,"Недопустимый статус")
    item=db.get(ServiceTicket,ticket_id)
    if not item: raise HTTPException(404,"Заявка не найдена")
    item.status=data.status; db.add(AuditLog(user_id=user.id,action="change_status",entity="ticket",entity_id=item.id,details=data.status)); db.commit(); db.refresh(item); return item
