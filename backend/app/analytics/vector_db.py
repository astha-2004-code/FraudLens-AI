from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from sqlalchemy.orm import Session
from .. import models
import json
import random
from datetime import datetime

class MockEmbedder:
    def encode(self, texts):
        if isinstance(texts, str):
            return [random.random() for _ in range(384)]
        return [[random.random() for _ in range(384)] for _ in texts]

class VectorSearchService:
    def __init__(self):
        self.client = QdrantClient(":memory:")
        self.model = MockEmbedder()
        
        self.client.recreate_collection(
            collection_name="fraud_cases",
            vectors_config=VectorParams(size=384, distance=Distance.COSINE),
        )
        self.client.recreate_collection(
            collection_name="policies",
            vectors_config=VectorParams(size=384, distance=Distance.COSINE),
        )

    def load_cases(self, db: Session):
        cases = db.query(models.FraudCase).all()
        if not cases:
            return
        texts = [f"Type: {c.fraud_type}. Description: {c.description}. Patterns: {json.dumps(c.patterns)}" for c in cases]
        vectors = self.model.encode(texts)
        points = [
            PointStruct(id=c.id, vector=vectors[i], payload={"id": c.id, "type": c.fraud_type, "patterns": c.patterns})
            for i, c in enumerate(cases)
        ]
        self.client.upsert(collection_name="fraud_cases", points=points)
        
    def load_policies(self, db: Session):
        policies = db.query(models.Policy).all()
        if not policies:
            return
        texts = [f"Category: {p.category}. Content: {p.content}" for p in policies]
        vectors = self.model.encode(texts)
        points = [
            PointStruct(id=p.id, vector=vectors[i], payload={"id": p.id, "category": p.category})
            for i, p in enumerate(policies)
        ]
        self.client.upsert(collection_name="policies", points=points)

    def search_similar_cases(self, transaction: models.Transaction, db: Session, limit: int = 3):
        query_text = f"Transaction amount: {transaction.amount}, Location: {transaction.location_country}. Device: {transaction.device_id}"
        query_vector = self.model.encode(query_text)
        search_result = self.client.search(collection_name="fraud_cases", query_vector=query_vector, limit=limit)
        results = []
        for hit in search_result:
            case = db.query(models.FraudCase).filter(models.FraudCase.id == hit.payload["id"]).first()
            if case:
                results.append({
                    "case_id": case.id,
                    "similarity": round(hit.score * 100, 2),
                    "fraud_type": case.fraud_type,
                    "similar_patterns": "Shared patterns like velocity anomaly and new device." if hit.score > 0.5 else "Some general similarity.",
                    "differences": "Different location and merchant." if hit.score <= 0.8 else "Minor differences."
                })
        return results
        
    def search_policies(self, query: str, db: Session, limit: int = 2):
        query_vector = self.model.encode(query)
        search_result = self.client.search(collection_name="policies", query_vector=query_vector, limit=limit)
        results = []
        now = datetime.utcnow()
        for hit in search_result:
            policy = db.query(models.Policy).filter(models.Policy.id == hit.payload["id"]).first()
            # Temporal check
            if policy and policy.effective_date <= now and (not policy.expiry_date or policy.expiry_date >= now):
                results.append({
                    "policy_id": policy.id,
                    "category": policy.category,
                    "content": policy.content,
                    "version": policy.version
                })
        return results

vector_db_service = VectorSearchService()
