from typing import Dict, Any

class AIInvestigationAgent:
    def __init__(self):
        # Initialize LLM client (e.g. OpenAI) here
        pass

    def generate_narrative(self, transaction: Dict[str, Any], scores: Dict[str, float], explanation: Dict[str, Any]) -> str:
        """
        Uses an LLM (mocked here) to write a human-readable investigation summary.
        """
        amount = transaction.get("amount", 0)
        ml_score = scores.get("ml_score", 0)
        
        # In production, this would be a prompt to an LLM:
        # prompt = f"Analyze this transaction {transaction} and these features {explanation}..."
        
        narrative = f"This transaction for ${amount} was flagged by the ML model with a score of {ml_score}. "
        
        if scores.get("graph_score", 0) > 0.8:
            narrative += "Additionally, the device used is associated with a known fraud ring. "
            
        if scores.get("rule_score", 0) > 0:
            narrative += "Business rules regarding high velocity or high amount were triggered. "
            
        narrative += "\n" + explanation.get("decision_summary", "")
        
        return narrative
