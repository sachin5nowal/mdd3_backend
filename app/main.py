# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from app.routers import auth





def create_application() -> FastAPI:
    app = FastAPI( title=settings.API_TITLE, version=settings.API_VERSION )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
        allow_methods=settings.CORS_ALLOW_METHODS,
        allow_headers=settings.CORS_ALLOW_HEADERS,
    )
    
    # Include routers - make sure these match the module names
    app.include_router(auth.router)
    # app.include_router(chat.router)
    # app.include_router(sessions.router)  
    
    # Root endpoint
    @app.get("/")
    async def root():
        return {"message": "AI Chat API - Firebase Auth Working!"}
    
    return app

app = create_application()