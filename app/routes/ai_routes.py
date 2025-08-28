from fastapi import APIRouter, HTTPException
from app.models.schemas import (
    LLMRequest, LLMResponse, MessageClassification,
    AIStatusResponse, APIResponse
)
from app.services import ai_service
from app.utils.logger import logger

router = APIRouter()

@router.post("/chat", response_model=LLMResponse)
async def chat_with_ai(request: LLMRequest):
    """Chat with AI assistant"""
    try:
        return ai_service.chat_with_ai(request)
    except Exception as e:
        logger.error(f"Error in AI chat endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail="AI service error")

@router.post("/classify", response_model=MessageClassification)
async def classify_message(request: LLMRequest):
    """Classify user message"""
    try:
        return ai_service.classify_message(request)
    except Exception as e:
        logger.error(f"Error in message classification endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail="Classification service error")

@router.get("/status", response_model=AIStatusResponse)
async def get_ai_status():
    """Get AI system status"""
    try:
        return ai_service.get_ai_status()
    except Exception as e:
        logger.error(f"Error getting AI status: {str(e)}")
        raise HTTPException(status_code=500, detail="Status check failed")