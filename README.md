# Agentic Fraud Intelligence Operating System (AFIOS)

AFIOS is an enterprise-grade backend architecture for an AI-native Fraud Intelligence Operating System. It is designed to serve Banks, Fintechs, Payment Processors, Digital Wallet Providers, and Enterprise Financial Institutions.

## Core Features
- **Transaction Ingestion**: Real-time streaming via Kafka.
- **Fraud Scoring Engine**: Mocked support for XGBoost, LightGBM.
- **Dynamic Rules Engine**: On-the-fly DSL parsing and evaluation.
- **Explainability**: SHAP value approximations and natural language narratives.
- **Fraud Memory & DNA**: Historical baseline deviation and behavioral fingerprinting.
- **Risk Orchestration**: Composite engine merging ML, rules, graph, and behavior scores.
- **AI Copilot & Investigation Agent**: Simulated RAG-based analysis.

## Quick Start

1. Start the infrastructure (PostgreSQL, Redis, Kafka, API):
```bash
docker-compose up --build
```

2. Access the OpenAPI Specification and Swagger UI:
Navigate to `http://localhost:8000/docs`

## Architecture Highlights
- FastAPI / Pydantic for the API layer.
- SQLAlchemy / SQLModel async drivers for PostgreSQL.
- Celery / Kafka for asynchronous job processing and streaming.
- OpenTelemetry readiness for Observability.

## Model Architecture

AFIOS uses a pre-trained XGBoost fraud detection model stored as:

afios/models/fraud_model.pkl

Runtime scoring endpoints load the model directly and do not require the original training dataset.

The creditcard.csv dataset is only required when retraining the model.

For normal deployment:

* No AWS configuration is required
* No S3 access is required
* No dataset download is required

Users can run AFIOS directly using Docker:

docker compose up -d

and access:

http://localhost:8000/docs

Lab 15 SonarQube Analysis
