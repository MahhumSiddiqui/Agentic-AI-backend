import os
import pickle
import logging
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_score, recall_score, f1_score, roc_auc_score, classification_report
import xgboost as xgb

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("AFIOS.ML_Train")

def train_fraud_model():
    # 1. Load the dataset
    data_path = os.path.join(os.path.dirname(__file__), "..", "data", "creditcard.csv")
    data_path = os.path.abspath(data_path)
    
    logger.info(f"Loading dataset from {data_path}")
    if not os.path.exists(data_path):
        logger.error(f"Dataset not found at {data_path}")
        return
        
    df = pd.read_csv(data_path)
    
    # 2. Prepare features and target
    target_col = "Class"
    if target_col not in df.columns:
        logger.error(f"Target column '{target_col}' not found in dataset.")
        return
        
    X = df.drop(columns=[target_col])
    y = df[target_col]
    feature_names = list(X.columns)
    
    logger.info(f"Features: {feature_names}")
    
    # 3. Stratified split (80/20)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # 4. Handle class imbalance
    # scale_pos_weight = sum(negative instances) / sum(positive instances)
    num_neg = (y_train == 0).sum()
    num_pos = (y_train == 1).sum()
    scale_pos_weight = num_neg / num_pos
    logger.info(f"Class imbalance: {num_neg} Negative, {num_pos} Positive. scale_pos_weight = {scale_pos_weight:.2f}")
    
    # 5. Initialize and train XGBoostClassifier
    logger.info("Initializing XGBClassifier...")
    model = xgb.XGBClassifier(
        scale_pos_weight=scale_pos_weight,
        random_state=42,
        eval_metric="logloss",
        n_estimators=100,
        max_depth=6,
        learning_rate=0.1,
        use_label_encoder=False
    )
    
    logger.info("Training the model...")
    model.fit(X_train, y_train)
    
    # 6. Evaluate model
    logger.info("Evaluating model on test set...")
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)[:, 1]
    
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    roc_auc = roc_auc_score(y_test, y_pred_proba)
    
    logger.info(f"Precision: {precision:.4f}")
    logger.info(f"Recall:    {recall:.4f}")
    logger.info(f"F1-Score:  {f1:.4f}")
    logger.info(f"ROC-AUC:   {roc_auc:.4f}")
    logger.info("\nClassification Report:\n" + classification_report(y_test, y_pred))
    
    # 7. Save model and feature schema
    output_dir = os.path.join(os.path.dirname(__file__), "..", "models")
    os.makedirs(output_dir, exist_ok=True)
    model_path = os.path.abspath(os.path.join(output_dir, "fraud_model.pkl"))
    
    # We save a dictionary containing both the model and the expected feature names
    artifact = {
        "model": model,
        "feature_names": feature_names
    }
    
    with open(model_path, "wb") as f:
        pickle.dump(artifact, f)
        
    logger.info(f"Model and feature schema saved to {model_path}")

if __name__ == "__main__":
    train_fraud_model()
