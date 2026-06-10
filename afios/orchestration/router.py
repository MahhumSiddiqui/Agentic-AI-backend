from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict, Any
from afios.orchestration.engine import RiskOrchestrationEngine
from afios.scoring.engine import FraudScoringEngine
from afios.rules.evaluator import RuleEvaluator
from afios.rules.router import active_rules
from afios.explainability.engine import ExplainabilityEngine
from afios.memory.engine import FraudMemoryEngine
from afios.dna.engine import FraudDNAEngine
from afios.behavioral.engine import BehavioralIntelligenceEngine
from afios.graph.engine import GraphIntelligenceEngine

router = APIRouter()

class RiskDecisionRequest(BaseModel):
    transaction: Dict[str, Any]
    features: Dict[str, Any]

class RiskDecisionResponse(BaseModel):
    tx_id: str
    final_score: float
    risk_tier: str
    decision: str
    breakdown: Dict[str, float]

orchestrator = RiskOrchestrationEngine()
ml_engine = FraudScoringEngine()
explainability_engine = ExplainabilityEngine()
memory_engine = FraudMemoryEngine()
dna_engine = FraudDNAEngine()
behavioral_engine = BehavioralIntelligenceEngine()
graph_engine = GraphIntelligenceEngine()

@router.post("/decision", response_model=RiskDecisionResponse)
async def get_decision(request: RiskDecisionRequest):
    # 1. Run ML Model
    ml_score = ml_engine.predict(request.transaction, request.features)
    
    # 2. Run Rules Engine
    rules_engine = RuleEvaluator(active_rules)
    rule_score = rules_engine.evaluate(request.transaction)
    
    # 3. Call other engines
    graph_score = graph_engine.get_graph_risk(request.transaction.get("device_id", ""), request.transaction)
    behavior_score = behavioral_engine.analyze_behavior(request.transaction)
    memory_score = memory_engine.get_deviation_score(request.transaction.get("customer_id", ""), request.transaction)
    dna_score = dna_engine.get_dna_risk(request.transaction.get("customer_id", ""), request.transaction)
    scores = {
        "ml_score": ml_score,
        "rule_score": rule_score,
        "graph_score": graph_score,
        "behavior_score": behavior_score,
        "memory_score": memory_score,
        "dna_score": dna_score
    }
    
    # 4. Orchestrate
    final_score, tier, decision = orchestrator.evaluate_risk(scores)
    
    return RiskDecisionResponse(
        tx_id=request.transaction.get("tx_id", "unknown"),
        final_score=final_score,
        risk_tier=tier,
        decision=decision,
        breakdown=scores
    )
