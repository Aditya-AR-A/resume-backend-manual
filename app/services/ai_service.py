"""
AI Service Module

Handles AI-related operations including chat, classification, and provider management.
"""

import time
from typing import Dict, Any, Optional

from app.config.settings import app_settings
from app.models.schemas import (
    LLMProvider, LLMRequest, LLMResponse, MessageClassification,
    AIStatusResponse, ProviderInfo
)
from app.utils.logger import logger


class AIService:
    """Service for AI operations and provider management"""

    def __init__(self):
        self.providers = self._initialize_providers()

    def _initialize_providers(self) -> Dict[LLMProvider, Any]:
        """Initialize available AI providers"""
        providers = {}

        # This is a placeholder for actual provider initialization
        # In a real implementation, you would initialize actual client libraries
        # like OpenAI, Anthropic, Groq, etc.

        if app_settings.groq_api_key:
            providers[LLMProvider.GROQ] = {
                "api_key": app_settings.groq_api_key,
                "model": app_settings.groq_model,
                "base_url": None
            }

        if app_settings.openai_api_key:
            providers[LLMProvider.OPENAI] = {
                "api_key": app_settings.openai_api_key,
                "model": app_settings.openai_model,
                "base_url": None
            }

        if app_settings.anthropic_api_key:
            providers[LLMProvider.ANTHROPIC] = {
                "api_key": app_settings.anthropic_api_key,
                "model": app_settings.anthropic_model,
                "base_url": None
            }

        return providers

    def chat_with_ai(self, request: LLMRequest) -> LLMResponse:
        """Process a chat request with AI"""
        try:
            logger.info(f"Processing AI chat request from user: {request.user_id}")

            # For now, return a mock response
            # In a real implementation, you would call the actual AI provider

            provider_info = self._get_provider_info(app_settings.primary_llm_provider)

            return LLMResponse(
                content_type="text",
                content=self._get_mock_response(request.message),
                confidence=0.85,
                provider_info=provider_info,
                processing_time=0.15
            )

        except Exception as e:
            logger.error(f"Error in AI chat service: {str(e)}")
            raise

    def classify_message(self, request: LLMRequest) -> MessageClassification:
        """Classify a user message"""
        try:
            logger.info(f"Classifying message: {request.message[:50]}...")

            # Mock classification logic
            # In a real implementation, you would use AI to classify the message

            message_type = self._classify_message_type(request.message)
            intent = self._extract_intent(request.message)

            return MessageClassification(
                type=message_type,
                intent=intent,
                confidence=0.78,
                entities=self._extract_entities(request.message)
            )

        except Exception as e:
            logger.error(f"Error in message classification: {str(e)}")
            raise

    def get_ai_status(self) -> AIStatusResponse:
        """Get the current status of AI services"""
        try:
            # Check provider availability
            provider_status = {}
            components_status = {
                "llm_service": "operational",
                "cache": "operational" if app_settings.cache_enabled else "disabled"
            }

            for provider, config in self.providers.items():
                # In a real implementation, you would check actual connectivity
                provider_status[provider.value] = True

            # Determine overall status
            has_providers = len(provider_status) > 0
            status = "operational" if has_providers else "degraded"

            return AIStatusResponse(
                status=status,
                components=components_status,
                providers=provider_status
            )

        except Exception as e:
            logger.error(f"Error getting AI status: {str(e)}")
            raise

    def _get_provider_info(self, provider: LLMProvider) -> ProviderInfo:
        """Get provider information for response"""
        if provider in self.providers:
            config = self.providers[provider]
            return ProviderInfo(
                provider=provider,
                model=config["model"],
                endpoint=config.get("base_url"),
                latency=0.1,  # Mock latency
                tokens_used=150,  # Mock token usage
                cost_estimate=0.002  # Mock cost
            )
        else:
            return ProviderInfo(
                provider=provider,
                model="unknown",
                latency=0.0,
                tokens_used=0,
                cost_estimate=0.0
            )

    def _get_mock_response(self, message: str) -> str:
        """Generate a mock AI response based on the input message"""
        # Simple keyword-based response generation
        message_lower = message.lower()

        if "project" in message_lower:
            return "I'd be happy to tell you about my projects! I have several interesting projects in data science, machine learning, and web development. You can check out my portfolio for more details."
        elif "experience" in message_lower or "work" in message_lower:
            return "I have experience in software development, data analysis, and machine learning. I've worked on various projects involving Python, React, and cloud technologies."
        elif "certificate" in message_lower or "certification" in message_lower:
            return "I hold several certifications in data science, machine learning, and software development. These include certifications from Google, AWS, and various online learning platforms."
        elif "contact" in message_lower or "email" in message_lower:
            return "You can reach out to me through the contact form on my website, or find my contact information in the portfolio."
        else:
            return "Hello! I'm here to help you learn more about my portfolio, projects, experience, and skills. Feel free to ask me anything specific!"

    def _classify_message_type(self, message: str) -> str:
        """Classify the type of message"""
        from app.models.schemas import MessageType

        message_lower = message.lower()

        if any(word in message_lower for word in ["what", "how", "tell me", "explain"]):
            return MessageType.QUESTION
        elif any(word in message_lower for word in ["do", "create", "build", "make"]):
            return MessageType.COMMAND
        elif any(word in message_lower for word in ["find", "search", "look for"]):
            return MessageType.SEARCH
        else:
            return MessageType.CONVERSATION

    def _extract_intent(self, message: str) -> str:
        """Extract the intent from the message"""
        message_lower = message.lower()

        if "project" in message_lower:
            return "project_inquiry"
        elif "experience" in message_lower or "work" in message_lower:
            return "experience_inquiry"
        elif "certificate" in message_lower:
            return "certificate_inquiry"
        elif "skill" in message_lower:
            return "skill_inquiry"
        elif "contact" in message_lower:
            return "contact_inquiry"
        else:
            return "general_inquiry"

    def _extract_entities(self, message: str) -> Dict[str, Any]:
        """Extract entities from the message"""
        # Simple entity extraction - in a real implementation,
        # you would use NLP libraries like spaCy
        entities = {}

        message_lower = message.lower()

        # Extract technology mentions
        technologies = ["python", "react", "javascript", "machine learning", "data science"]
        mentioned_tech = [tech for tech in technologies if tech in message_lower]
        if mentioned_tech:
            entities["technologies"] = mentioned_tech

        return entities


# Create global AI service instance
ai_service = AIService()
