# app/services/session_service.py
import logging
from typing import Dict, List, Optional
import uuid
from datetime import datetime
from ..models.session import ChatSession, ChatSessionCreate
from ..models.chat import ChatMessage
from .database_service import firestore_service

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class SessionService:
    def __init__(self):
        self.db = firestore_service
        logger.debug("Session service initialized with Firestore database")
    
    def create_session(self, user_id: str) -> ChatSession:
        """Create a new chat session"""
        logger.debug(f"Creating new session for user: {user_id}")
        session_id = str(uuid.uuid4())
        new_session = ChatSessionCreate(
            session_id=session_id,
            user_id=user_id,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        session = self.db.create_session(new_session)
        logger.debug(f"Session created successfully: {session_id}")
        return session
    
    def get_session(self, session_id: str) -> Optional[ChatSession]:
        """Get session by ID"""
        logger.debug(f"Getting session by ID: {session_id}")
        return self.db.get_session(session_id)
    
    def get_user_sessions(self, user_id: str) -> List[ChatSession]:
        """Get all sessions for a user"""
        logger.debug(f"Getting all sessions for user: {user_id}")
        return self.db.get_user_sessions(user_id)
    
    def add_message(self, session_id: str, message: ChatMessage):
        """Add message to session"""
        logger.debug(f"Adding message to session: {session_id}")
        self.db.add_message(session_id, message)
    
    def verify_session_owner(self, session_id: str, user_id: str) -> bool:
        """Verify if user owns the session"""
        logger.debug(f"Verifying session ownership - session: {session_id}, user: {user_id}")
        return self.db.verify_session_owner(session_id, user_id)

# Create singleton instance
session_service = SessionService()