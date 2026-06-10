from fastapi import APIRouter, Depends, BackgroundTasks, Request
from afios.ingestion.schemas import TransactionIngest, IngestResponse
from afios.common.security import get_current_user
import json
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

async def publish_to_kafka(transaction: TransactionIngest, tenant_id: str):
    # Mocking kafka publish
    logger.info(f"Publishing to afios.transactions.raw for tenant {tenant_id}: {transaction.tx_id}")
    # In a real scenario, use aiokafka producer here

@router.post("/ingest", response_model=IngestResponse, status_code=202)
async def ingest_transaction(
    request: Request,
    transaction: TransactionIngest,
    background_tasks: BackgroundTasks,
    # user: dict = Depends(get_current_user) # Uncomment when auth is strictly enforced
):
    """
    Ingest a new transaction and publish it to the event stream for processing.
    """
    # tenant_id = user.get("tenant_id", "default")
    tenant_id = request.headers.get("X-Tenant-ID", "default")
    
    # Send to background task to avoid blocking API response
    background_tasks.add_task(publish_to_kafka, transaction, tenant_id)
    
    return IngestResponse(
        status="accepted",
        tx_id=transaction.tx_id,
        message="Transaction accepted for processing."
    )
