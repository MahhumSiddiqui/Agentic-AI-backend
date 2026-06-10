from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime

class TransactionIngest(BaseModel):
    tx_id: str
    tx_type: str = Field(..., description="Card, ACH, Wire, Wallet, Merchant")
    amount: float
    currency: str
    timestamp: datetime
    customer_id: str
    merchant_id: Optional[str] = None
    device_id: Optional[str] = None
    location: Optional[str] = None
    ip_address: Optional[str] = None
    metadata_fields: Optional[Dict[str, Any]] = None

class IngestResponse(BaseModel):
    status: str
    tx_id: str
    message: str
