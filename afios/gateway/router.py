from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from afios.common.security import verify_password, create_access_token, get_password_hash
from afios.common.config import settings

router = APIRouter()

# Mock user database
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

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    if not verify_password(form_data.password, user_dict["hashed_password"]):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    access_token = create_access_token(
        data={"sub": user_dict["username"], "tenant_id": user_dict["tenant_id"]}
    )
    return {"access_token": access_token, "token_type": "bearer"}
