from typing import Dict, Any, Tuple
import logging

logger = logging.getLogger(__name__)

class RiskOrchestrationEngine:
    def __init__(self):
        # Weights for composite score
        self.weights = {
            "ml_score": 0.4,
            "rule_score": 0.2,
            "graph_score": 0.1,
            "behavior_score": 0.1,
            "memory_score": 0.1,
            "dna_score": 0.1
        }

    def evaluate_risk(self, scores: Dict[str, float]) -> Tuple[float, str, str]:
        """
        Calculate composite risk score and generate tier + decision.
        """
        final_score = 0.0
        for key, weight in self.weights.items():
            final_score += scores.get(key, 0.0) * weight
            
        final_score = round(final_score, 3)
        
        # Tier assignment
        if final_score >= 0.85:
            tier = "CRITICAL"
            decision = "DECLINE"
        elif final_score >= 0.65:
            tier = "HIGH"
            decision = "REVIEW"
        elif final_score >= 0.35:
            tier = "MEDIUM"
            decision = "REVIEW"
        else:
            tier = "LOW"
            decision = "APPROVE"
            
        logger.info(f"Composite Score: {final_score} | Tier: {tier} | Decision: {decision}")
        return final_score, tier, decision
