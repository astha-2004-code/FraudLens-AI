from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from .. import models, auth, database
from .analytics.vector_db import vector_db_service
from datetime import datetime
from pydantic import BaseModel
from typing import Optional

router = APIRouter(
    prefix="/api",
    tags=["Policies"]
)

class PolicyCreate(BaseModel):
    category: str
    content: str
    effective_date: datetime
    expiry_date: Optional[datetime] = None
    version: str

@router.post("/documents/upload")
def upload_policy(policy: PolicyCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.role_required([models.RoleEnum.ADMIN]))):
    new_policy = models.Policy(**policy.model_dump())
    db.add(new_policy)
    db.commit()
    db.refresh(new_policy)
    vector_db_service.load_policies(db)
    return new_policy

@router.get("/policies")
def get_policies(query: str = "", db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    vector_db_service.load_policies(db)
    if query:
        return vector_db_service.search_policies(query, db)
    now = datetime.utcnow()
    policies = db.query(models.Policy).filter(
        models.Policy.effective_date <= now,
        (models.Policy.expiry_date == None) | (models.Policy.expiry_date >= now)
    ).all()
    return policies
