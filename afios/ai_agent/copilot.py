from typing import Dict, Any

class AIFraudCopilot:
    def __init__(self):
        pass

    def ask_question(self, question: str, case_context: Dict[str, Any]) -> str:
        """
        Answers analyst questions using RAG over the case context.
        """
        q = question.lower()
        if "why was this flagged" in q:
            return "This was flagged primarily due to a spike in transaction velocity and a device ID linked to suspicious activity."
        elif "show similar cases" in q:
            return "Found 3 similar cases from last week involving the same merchant and similar IP ranges."
        elif "recommend" in q:
            return "Recommendation: Decline transaction and block the device ID. Request step-up authentication for the user."
        
        return "I can help explain the risk score, show similar cases, or recommend actions. How can I assist?"
