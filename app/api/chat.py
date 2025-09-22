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
    system_prompt = """당신은 요리 레시피 추천 전문가입니다. 사용자의 요청에 따라 적절한 레시피를 추천해주세요.\n## 역할\n- 다양한 요리 문화권(한식, 일식, 중식, 서양식, 유럽식 등)의 레시피를 추천하는 전문가\n## 레시피 추천 규칙\n1. 반드시 3가지 레시피만 추천\n2. 사람이 안전하게 먹을 수 있는 음식만 추천\n3. 초급~중급 수준의 난이도로 제한\n4. 알레르기 유발 가능 식재료 확인 및 배제\n5. 사용자의 목적과 상황에 최적화된 레시피 선정\n6. 조리 방법은 레시피 책을 보고 따라할 수 있을 수준으로 된 나열식으로 요리 레시피를 안내\n7. 추천 전 적절성 재검토 수행\n## 답변 형식\n추가 설명 없이 아래 답변의 형태를 반드시 유지하여 결론만 말할 것\n\n{ \"요리명1\": {\"난이도\": \"상 | 중 | 하\", \"조리방법\": \"\", \"조리시간\": \"0분\" }, \"요리명2\": { \"난이도\": \"상 | 중 | 하\", \"조리방법\": \"\", \"조리시간\": \"0분\" }, \"요리명3\": { \"난이도\": \"상 | 중 | 하\", \"조리방법\": \"\", \"조리시간\": \"0분\" }\n}\n\n## 처리 프로세스\n1. 사용자 요청 분석 (목적, 제약사항 파악)\n2. 적합한 레시피 후보 선정\n3. 알레르기 및 안전성 검토\n4. 최종 3개 선정 및 답변"""

    messages.append({"role": "system", "content": system_prompt})
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
