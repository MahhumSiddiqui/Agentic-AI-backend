from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict, Any
from afios.scoring.engine import FraudScoringEngine
import hashlib
import random

router = APIRouter()
engine = FraudScoringEngine()


class ScoringRequest(BaseModel):
    transaction: Dict[str, Any]
    features: Dict[str, Any] = {}


class ScoringResponse(BaseModel):
    fraud_score: float
    model_version: str
    input_transaction: Dict[str, Any]


def generate_pseudo_features(transaction: dict):
    seed_str = f"{transaction.get('transaction_id')}:{transaction.get('amount')}:{transaction.get('customer_id')}"
    seed = int(hashlib.md5(seed_str.encode()).hexdigest(), 16)
    random.seed(seed)

    return {
        "amount_zscore": round(random.uniform(0.2, 3.5), 3),
        "device_unseen": random.choice([0, 1]),
        "merchant_velocity_1h": round(random.uniform(0.1, 5.0), 3),
        "geo_distance_24h": round(random.uniform(0.0, 100.0), 2),
        "mcc_unusual_for_customer": random.choice([0, 1]),
        "ip_asn_risk": round(random.uniform(0.0, 1.0), 3),
        "time_of_day_anomaly": round(random.uniform(-1.0, 1.0), 3),
        "card_age_days": round(random.uniform(10, 2000), 0)
    }


@router.post("/predict", response_model=ScoringResponse)
async def predict_fraud(request: ScoringRequest):

    features = request.features

    # 🔥 FIX: if frontend sends empty features, generate them
    if not features:
        features = generate_pseudo_features(request.transaction)

    score = engine.predict(request.transaction, features)

    return ScoringResponse(
        fraud_score=score,
        model_version=engine.model_version,
        input_transaction=request.transaction
    )