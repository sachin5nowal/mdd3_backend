# app/dependencies.py
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials
from .core.security import security
from .services.firebase_service import firebase_service


