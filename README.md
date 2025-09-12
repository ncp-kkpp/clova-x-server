# Clova X Server

네이버 클라우드 플랫폼(NCP)의 HyperCLOVA X 모델을 기반으로 동작하는 FastAPI 백엔드 서버입니다. 이 서버는 간단한 텍스트 기반 채팅 및 대화형 채팅 기능을 API 형태로 제공합니다.

## 주요 기능

- **🤖 HyperCLOVA X 연동:** NCP의 강력한 언어 모델을 활용하여 자연스러운 대화를 생성합니다.
- **⚡️ FastAPI 기반:** 현대적이고 빠른 비동기 웹 프레임워크를 사용하여 높은 성능을 제공합니다.
- **💬 두 가지 채팅 모드:**
  - **Simple Chat:** 단일 메시지를 주고받는 간단한 채팅 API
  - **Conversation Chat:** 이전 대화 내용을 기억하며 이어가는 대화형 채팅 API
- **✅ Health Check:** 서버의 상태를 확인할 수 있는 헬스 체크 엔드포인트
- **🐳 Docker 지원:** Dockerfile이 포함되어 있어 손쉽게 컨테이너 환경에서 배포하고 운영할 수 있습니다.

## 프로젝트 구조

```
clova-x-server/
├── app/                  # FastAPI 애플리케이션 소스 코드
│   ├── api/              # API 라우터 (엔드포인트)
│   ├── services/         # 외부 서비스(HyperCLOVA X) 연동 로직
│   ├── models.py         # API 요청/응답 데이터 모델
│   ├── config.py         # 환경 변수 및 설정
│   └── main.py           # FastAPI 앱 초기화 및 메인 실행 파일
├── scripts/              # 보조 스크립트
├── Dockerfile            # Docker 이미지 빌드를 위한 설정 파일
├── requirements.txt      # Python 의존성 패키지 목록
└── README.md             # 프로젝트 안내 문서
```

## 시작하기

### 1. 사전 준비

- Python 3.11 이상
- Docker (선택 사항)
- Naver Cloud Platform API Key (HyperCLOVA X 사용 권한)

### 2. 설치

```bash
# 1. 프로젝트 클론
git clone https://github.com/ncp-kkpp/clova-x-server.git
cd clova-x-server

# 2. 가상환경 생성 및 활성화
python3 -m venv venv
source venv/bin/activate

# 3. 의존성 패키지 설치
pip install -r requirements.txt
```

### 3. 환경 변수 설정

프로젝트 루트 디렉터리에 `.env` 파일을 생성하고 아래 내용을 채워주세요.

```env
# .env

# Naver Cloud Platform에서 발급받은 HyperCLOVA X API 키
HYPERCLOVA_API_KEY="여기에_API_키를_입력하세요"
```

### 4. 서버 실행

#### 개발 환경

`uvicorn`을 사용하여 개발 서버를 실행합니다. 코드가 변경될 때마다 자동으로 재시작되어 편리합니다.

```bash
uvicorn app.main:app --reload
```

서버가 `http://127.0.0.1:8000`에서 실행됩니다.

#### Docker 사용

Docker를 사용하여 컨테이너 환경에서 서버를 실행할 수 있습니다.

```bash
# 1. Docker 이미지 빌드
docker build -t clova-x-server .

# 2. Docker 컨테이너 실행
docker run -d --name clova-x-server \
  --env-file .env \
  -p 8000:8000 \
  clova-x-server
```

## API 사용법

API 문서는 서버 실행 후 `http://127.0.0.1:8000/docs` 에서 확인할 수 있습니다.

### 1. Health Check

서버가 정상적으로 동작하는지 확인합니다.

**Request**

```bash
curl -X GET "http://127.0.0.1:8000/api/v1/health/"
```

**Response**

```json
{
  "status": "ok"
}
```

### 2. Simple Chat (Streaming)

간단한 단일 메시지로 채팅하며, 응답을 스트리밍으로 받습니다.

**Request**

```bash
curl.exe -N -X POST "http://localhost:8000/api/v1/chat/simple" -H "Accept: text/event-stream" -H "Content-Type: application/json" --data-raw "{\"message\":\"당근 양파 쌀밥 배추\",\"max_tokens\":256,\"temperature\":0.5,\"system_prompt\":\"너는 고급 레스토랑에서 일을하는 전문 요리사 ai assistant야. 사용자는 식재료만 입력할거야. 식재료를 가 지고 할 수 있는 간단한 요리라도 추천해줄 수 있는 유능한 요리사야. 대답할 땐, 추천할 수 있는 요리와 요리의 난이도, 조리과정을 구체적으로 설명해.\"}"
```

**Response**

응답은 `text/event-stream` 형식으로 스트리밍됩니다. 각 이벤트는 다음과 같은 JSON 구조를 가집니다.

```json
data: {"success":true,"message":"사용자님께서 제공하신 식재료로 만들 수 있는 요리는 '채소 볶음밥'입니다."}

data: {"success":true,"message":"\n\n난이도는 중간이며, 아래는 조리 과정입니다."}

data: {"success":true,"message":"\n\n1. 당근과 양파는 잘게 다지고, 배추는 적당한 크기로 썰어줍니다."}

data: {"success":true,"message":"\n2. 팬에 기름을 두르고 다진 마늘 1큰술을 넣어 향이 올라올 때까지 볶아줍니다."}

data: {"success":true,"message":"\n3. 이후 다져둔 당근, 양파를 넣고 함께 볶다가 반쯤 익으면 배추를 넣습니다."}

data: {"success":true,"message":"\n4. 채소가 모두 익으면 밥 한 공기를 넣고 같이 볶아줍니다."}

data: {"success":true,"message":"\n5. 소금과 후추로 간을 하고, 마지막으로 참기름을 뿌려주면 완성됩니다."}

data: {"success":true,"message":"\n\n간단하면서도 영양가 높은 채소 볶음밥은 아이들도 좋아하는 건강식 메뉴입니다. 취향에 따라 다른 야채나 고기를 추가하여 더욱 맛있게 즐길 수도 있습니다. 즐거운 식사 되세요!"}
```

