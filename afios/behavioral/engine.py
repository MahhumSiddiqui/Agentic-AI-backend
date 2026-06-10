from typing import Dict, Any

class BehavioralIntelligenceEngine:
    def __init__(self):
        pass

    def analyze_behavior(self, transaction: Dict[str, Any]) -> float:
        """
        Performs anomaly detection (Isolation Forest simulation) and temporal analysis.
        """
        # Temporal risk mock: e.g. 3 AM transactions are riskier
        time_hour = transaction.get("timestamp").hour if transaction.get("timestamp") else 12
        
        if time_hour < 5:
            return 0.6
        return 0.1
