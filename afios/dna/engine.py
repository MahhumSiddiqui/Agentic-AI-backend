from typing import Dict, Any
import math

class FraudDNAEngine:
    def __init__(self):
        pass

    def calculate_similarity(self, current_dna: list, historical_dna: list) -> float:
        """
        Cosine similarity between DNA vectors.
        """
        if not current_dna or not historical_dna:
            return 0.0
            
        dot_product = sum(a * b for a, b in zip(current_dna, historical_dna))
        norm_a = math.sqrt(sum(a * a for a in current_dna))
        norm_b = math.sqrt(sum(b * b for b in historical_dna))
        
        if norm_a == 0 or norm_b == 0:
            return 0.0
            
        return dot_product / (norm_a * norm_b)

    def get_dna_risk(self, entity_id: str, transaction: Dict[str, Any]) -> float:
        """
        Mock DNA risk generation. Returns a risk score based on DNA drift.
        """
        # 1.0 means full drift (high risk)
        return 0.25 # Mocked risk score
