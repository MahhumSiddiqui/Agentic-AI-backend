import json
from typing import Dict, Any

class ExplainabilityEngine:
    def __init__(self):
        pass

    def generate_explanation(self, transaction: Dict[str, Any], features: Dict[str, Any], model_score: float) -> Dict[str, Any]:
        """
        Generate SHAP-like explanations and feature contributions.
        """
        # Mocking SHAP values
        top_features = [
            {"feature": "transaction_velocity_24h", "contribution": 0.35, "value": 15},
            {"feature": "distance_from_home", "contribution": 0.25, "value": 1200},
            {"feature": "merchant_risk_score", "contribution": 0.15, "value": 0.8}
        ]
        
        narrative = "The transaction was flagged due to high velocity in the last 24 hours, " \
                    "combined with an unusual distance from the customer's typical locations."

        return {
            "shap_values": top_features,
            "decision_summary": narrative,
            "model_score": model_score
        }
