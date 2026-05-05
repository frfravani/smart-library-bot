"""
API Routes for chatbot conversations.
"""
from typing import Optional
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from config.database import get_db
from services.chatbot_service import ChatbotService
from models import Conversation
import json

router = APIRouter()
chatbot_service = ChatbotService()


class ChatRequest(BaseModel):
    """Chat request model."""
    message: str
    user_id: Optional[str] = None


class ChatResponse(BaseModel):
    """Chat response model."""
    user_message: str
    bot_response: str
    intent: str
    entities: dict


@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest, db: Session = Depends(get_db)):
    """Send a message to the chatbot and get a response."""
    
    # Process message
    result = await chatbot_service.process_message(db, request.message)
    
    # Save to conversation history
    conversation = Conversation(
        user_id=request.user_id,
        user_message=result["user_message"],
        bot_response=result["bot_response"],
        intent=result["intent"],
        entities=json.dumps(result["entities"])
    )
    db.add(conversation)
    db.commit()
    
    return ChatResponse(
        user_message=result["user_message"],
        bot_response=result["bot_response"],
        intent=result["intent"],
        entities=result["entities"]
    )


@router.get("/history/{user_id}")
async def get_conversation_history(user_id: str, skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    """Get conversation history for a user."""
    conversations = db.query(Conversation).filter(Conversation.user_id == user_id).offset(skip).limit(limit).all()
    
    return [
        {
            "id": c.id,
            "user_message": c.user_message,
            "bot_response": c.bot_response,
            "intent": c.intent,
            "created_at": c.created_at
        }
        for c in conversations
    ]
