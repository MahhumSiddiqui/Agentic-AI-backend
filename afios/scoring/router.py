from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer
from pydantic import BaseModel
from typing import Dict, Any
from afios.scoring.engine import FraudScoringEngine
from afios.gateway.auth import SECRET_KEY, ALGORITHM
from jose import jwt, JWTError
import random

router = APIRouter()
engine = FraudScoringEngine()

# -----------------------
# SECURITY
# -----------------------
security = HTTPBearer()

def get_current_user(token: str = Depends(security)):
    try:
        payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")


# -----------------------
# MODELS
# -----------------------
class ScoringRequest(BaseModel):
    transaction: Dict[str, Any]
    features: Dict[str, Any] = {}


class ScoringResponse(BaseModel):
    fraud_score: float
    model_version: str
    input_transaction: Dict[str, Any]


# -----------------------
# FEATURE FALLBACK
# -----------------------
def generate_pseudo_features(transaction: Dict[str, Any]) -> Dict[str, float]:
    amount = float(transaction.get("amount", 0))

    return {
        "transaction_velocity_24h": random.uniform(0, 1),
        "distance_from_home": random.uniform(0, 1),
        "merchant_risk_score": random.uniform(0, 1),
        "amount_normalized": min(amount / 10000, 1),
        "device_risk": random.uniform(0, 1),
        "ip_risk": random.uniform(0, 1),
    }


# -----------------------
# PROTECTED ENDPOINT
# -----------------------
@router.post("/predict", response_model=ScoringResponse)
async def predict_fraud(
    request: ScoringRequest,
    user: str = Depends(get_current_user)
):
    features = request.features

    if not features:
        features = generate_pseudo_features(request.transaction)

    score = engine.predict(request.transaction, features)

    return ScoringResponse(
        fraud_score=score,
        model_version=engine.model_version,
        input_transaction=request.transaction
    )