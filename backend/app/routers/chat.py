from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, auth, database
from pydantic import BaseModel
from typing import List

router = APIRouter(
    prefix="/api/investigations",
    tags=["Chat"]
)

class ChatMessage(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str
    sources: List[str]

@router.post("/{id}/chat", response_model=ChatResponse)
def investigator_chat(id: int, chat_message: ChatMessage, db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    investigation = db.query(models.Investigation).filter(models.Investigation.id == id).first()
    if not investigation:
        raise HTTPException(status_code=404, detail="Investigation not found")
        
    # Mocking the AI response with RAG context
    reply = ""
    sources = []
    msg_lower = chat_message.message.lower()
    
    if "why" in msg_lower or "flagged" in msg_lower:
        reply = "The transaction was flagged primarily due to an unusual amount and a new device in a high-risk location."
        sources = ["Transaction Analytics Service", "Amount Anomaly Module"]
    elif "similar" in msg_lower:
        reply = "I found 3 similar cases from the past month involving new devices and rapid succession of transactions."
        sources = ["Historical Fraud Database (Cases #182, #184)"]
    elif "contradict" in msg_lower:
        reply = "The main contradictory evidence is that the customer has used this merchant previously and has a history of travel to this country."
        sources = ["Customer History Database", "Merchant Analytics"]
    else:
        reply = "Based on the evidence, manual investigation is recommended before blocking the account."
        sources = ["Investigation Context", "Risk Scorer"]
        
    # Save the chat message to DB (Optional based on models, we have investigation_messages)
    db_msg_user = models.InvestigationMessage(investigation_id=id, sender_id=current_user.id, message=chat_message.message)
    db.add(db_msg_user)
    db_msg_ai = models.InvestigationMessage(investigation_id=id, sender_id=None, message=reply, sources=sources)
    db.add(db_msg_ai)
    db.commit()

    return ChatResponse(reply=reply, sources=sources)
