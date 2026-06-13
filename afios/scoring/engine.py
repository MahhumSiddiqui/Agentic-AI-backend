import os
import pickle
import random
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

try:
    import pandas as pd
    import xgboost as xgb
    HAS_ML_LIBRARIES = True
except ImportError as e:
    logger.error(f"Failed to import ML libraries (pandas/xgboost): {e}")
    HAS_ML_LIBRARIES = False

class FraudScoringEngine:
    def __init__(self, model_version="v1.0.0"):
        self.model_version = model_version
        self.model = None
        self.feature_names = None
        
        if not HAS_ML_LIBRARIES:
            logger.warning("ML libraries not available. Engine will run in failsafe mode.")
            return

        CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
        MODEL_PATH = os.path.abspath(os.path.join(CURRENT_DIR, "..", "models", "fraud_model.pkl"))
        
        try:
            if os.path.exists(MODEL_PATH):
                with open(MODEL_PATH, "rb") as f:
                    artifact = pickle.load(f)
                    
                # Support both pure model files (backward compatibility) and new artifact dictionaries
                if isinstance(artifact, dict) and "model" in artifact and "feature_names" in artifact:
                    self.model = artifact["model"]
                    self.feature_names = artifact["feature_names"]
                else:
                    self.model = artifact
                    # Default feature names if schema is missing
                    self.feature_names = ["Time"] + [f"V{i}" for i in range(1, 29)] + ["Amount"]
                    
                logger.info(f"Successfully loaded ML model and feature schema from {MODEL_PATH}")
            else:
                logger.error(f"Model file not found at {MODEL_PATH}")
        except Exception as e:
            logger.error(f"Failed to load fraud detection model: {e}", exc_info=True)

    def predict(self, transaction: Dict[str, Any], features: Dict[str, Any]) -> float:
        """
        Predict probability of transaction being fraudulent.
        """
        if not HAS_ML_LIBRARIES or self.model is None or self.feature_names is None:
            logger.warning("ML model not available or loaded. Returning failsafe score of 0.5")
            return 0.5

        try:
            # Extract features safely, preserving the exact order from training schema
            feat_dict = {}
            for feature_name in self.feature_names:
                # First try features dict (exact match or lowercased)
                if feature_name in features:
                    val = features[feature_name]
                elif feature_name.lower() in features:
                    val = features[feature_name.lower()]
                # Then try transaction dict
                elif feature_name in transaction:
                    val = transaction[feature_name]
                elif feature_name.lower() in transaction:
                    val = transaction[feature_name.lower()]
                else:
                    # Fallback default
                    val = 0.0
                    
                feat_dict[feature_name] = float(val)
            
            # Convert to DataFrame
            df = pd.DataFrame([feat_dict], columns=self.feature_names)
            
            # Predict probability
            proba = self.model.predict_proba(df)[0]
            if len(proba) > 1:
                ml_score = float(proba[1])
            else:
                ml_score = float(proba[0])
                
            # Ensure it is between 0 and 1
            ml_score = max(0.0, min(1.0, ml_score))
            return ml_score
            
        except Exception as e:
            logger.error(f"Error during ML inference: {e}", exc_info=True)
            return 0.5
