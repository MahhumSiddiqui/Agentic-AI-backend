from typing import Dict, Any
import datetime

class ModelGovernanceService:
    def __init__(self):
        self.model_registry = []

    def deploy_model(self, name: str, version: str, deployed_by: str) -> Dict[str, Any]:
        """
        Tracks model versions, approvals, and deployments.
        """
        record = {
            "name": name,
            "version": version,
            "status": "DEPLOYED",
            "deployed_by": deployed_by,
            "deployed_at": datetime.datetime.utcnow().isoformat()
        }
        self.model_registry.append(record)
        return record
        
    def rollback_model(self, name: str, version: str) -> Dict[str, Any]:
        return {"status": "success", "message": f"Rolled back {name} to {version}"}
