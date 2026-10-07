from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import numpy as np
from .. import models

class TransactionAnalyzer:
    def __init__(self, db: Session, transaction: models.Transaction):
        self.db = db
        self.transaction = transaction
        self.customer_history = self.db.query(models.Transaction).filter(
            models.Transaction.customer_id == transaction.customer_id,
            models.Transaction.id != transaction.id
        ).all()

    def analyze_amount(self):
        if not self.customer_history:
            return {"status": "INSUFFICIENT_DATA"}
            
        amounts = [t.amount for t in self.customer_history]
        avg = np.mean(amounts)
        median = np.median(amounts)
        std_dev = np.std(amounts) if len(amounts) > 1 else 0
        percentile = sum(a < self.transaction.amount for a in amounts) / len(amounts) * 100
        
        deviation = (self.transaction.amount - avg) / avg * 100 if avg > 0 else 0
        
        return {
            "average": avg,
            "median": median,
            "std_dev": std_dev,
            "percentile": percentile,
            "deviation_pct": deviation,
            "is_anomalous": deviation > 200 or percentile > 95
        }

    def analyze_velocity(self):
        one_hour_ago = self.transaction.timestamp - timedelta(hours=1)
        one_minute_ago = self.transaction.timestamp - timedelta(minutes=1)
        
        tx_last_hour = [t for t in self.customer_history if t.timestamp >= one_hour_ago]
        tx_last_minute = [t for t in tx_last_hour if t.timestamp >= one_minute_ago]
        
        amount_last_hour = sum(t.amount for t in tx_last_hour)
        
        return {
            "tx_per_hour": len(tx_last_hour),
            "tx_per_minute": len(tx_last_minute),
            "amount_per_hour": amount_last_hour,
            "is_anomalous": len(tx_last_minute) > 3 or len(tx_last_hour) > 10
        }

    def analyze_device(self):
        known_devices = set(t.device_id for t in self.customer_history)
        is_new_device = self.transaction.device_id not in known_devices
        
        # Check if device is shared by other customers
        shared_users_count = self.db.query(models.Transaction.customer_id).filter(
            models.Transaction.device_id == self.transaction.device_id
        ).distinct().count()
        
        return {
            "is_new_device": is_new_device,
            "shared_by_others": shared_users_count > 1,
            "is_anomalous": is_new_device or shared_users_count > 2
        }

    def analyze_location(self):
        known_countries = set(t.location_country for t in self.customer_history)
        known_cities = set(t.location_city for t in self.customer_history)
        
        is_new_country = self.transaction.location_country not in known_countries
        is_new_city = self.transaction.location_city not in known_cities
        
        # Impossible travel - just a simple heuristic for now
        last_tx = max(self.customer_history, key=lambda t: t.timestamp) if self.customer_history else None
        impossible_travel = False
        if last_tx and last_tx.location_country != self.transaction.location_country:
            time_diff = (self.transaction.timestamp - last_tx.timestamp).total_seconds() / 3600
            if time_diff < 4:  # Assuming changing countries within 4 hours is highly suspicious
                impossible_travel = True

        return {
            "is_new_country": is_new_country,
            "is_new_city": is_new_city,
            "impossible_travel": impossible_travel,
            "is_anomalous": is_new_country or impossible_travel
        }

    def analyze_merchant(self):
        known_merchants = set(t.merchant_id for t in self.customer_history)
        return {
            "is_new_merchant": self.transaction.merchant_id not in known_merchants,
            "is_anomalous": self.transaction.merchant_id not in known_merchants
        }

    def analyze_time(self):
        tx_hour = self.transaction.timestamp.hour
        # Assuming typical transaction hours are between 6 AM and 11 PM
        is_unusual_hour = not (6 <= tx_hour <= 23)
        return {
            "transaction_hour": tx_hour,
            "is_unusual_hour": is_unusual_hour,
            "is_anomalous": is_unusual_hour
        }

    def run_all(self):
        return {
            "amount": self.analyze_amount(),
            "velocity": self.analyze_velocity(),
            "device": self.analyze_device(),
            "location": self.analyze_location(),
            "merchant": self.analyze_merchant(),
            "time": self.analyze_time()
        }
