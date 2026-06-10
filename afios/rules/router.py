from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import List, Dict, Any

router = APIRouter()

class RuleSchema(BaseModel):
    name: str
    description: str
    condition: Dict[str, Any]
    weight: float

# In-memory store for demo
active_rules: List[Dict[str, Any]] = []

@router.post("/create")
async def create_rule(rule: RuleSchema):
    active_rules.append(rule.dict())
    return {"status": "success", "message": f"Rule {rule.name} created dynamically"}

@router.get("/list")
async def list_rules():
    return {"rules": active_rules}
