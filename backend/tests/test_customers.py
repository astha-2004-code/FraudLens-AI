from fastapi.testclient import TestClient
from app.main import app
from app.database import get_db, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app import models, auth
import pytest

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_customers.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="module")
def client():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    
    user = models.User(email="test@test.com", hashed_password="hashed", role=models.RoleEnum.INVESTIGATOR)
    db.add(user)
    
    customer = models.Customer(name="John", email="john@test.com", phone="123", country="US")
    db.add(customer)
    db.commit()
    
    tx1 = models.Transaction(customer_id=1, amount=100.0, location_country="US")
    tx2 = models.Transaction(customer_id=1, amount=150.0, location_country="US")
    tx_current = models.Transaction(customer_id=1, amount=1000.0, location_country="UK")
    db.add_all([tx1, tx2, tx_current])
    db.commit()
    
    token = auth.create_access_token({"sub": "test@test.com"})
    
    with TestClient(app) as c:
        c.headers.update({"Authorization": f"Bearer {token}"})
        yield c
        
    Base.metadata.drop_all(bind=engine)

def test_get_customer_behavior(client):
    response = client.get("/api/customers/1/behavior?current_tx_id=3")
    assert response.status_code == 200
    data = response.json()
    assert "average_transaction" in data
    assert "comparison" in data
    assert data["comparison"]["current_amount"] == 1000.0
