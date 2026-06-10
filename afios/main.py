from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from afios.common.config import settings
from afios.ingestion.router import router as ingestion_router
from afios.gateway.router import router as gateway_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Enterprise Fraud Intelligence Operating System API",
    version="1.0.0"
)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(gateway_router, prefix=f"{settings.API_V1_STR}/auth", tags=["Gateway & Auth"])
app.include_router(ingestion_router, prefix=f"{settings.API_V1_STR}/transactions", tags=["Ingestion"])

@app.get("/health", tags=["System"])
async def health_check():
    return {"status": "ok", "version": "1.0.0"}
