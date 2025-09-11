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

class ChatRequest(BaseModel):
    message: str = Field(..., description="사용자 메시지")
    max_tokens: int = Field(default=256, ge=1, le=4096, description="최대 토큰 수")
    temperature: float = Field(default=0.5, ge=0.0, le=1.0, description="창의성 조절")
    system_prompt: Optional[str] = Field(default=None, description="시스템 프롬프트")

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