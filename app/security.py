# app/security.py (Versão Corrigida)

import os
from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from sqlalchemy.orm import Session # <-- Importamos a Session para type hinting

# Importações do nosso projeto
from .database import get_db # <-- ## CORREÇÃO AQUI ##: Importamos a função get_db
from .models import usuario_model

load_dotenv()

# --- Configuração do JWT ---
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# --- Configuração do Hashing ---
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# --- Esquema para os dados do token ---
class TokenData(BaseModel):
    username: Optional[str] = None
    role: Optional[str] = None

# --- Funções de Segurança ---

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# --- Função de Dependência Principal ---
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)): # <-- ## CORREÇÃO AQUI ##
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username, role=payload.get("role"))
    except JWTError:
        raise credentials_exception
    
    user = db.query(usuario_model.Usuario).filter(usuario_model.Usuario.username == token_data.username).first()
    if user is None:
        raise credentials_exception
    return user