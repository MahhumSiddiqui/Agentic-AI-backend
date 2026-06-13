import os
import sys

# Ensure afios is in the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from afios.scoring.engine import FraudScoringEngine

def run_tests():
    print("Initializing FraudScoringEngine...")
    engine = FraudScoringEngine()
    
    if engine.model is None:
        print("WARNING: Model failed to load. Is HAS_ML_LIBRARIES False or the pkl file missing?")
    else:
        print("Model loaded successfully.")
        
    print("\nTest 1: Normal transaction with some matching features")
    tx_1 = {
        "amount": 125.50,
        "customer_id": "cust_123"
    }
    feat_1 = {
        "V1": -1.3,
        "V2": 0.5,
        "Time": 1000.0
    }
    
    score_1 = engine.predict(tx_1, feat_1)
    print(f"Score 1: {score_1} (Type: {type(score_1)})")
    
    print("\nTest 2: Fraud-like high amount transaction with different casing")
    tx_2 = {
        "Amount": 15000.0,
    }
    feat_2 = {
        "v1": -5.0,
        "v2": 2.0,
        "time": 2000.0
    }
    
    score_2 = engine.predict(tx_2, feat_2)
    print(f"Score 2: {score_2} (Type: {type(score_2)})")
    
    print("\nTest 3: Empty features and transaction")
    score_3 = engine.predict({}, {})
    print(f"Score 3: {score_3} (Type: {type(score_3)})")

if __name__ == "__main__":
    run_tests()
