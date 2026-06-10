import json
from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)

class RuleEvaluator:
    def __init__(self, rules: List[Dict[str, Any]]):
        self.rules = rules

    def evaluate(self, transaction: Dict[str, Any]) -> float:
        """
        Evaluates a set of dynamic rules against the transaction payload.
        Returns a rule score (e.g., 0.0 to 1.0)
        """
        score = 0.0
        triggered_rules = []
        
        for rule in self.rules:
            if self._apply_rule(rule, transaction):
                triggered_rules.append(rule["name"])
                # Simple additive scoring for demo purposes
                score += rule.get("weight", 0.1)
                
        logger.info(f"Triggered rules: {triggered_rules}")
        return min(score, 1.0)

    def _apply_rule(self, rule: Dict[str, Any], transaction: Dict[str, Any]) -> bool:
        # Example simple DSL evaluator
        condition = rule.get("condition", {})
        field = condition.get("field")
        operator = condition.get("operator")
        value = condition.get("value")
        
        tx_val = transaction.get(field)
        
        if tx_val is None:
            return False
            
        if operator == "gt":
            return tx_val > value
        elif operator == "lt":
            return tx_val < value
        elif operator == "eq":
            return tx_val == value
        elif operator == "in":
            return tx_val in value
            
        return False
