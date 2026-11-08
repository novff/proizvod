from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.entities import SoftwareComponent, AuditLog, User
from app.schemas.component import ComponentIn, ComponentOut
from app.api.deps import get_current_user, require_admin
router=APIRouter(prefix="/api/components", tags=["Программные компоненты"])
@router.get("", response_model=list[ComponentOut])
def list_components(q: str | None = None, limit: int = Query(100, ge=1, le=200), db: Session=Depends(get_db), user: User=Depends(get_current_user)):
    query=db.query(SoftwareComponent)
    if q: query=query.filter(SoftwareComponent.name.ilike(f"%{q}%"))
    return query.order_by(SoftwareComponent.id).limit(limit).all()
@router.post("", response_model=ComponentOut, status_code=201)
def create_component(data: ComponentIn, db: Session=Depends(get_db), user: User=Depends(require_admin)):
    if db.query(SoftwareComponent).filter_by(name=data.name).first(): raise HTTPException(409,"Компонент с таким названием уже существует")
    item=SoftwareComponent(**data.model_dump()); db.add(item); db.commit(); db.refresh(item)
    db.add(AuditLog(user_id=user.id, action="create", entity="component", entity_id=item.id)); db.commit(); return item
@router.get("/{component_id}", response_model=ComponentOut)
def get_component(component_id: int, db: Session=Depends(get_db), user: User=Depends(get_current_user)):
    item=db.get(SoftwareComponent, component_id)
    if not item: raise HTTPException(404,"Компонент не найден")
    return item
@router.put("/{component_id}", response_model=ComponentOut)
def update_component(component_id: int, data: ComponentIn, db: Session=Depends(get_db), user: User=Depends(require_admin)):
    item=db.get(SoftwareComponent, component_id)
    if not item: raise HTTPException(404,"Компонент не найден")
    for key,value in data.model_dump().items(): setattr(item,key,value)
    db.add(AuditLog(user_id=user.id, action="update", entity="component", entity_id=item.id)); db.commit(); db.refresh(item); return item
