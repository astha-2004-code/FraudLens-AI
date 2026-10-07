import os
import sys
import random
from datetime import datetime, timedelta
from faker import Faker

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))

from app.database import SessionLocal, engine
from app import models

fake = Faker()

def generate_data():
    db = SessionLocal()
    
    # 1. Generate Customers
    customers = []
    print("Generating 5000 customers...")
    for _ in range(5000):
        c = models.Customer(
            name=fake.name(),
            email=fake.email(),
            phone=fake.phone_number(),
            country=fake.country()
        )
        customers.append(c)
    db.bulk_save_objects(customers)
    db.commit()
    
    # Reload to get IDs
    customers = db.query(models.Customer).all()
    customer_ids = [c.id for c in customers]
    customer_countries = {c.id: c.country for c in customers}

    # 2. Generate Devices
    devices = []
    print("Generating 10000 devices...")
    for _ in range(10000):
        d = models.Device(
            device_id=fake.uuid4(),
            device_type=random.choice(["MOBILE", "DESKTOP", "TABLET"]),
            os_version=random.choice(["Android 12", "iOS 16", "Windows 11", "macOS 13"])
        )
        devices.append(d)
    db.bulk_save_objects(devices)
    db.commit()
    
    devices = db.query(models.Device).all()
    device_ids = [d.id for d in devices]

    # 3. Generate Merchants
    merchants = []
    print("Generating Merchants...")
    for _ in range(500):
        m = models.Merchant(
            name=fake.company(),
            category=random.choice(["RETAIL", "TRAVEL", "ELECTRONICS", "GROCERY", "GAMING"]),
            country=fake.country()
        )
        merchants.append(m)
    db.bulk_save_objects(merchants)
    db.commit()

    merchants = db.query(models.Merchant).all()
    merchant_ids = [m.id for m in merchants]

    # 4. Generate Transactions (Normal and Suspicious)
    transactions = []
    print("Generating 50000 transactions...")
    for i in range(50000):
        cid = random.choice(customer_ids)
        is_suspicious = random.random() < 0.05 # 5% suspicious
        
        # Base transaction
        t = models.Transaction(
            customer_id=cid,
            device_id=random.choice(device_ids),
            merchant_id=random.choice(merchant_ids),
            amount=round(random.uniform(10, 5000), 2),
            currency="INR",
            status="COMPLETED",
            timestamp=datetime.utcnow() - timedelta(days=random.randint(0, 365), hours=random.randint(0, 23)),
            ip_address=fake.ipv4(),
            location_city=fake.city(),
            location_country=customer_countries[cid]
        )
        
        if is_suspicious:
            # Modify to be suspicious
            t.amount = round(random.uniform(20000, 100000), 2)
            t.location_country = fake.country() if random.random() < 0.5 else t.location_country
            t.device_id = random.choice(device_ids) # new device
            
        transactions.append(t)
        
        if len(transactions) >= 5000:
            db.bulk_save_objects(transactions)
            db.commit()
            transactions = []
            
    if transactions:
        db.bulk_save_objects(transactions)
        db.commit()

    # 5. Generate Fraud Cases
    fraud_cases = []
    print("Generating 500 Fraud Cases...")
    for _ in range(500):
        fc = models.FraudCase(
            fraud_type=random.choice(["ACCOUNT_TAKEOVER", "CARD_NOT_PRESENT", "FRIENDLY_FRAUD", "SYNTHETIC_IDENTITY"]),
            description=fake.text(),
            patterns={"velocity_anomaly": random.choice([True, False]), "new_device": True}
        )
        fraud_cases.append(fc)
    db.bulk_save_objects(fraud_cases)
    db.commit()

    print("Data generation complete.")

if __name__ == "__main__":
    generate_data()
