from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict, Any, List
from afios.explainability.engine import ExplainabilityEngine

router = APIRouter()
engine = ExplainabilityEngine()

class ExplainRequest(BaseModel):
    transaction: Dict[str, Any]
    features: Dict[str, Any]
    model_score: float

class ExplainResponse(BaseModel):
    shap_values: List[Dict[str, Any]]
    decision_summary: str
    model_score: float

@router.post("/explain", response_model=ExplainResponse)
async def explain_fraud(request: ExplainRequest):
    explanation = engine.generate_explanation(
        request.transaction, 
        request.features, 
        request.model_score
    )
    return ExplainResponse(
        shap_values=explanation.get("shap_values", []),
        decision_summary=explanation.get("decision_summary", ""),
        model_score=explanation.get("model_score", 0.0)
    )
