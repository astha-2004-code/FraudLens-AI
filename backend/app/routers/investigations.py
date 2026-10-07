from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, auth, database
from .analytics.vector_db import vector_db_service

router = APIRouter(
    prefix="/api/investigations",
    tags=["Investigations"]
)

@router.get("/{id}/similar-cases")
def get_similar_cases(id: int, db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    investigation = db.query(models.Investigation).filter(models.Investigation.id == id).first()
    if not investigation:
        raise HTTPException(status_code=404, detail="Investigation not found")
        
    transaction = investigation.transaction
    
    # Load cases into memory index if not already loaded (In production, this would be a persistent Qdrant instance)
    vector_db_service.load_cases(db)
    
    similar_cases = vector_db_service.search_similar_cases(transaction, db)
    
    return similar_cases
