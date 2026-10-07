from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, List, Dict, Any
from enum import Enum

class RoleEnum(str, Enum):
    ADMIN = "ADMIN"
    INVESTIGATOR = "INVESTIGATOR"
    VIEWER = "VIEWER"

class RiskLevelEnum(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class UserBase(BaseModel):
    email: str
    role: RoleEnum

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class CustomerBase(BaseModel):
    name: str
    email: str
    phone: str
    country: str

class Customer(CustomerBase):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class TransactionBase(BaseModel):
    customer_id: int
    device_id: int
    merchant_id: int
    amount: float
    currency: str
    status: str
    ip_address: str
    location_city: str
    location_country: str

class Transaction(TransactionBase):
    id: int
    timestamp: datetime
    model_config = ConfigDict(from_attributes=True)
