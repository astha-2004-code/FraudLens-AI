from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from sqlalchemy.orm import Session
from .. import models
import json
import random

class MockEmbedder:
    def encode(self, texts):
        if isinstance(texts, str):
            return [random.random() for _ in range(384)]
        return [[random.random() for _ in range(384)] for _ in texts]

class VectorSearchService:
    def __init__(self):
        self.client = QdrantClient(":memory:")
        self.model = MockEmbedder()
        self.collection_name = "fraud_cases"
        
        self.client.recreate_collection(
            collection_name=self.collection_name,
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
        
        self.client.upsert(
            collection_name=self.collection_name,
            points=points
        )

    def search_similar_cases(self, transaction: models.Transaction, db: Session, limit: int = 3):
        query_text = f"Transaction amount: {transaction.amount}, Location: {transaction.location_country}. Device: {transaction.device_id}"
        query_vector = self.model.encode(query_text)
        
        search_result = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            limit=limit
        )
        
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

vector_db_service = VectorSearchService()
