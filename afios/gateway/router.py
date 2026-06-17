from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from afios.common.security import (
    verify_password,
    create_access_token,
    get_password_hash
)

router = APIRouter()

# -----------------------
# DEMO USERS DB
# -----------------------
fake_users_db = {
    "admin": {
        "username": "admin",
        "full_name": "Admin User",
        "email": "admin@afios.com",
        "hashed_password": get_password_hash("admin123"),
        "disabled": False,
        "tenant_id": "tenant-001"
    }
}

# -----------------------
# LOGIN ENDPOINT
# -----------------------
@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = fake_users_db.get(form_data.username)

    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    if not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    token = create_access_token(
        data={
            "sub": user["username"],
            "tenant_id": user["tenant_id"]
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }