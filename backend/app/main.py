from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="FraudLens AI",
    description="Evidence-Driven Fraud Investigation Copilot",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from app.routers import auth, customers, investigations

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "FraudLens AI Backend"}

app.include_router(auth.router)
app.include_router(customers.router)
app.include_router(investigations.router)
