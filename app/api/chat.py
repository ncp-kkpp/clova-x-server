from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import StreamingResponse
from fastapi.concurrency import iterate_in_threadpool
import json
from app.models import ChatRequest, ConversationRequest, ChatResponse, ErrorResponse
from app.services.hyperclova_service import HyperCLOVAService

router = APIRouter(prefix="/api/v1/chat", tags=["Chat"])

def get_hyperclova_service():
    return HyperCLOVAService()

@router.post("/recipe-recommend")
async def simple_chat(
    request: ChatRequest,
    service: HyperCLOVAService = Depends(get_hyperclova_service)
):
    """간단한 단일 메시지 채팅 (스트리밍)"""
    messages = []
    
    if request.system_prompt:
        messages.append({"role": "system", "content": request.system_prompt})
    
    messages.append({"role": "user", "content": request.message})

    async def stream_generator():
        sync_generator = service.chat_completion_stream_generator(
            messages=messages,
            max_tokens=request.max_tokens,
            temperature=request.temperature
        )
        async for chunk in iterate_in_threadpool(sync_generator):
            if chunk.get("success") is False:
                error_data = json.dumps(chunk, ensure_ascii=False)
                yield f"data: {error_data}\n\n"
                break

            if 'message' in chunk and 'content' in chunk['message']:
                content = chunk['message']['content']
                response_chunk = {
                    "success": True,
                    "message": content
                }
                json_string = json.dumps(response_chunk, ensure_ascii=False)
                yield f"data: {json_string}\n\n"

    return StreamingResponse(stream_generator(), media_type="text/event-stream")
