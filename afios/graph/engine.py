from typing import Dict, Any

class GraphIntelligenceEngine:
    def __init__(self):
        pass

    def get_graph_risk(self, entity_id: str, transaction: Dict[str, Any]) -> float:
        """
        Evaluates risk based on entity relationships (e.g. shared device ID across multiple accounts).
        """
        # Mock logic: if device ID is in known fraud ring, return high score
        device_id = transaction.get("device_id")
        known_fraud_devices = ["dev_123_fraud", "dev_456_ring"]
        
        if device_id in known_fraud_devices:
            return 0.95
        return 0.05
