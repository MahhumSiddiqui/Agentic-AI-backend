import random
from typing import Dict, Any

class FraudScoringEngine:
    def __init__(self, model_version="v1.0.0"):
        self.model_version = model_version
        # In a real app, load XGBoost / LightGBM models here using mlflow or local artifacts

    def predict(self, transaction: Dict[str, Any], features: Dict[str, Any]) -> float:
        """
        Mock inference for ML model. 
        In reality, this would prepare a feature vector and call `model.predict_proba()`.
        """
        # Simulated ML score logic based on amount
        amount = transaction.get("amount", 0)
        
        if amount > 10000:
            base_score = 0.85
        elif amount > 1000:
            base_score = 0.50
        else:
            base_score = 0.05
            
        # Add random noise
        noise = random.uniform(-0.05, 0.05)
        
        final_score = max(0.0, min(1.0, base_score + noise))
        return final_score
