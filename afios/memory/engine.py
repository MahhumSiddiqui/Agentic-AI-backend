from typing import Dict, Any

class FraudMemoryEngine:
    def __init__(self):
        # Redis connection would be initialized here
        pass

    def get_deviation_score(self, entity_id: str, transaction: Dict[str, Any]) -> float:
        """
        Calculates how much the current transaction deviates from the known historical baseline.
        """
        # Mocking deviation calculation
        amount = transaction.get("amount", 0)
        
        # Assume baseline is 50
        baseline_avg = 50
        deviation = abs(amount - baseline_avg) / (baseline_avg + 1)
        
        return min(deviation / 10.0, 1.0) # Normalize
