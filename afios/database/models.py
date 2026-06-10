from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, JSON, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from afios.common.database import Base

class Tenant(Base):
    __tablename__ = "tenants"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"))
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String) # Admin, Analyst, Manager
    is_active = Column(Boolean, default=True)

class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(String, primary_key=True, index=True) # UUID
    tenant_id = Column(Integer, ForeignKey("tenants.id"))
    tx_type = Column(String) # Card, ACH, Wire, Wallet, Merchant
    amount = Column(Float)
    currency = Column(String)
    timestamp = Column(DateTime)
    customer_id = Column(String, index=True)
    merchant_id = Column(String)
    device_id = Column(String)
    location = Column(String)
    raw_data = Column(JSON) # Store full payload
    
    # Relationships
    prediction = relationship("Prediction", back_populates="transaction", uselist=False)

class Prediction(Base):
    __tablename__ = "predictions"
    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(String, ForeignKey("transactions.id"))
    model_version = Column(String)
    ml_score = Column(Float)
    rule_score = Column(Float)
    graph_score = Column(Float)
    behavior_score = Column(Float)
    memory_score = Column(Float)
    dna_score = Column(Float)
    final_risk_score = Column(Float)
    risk_tier = Column(String) # LOW, MEDIUM, HIGH, CRITICAL
    decision_recommendation = Column(String) # APPROVE, REVIEW, DECLINE
    
    transaction = relationship("Transaction", back_populates="prediction")
    explanation = relationship("Explanation", back_populates="prediction", uselist=False)

class Explanation(Base):
    __tablename__ = "explanations"
    id = Column(Integer, primary_key=True, index=True)
    prediction_id = Column(Integer, ForeignKey("predictions.id"))
    shap_values = Column(JSON)
    feature_contributions = Column(JSON)
    decision_summary = Column(Text)
    
    prediction = relationship("Prediction", back_populates="explanation")

class Alert(Base):
    __tablename__ = "alerts"
    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"))
    transaction_id = Column(String, ForeignKey("transactions.id"))
    status = Column(String) # NEW, REVIEW, ESCALATED, CONFIRMED_FRAUD, FALSE_POSITIVE, CLOSED
    priority = Column(String) # HIGH, MEDIUM, LOW
    created_at = Column(DateTime, default=datetime.utcnow)

class Case(Base):
    __tablename__ = "cases"
    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"))
    alert_id = Column(Integer, ForeignKey("alerts.id"))
    assigned_to = Column(Integer, ForeignKey("users.id"), nullable=True)
    status = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

class Rule(Base):
    __tablename__ = "rules"
    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"))
    name = Column(String)
    description = Column(String)
    rule_logic = Column(JSON) # DSL logic
    action = Column(String)
    is_active = Column(Boolean, default=True)

class Profile(Base):
    """Customer, Device, or Merchant profiles for Memory and DNA Engines"""
    __tablename__ = "profiles"
    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"))
    entity_type = Column(String) # CUSTOMER, DEVICE, MERCHANT
    entity_id = Column(String, index=True)
    behavioral_baselines = Column(JSON)
    dna_fingerprint = Column(JSON) # Vector or encoded features
    updated_at = Column(DateTime, default=datetime.utcnow)
