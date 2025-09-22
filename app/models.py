from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum

class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"

class ChatMessage(BaseModel):
    role: MessageRole
    content: str

class RecipeRecommendRequest(BaseModel):
    message: str = Field(default="당근,양배추,김치,밥", description="냉장고 속 남은 식재료")
    max_tokens: int = Field(default=3000, ge=1000, le=4096, description="최대 토큰 수")
    temperature: float = Field(default=0.3, ge=0.0, le=1.0, description="다양성 조절")

class MealGenerateRequest(BaseModel):
    message: str = Field(default="{\n  \"title\": \"9월 3주차 감량 플랜\",\n  \"period\": \"weekly\",\n  \"goals\": \"weight_loss\",\n  \"age\": 28,\n  \"gender\": \"female\",\n  \"basic_metabolism\": 1380\n}", description="사용자 식단 목적")
    max_tokens: int = Field(default=4096, ge=2000, le=4096, description="최대 토큰 수")
    temperature: float = Field(default=0.3, ge=0.0, le=1.0, description="다양성 조절")

class ConversationRequest(BaseModel):
    messages: List[ChatMessage] = Field(..., description="대화 히스토리")
    max_tokens: int = Field(default=256, ge=1, le=4096)
    temperature: float = Field(default=0.5, ge=0.0, le=1.0)

class ChatResponse(BaseModel):
    success: bool
    message: str
    tokens_used: Optional[int] = None
    model: str = "hyperclova-x"

class ErrorResponse(BaseModel):
    success: bool = False
    error: str
    detail: Optional[str] = None
