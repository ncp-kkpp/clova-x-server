from fastapi import APIRouter, HTTPException, Depends
from app.models import ChatRequest, ConversationRequest, ChatResponse, ErrorResponse
from app.services.hyperclova_service import HyperCLOVAService

router = APIRouter(prefix="/api/v1/chat", tags=["Chat"])

def get_hyperclova_service():
    return HyperCLOVAService()

@router.post("/simple", response_model=ChatResponse)
async def simple_chat(
    request: ChatRequest,
    service: HyperCLOVAService = Depends(get_hyperclova_service)
):
    """간단한 단일 메시지 채팅"""
    messages = []
    
    # 시스템 프롬프트가 있으면 추가
    if request.system_prompt:
        messages.append({"role": "system", "content": request.system_prompt})
    
    messages.append({"role": "user", "content": request.message})
    
    result = await service.chat_completion(
        messages=messages,
        max_tokens=request.max_tokens,
        temperature=request.temperature
    )
    
    if not result.get("success"):
        raise HTTPException(status_code=500, detail=result.get("error"))
    
    return ChatResponse(
        success=True,
        message=result["content"],
        tokens_used=result.get("tokens_used")
    )

@router.post("/conversation", response_model=ChatResponse)
async def conversation_chat(
    request: ConversationRequest,
    service: HyperCLOVAService = Depends(get_hyperclova_service)
):
    """대화 히스토리를 포함한 채팅"""
    messages = [{"role": msg.role.value, "content": msg.content} for msg in request.messages]
    
    result = await service.chat_completion(
        messages=messages,
        max_tokens=request.max_tokens,
        temperature=request.temperature
    )
    
    if not result.get("success"):
        raise HTTPException(status_code=500, detail=result.get("error"))
    
    return ChatResponse(
        success=True,
        message=result["content"],
        tokens_used=result.get("tokens_used")
    )