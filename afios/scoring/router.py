from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict, Any
from afios.scoring.engine import FraudScoringEngine

router = APIRouter()
engine = FraudScoringEngine()

class ScoringRequest(BaseModel):
    transaction: Dict[str, Any]
    features: Dict[str, Any]

class ScoringResponse(BaseModel):
    fraud_score: float
    model_version: str
    input_transaction: Dict[str, Any]

@router.post("/predict", response_model=ScoringResponse)
async def predict_fraud(request: ScoringRequest):
    score = engine.predict(request.transaction, request.features)
    return ScoringResponse(
        fraud_score=score,
        model_version=engine.model_version,
        input_transaction=request.transaction
    )
