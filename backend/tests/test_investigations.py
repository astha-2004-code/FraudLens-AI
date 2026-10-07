from fastapi.testclient import TestClient
from app.main import app
from app.database import get_db, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app import models, auth
import pytest

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_investigations.db"
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
    
    user = models.User(email="inv@test.com", hashed_password="hashed", role=models.RoleEnum.INVESTIGATOR)
    db.add(user)
    
    tx = models.Transaction(customer_id=1, amount=100.0, location_country="US")
    db.add(tx)
    db.commit()
    
    inv = models.Investigation(transaction_id=tx.id, investigator_id=user.id)
    db.add(inv)
    
    fc = models.FraudCase(fraud_type="ACCOUNT_TAKEOVER", description="Test", patterns={})
    db.add(fc)
    db.commit()
    
    token = auth.create_access_token({"sub": "inv@test.com"})
    
    with TestClient(app) as c:
        c.headers.update({"Authorization": f"Bearer {token}"})
        yield c
        
    Base.metadata.drop_all(bind=engine)

def test_get_similar_cases(client):
    response = client.get("/api/investigations/1/similar-cases")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert "case_id" in data[0]
    assert "similarity" in data[0]
