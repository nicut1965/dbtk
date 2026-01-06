from fastapi import Depends, Request
from jose import jwt, JWTError
from app.core.security import SECRET_KEY, ALGORITHM

def get_current_user(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        raise Exception("Neautorizat")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise Exception("Token invalid")
