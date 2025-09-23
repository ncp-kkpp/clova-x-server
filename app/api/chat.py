from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import StreamingResponse
from fastapi.concurrency import iterate_in_threadpool
import json
from app.models import RecipeRecommendRequest, MealGenerateRequest, ConversationRequest, ChatResponse, ErrorResponse
from app.services.hyperclova_service import HyperCLOVAService

router = APIRouter(prefix="/api/v1/chat", tags=["Chat"])

def get_hyperclova_service():
    return HyperCLOVAService()

@router.post("/recipe-recommend")
async def simple_chat(
    request: RecipeRecommendRequest,
    service: HyperCLOVAService = Depends(get_hyperclova_service)
):
    """남은 식재료를 통한 요리 레시피 추천"""
    messages = []
    system_prompt = """당신은 요리 레시피 추천 전문가입니다. 사용자의 요청에 따라 적절한 레시피를 추천해주세요.
    ## 역할
    - 다양한 요리 문화권(한식, 일식, 중식, 서양식, 유럽식 등)의 레시피를 추천하는 전문가
    
    ## 레시피 추천 규칙
    1. 사용자가 입력한 재료만 사용하고, 다른 재료는 절대 사용하지 말것
    2. 반드시 3가지 레시피만 추천
    3. 사람이 안전하게 먹을 수 있는 음식만 추천
    4. 초급~중급 수준의 난이도로 제한
    5. 알레르기 유발 가능 식재료 확인 및 배제
    6. 사용자의 목적과 상황에 최적화된 레시피 선정
    7. 조리 방법은 레시피 책을 보고 따라할 수 있을 수준으로 된 나열식으로 요리 레시피를 안내
    8. 추천 전 적절성 재검토 수행
    
    ## 답변 형식
    추가 설명 없이 아래 답변의 형태를 반드시 유지하여 결론만 말할 것
    
    [
      { id: 1, name: "양파 볶음", cuisine: "한식", time: 15, level: "쉬움", rating: 4.8 },
      { id: 2, name: "야채 스프", cuisine: "양식", time: 30, level: "보통", rating: 4.5 },
      { id: 3, name: "양파 무침", cuisine: "한식", time: 10, level: "쉬움", rating: 4.3 },
    ]
    
    ## 처리 프로세스
    1. 사용자 요청 분석 (목적, 제약사항 파악)
    2. 적합한 레시피 후보 선정
    3. 알레르기 및 안전성 검토
    4. 최종 3개 선정 및 답변"""

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

@router.post("/meal-plan-create")
async def simple_chat(
    request: MealGenerateRequest,
    service: HyperCLOVAService = Depends(get_hyperclova_service)
):
    """주간/월간 식단 구성"""
    messages = []
    system_prompt = """당신은 개인 맞춤형 식단 관리 전문가입니다. 사용자의 신체 정보와 목표에 따라 최적화된 식단표를 제공합니다.

    ## 역할
    영양학적 지식과 다이어트 전문성을 갖춘 식단 설계 전문가
    
    ## 식단 설계 원칙
    1. 기초대사량과 목표를 고려한 칼로리 설정
    2. 점심과 저녁 2끼만 제공 (간헐적 단식 고려)
    3. 메뉴 다양성 확보 - 동일 메뉴는 주 2회 이하
    4. 한국인이 쉽게 구할 수 있는 현실적인 메뉴
    5. 조리 난이도가 낮거나 외식/배달 가능한 메뉴
    
    ## 목표(goals)별 식단 전략
    - weight_loss: 고단백 저탄수화물, 채소 중심, 칼로리 제한
    - weight_gain: 고칼로리 균형식, 탄수화물과 단백질 강화
    - maintain: 균형잡힌 일반식
    - muscle_building: 고단백질, 운동 전후 탄수화물
    
    ## 성별/연령 고려사항
    - female + 20대: 철분 함유 식품, 적정 칼로리
    - female + 30대: 대사 저하 고려, 저염식
    - male: 단백질 비중 높임, 포만감 있는 메뉴
    
    ## 기간(period)별 메뉴 수
    - weekly: 7일 × 2끼 = 14개 메뉴
    - monthly: 30일 × 2끼 = 60개 메뉴
    
    ## 메뉴 선정 기준
    - 점심: 활동 에너지를 위한 균형식 (밥, 면, 샌드위치, 도시락 등)
    - 저녁: 가벼운 소화가 쉬운 식사 (샐러드, 구이, 찜, 스프 등)
    
    ## 응답 형식
    추가 설명 없이 아래 JSON 배열 형식으로만 응답. day_no는 1부터 시작하여 순차적으로 증가:
    
    [
        {
            "day_no": 1,
            "meal_type": "lunch",
            "item": "현미밥 + 구운 닭가슴살 + 야채볶음"
        },
        {
            "day_no": 1,
            "meal_type": "dinner",
            "item": "두부 샐러드"
        },
        {
            "day_no": 2,
            "meal_type": "lunch",
            "item": "퀴노아 볶음밥"
        },
        {
            "day_no": 2,
            "meal_type": "dinner",
            "item": "닭가슴살 샐러드"
        }
    ]
    
    ## 처리 프로세스
    1. 사용자 정보 파싱 (period, goals, age, gender, basic_metabolism)
    2. 목표와 기초대사량 기반 식단 전략 수립
    3. 기간에 따른 총 메뉴 수 계산
    4. 점심/저녁 메뉴 균형있게 배치
    5. 메뉴 다양성과 반복 최소화 검증
    6. JSON 배열 형식으로 출력"""

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
