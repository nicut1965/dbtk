from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.user import User
from app.core.security import verify_password, create_access_token

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/login")
def login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        return RedirectResponse("/login?error=1", status_code=302)

    token = create_access_token({"sub": user.email, "role": user.role})

    response = RedirectResponse("/", status_code=302)
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True
    )
    return response
