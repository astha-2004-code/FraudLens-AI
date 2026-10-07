from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime, JSON, Text, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from .database import Base

class RoleEnum(str, enum.Enum):
    ADMIN = "ADMIN"
    INVESTIGATOR = "INVESTIGATOR"
    VIEWER = "VIEWER"

class RiskLevelEnum(str, enum.Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(Enum(RoleEnum), default=RoleEnum.VIEWER)
    created_at = Column(DateTime, default=datetime.utcnow)

class Customer(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    phone = Column(String, index=True)
    country = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    transactions = relationship("Transaction", back_populates="customer")

class Device(Base):
    __tablename__ = "devices"
    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String, unique=True, index=True)
    device_type = Column(String)
    os_version = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

class Merchant(Base):
    __tablename__ = "merchants"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    category = Column(String)
    country = Column(String)

class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), index=True)
    device_id = Column(Integer, ForeignKey("devices.id"))
    merchant_id = Column(Integer, ForeignKey("merchants.id"))
    amount = Column(Float)
    currency = Column(String, default="INR")
    status = Column(String, default="PENDING")
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    ip_address = Column(String)
    location_city = Column(String)
    location_country = Column(String)
    customer = relationship("Customer", back_populates="transactions")
    investigations = relationship("Investigation", back_populates="transaction")

class Investigation(Base):
    __tablename__ = "investigations"
    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(Integer, ForeignKey("transactions.id"), unique=True)
    investigator_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    status = Column(String, default="OPEN") # OPEN, CLOSED, ESCALATED
    risk_score = Column(Integer, nullable=True)
    risk_level = Column(Enum(RiskLevelEnum), nullable=True)
    hypothesis = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    transaction = relationship("Transaction", back_populates="investigations")
    signals = relationship("RiskSignal", back_populates="investigation")
    evidence = relationship("Evidence", back_populates="investigation")

class RiskSignal(Base):
    __tablename__ = "risk_signals"
    id = Column(Integer, primary_key=True, index=True)
    investigation_id = Column(Integer, ForeignKey("investigations.id"))
    signal_type = Column(String)
    description = Column(String)
    score_impact = Column(Integer)
    investigation = relationship("Investigation", back_populates="signals")

class FraudCase(Base):
    __tablename__ = "fraud_cases"
    id = Column(Integer, primary_key=True, index=True)
    fraud_type = Column(String)
    description = Column(Text)
    patterns = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)

class Evidence(Base):
    __tablename__ = "evidence"
    id = Column(Integer, primary_key=True, index=True)
    investigation_id = Column(Integer, ForeignKey("investigations.id"))
    claim = Column(String)
    evidence_text = Column(Text)
    source = Column(String)
    confidence = Column(Float)
    is_contradictory = Column(Boolean, default=False)
    investigation = relationship("Investigation", back_populates="evidence")

class Policy(Base):
    __tablename__ = "policies"
    id = Column(Integer, primary_key=True, index=True)
    category = Column(String)
    content = Column(Text)
    effective_date = Column(DateTime)
    expiry_date = Column(DateTime, nullable=True)
    version = Column(String)

class InvestigationMessage(Base):
    __tablename__ = "investigation_messages"
    id = Column(Integer, primary_key=True, index=True)
    investigation_id = Column(Integer, ForeignKey("investigations.id"))
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=True) # None for AI
    message = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)
    sources = Column(JSON, nullable=True)

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    action = Column(String)
    details = Column(JSON)
    timestamp = Column(DateTime, default=datetime.utcnow)
