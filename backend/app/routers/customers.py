from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, auth, database
import numpy as np

router = APIRouter(
    prefix="/api/customers",
    tags=["Customers"]
)

@router.get("/{id}/behavior")
def get_customer_behavior(id: int, current_tx_id: int = None, db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    customer = db.query(models.Customer).filter(models.Customer.id == id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
        
    transactions = db.query(models.Transaction).filter(models.Transaction.customer_id == id).all()
    
    if not transactions:
        return {"status": "INSUFFICIENT_DATA"}
        
    amounts = [t.amount for t in transactions]
    countries = list(set(t.location_country for t in transactions))
    devices = list(set(t.device_id for t in transactions))
    merchants = list(set(t.merchant_id for t in transactions))
    
    avg_tx = np.mean(amounts)
    std_tx = np.std(amounts) if len(amounts) > 1 else 0
    tx_range = f"{max(0, avg_tx - std_tx):.2f} - {avg_tx + std_tx:.2f}"
    
    hours = [t.timestamp.hour for t in transactions]
    freq_hours = f"{min(hours)}:00 - {max(hours)}:00"
    
    profile = {
        "average_transaction": round(avg_tx, 2),
        "typical_transaction_range": tx_range,
        "usual_countries": countries,
        "usual_devices": devices,
        "usual_merchants": merchants,
        "normal_transaction_frequency": f"{len(transactions)} total",
        "normal_transaction_hours": freq_hours
    }
    
    if current_tx_id:
        current_tx = db.query(models.Transaction).filter(models.Transaction.id == current_tx_id).first()
        if current_tx:
            deviation = ((current_tx.amount - avg_tx) / avg_tx) * 100 if avg_tx > 0 else 0
            profile["comparison"] = {
                "normal_amount": round(avg_tx, 2),
                "current_amount": current_tx.amount,
                "deviation": f"{'+' if deviation > 0 else ''}{round(deviation, 2)}%"
            }

    return profile
