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
    vector_db_service.load_cases(db)
    similar_cases = vector_db_service.search_similar_cases(transaction, db)
    return similar_cases

@router.get("/{id}/evidence")
def get_evidence(id: int, db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    investigation = db.query(models.Investigation).filter(models.Investigation.id == id).first()
    if not investigation:
        raise HTTPException(status_code=404, detail="Investigation not found")
        
    evidence_list = db.query(models.Evidence).filter(models.Evidence.investigation_id == id).all()
    if not evidence_list:
        return {"message": "Insufficient evidence."}
        
    return evidence_list

from pydantic import BaseModel

class ChallengeResponse(BaseModel):
    original_confidence: float
    supporting_evidence: list[str]
    contradicting_evidence: list[str]
    alternative_explanations: list[str]
    updated_confidence: float
    recommendation: str

@router.post("/{id}/challenge", response_model=ChallengeResponse)
def challenge_assessment(id: int, db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.role_required([models.RoleEnum.INVESTIGATOR, models.RoleEnum.ADMIN]))):
    investigation = db.query(models.Investigation).filter(models.Investigation.id == id).first()
    if not investigation:
        raise HTTPException(status_code=404, detail="Investigation not found")
        
    # Mock Challenge agent execution
    response = ChallengeResponse(
        original_confidence=91.0,
        supporting_evidence=["Unusually large transaction amount", "New device detected"],
        contradicting_evidence=["Customer has previously used this merchant", "Customer has traveled to this country before"],
        alternative_explanations=["Customer is on vacation and making a large purchase from a known merchant using a new phone."],
        updated_confidence=74.0,
        recommendation="Manual investigation"
    )
    
from .analytics.graph import build_transaction_graph

@router.get("/{id}/graph")
def get_investigation_graph(id: int, db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    investigation = db.query(models.Investigation).filter(models.Investigation.id == id).first()
    if not investigation:
        raise HTTPException(status_code=404, detail="Investigation not found")
        
    transaction = investigation.transaction
    graph_data = build_transaction_graph(transaction, db)
    
    return graph_data
