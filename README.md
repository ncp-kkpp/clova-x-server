# clova-x-server

`clova-x-server`는 네이버 클라우드 플랫폼(NCP)의 CLOVA Studio / HyperCLOVA X 같은 모델들을 활용하는 서버 백엔드 프로젝트이다.  
Python 기반으로 구성되어 있으며, Docker 도커라이징 및 스크립트 관리가 포함되어 있다.

## 프로젝트 구조

clova-x-server/  
├── app/   
├── scripts/  
├── Dockerfile  
├── requirements.txt  
├── .gitignore  
└── README.md

- app/  
  서버 동작을 위한 주요 코드들이 위치. 예: API, 라우팅, 모델 호출, 입력/출력 처리 등.
- scripts/  
  데이터 처리, 마이그레이션, 테스팅 보조 스크립트 등 개발·운영 지원용 코드.
- Dockerfile  
  컨테이너 이미지 빌드를 위한 설정 파일.
- requirements.txt  
  Python 의존성 패키지 목록.
- .gitignore  
  Git에 포함하지 않을 파일/디렉토리 설정.

## 설치 및 실행 방법

아래는 개발 환경에서 테스트 또는 실제 서비스를 구동할 때 기본적인 절차이다.

### 직접 실행

1. 저장소 클론  
   ```bash
   git clone https://github.com/ncp-kkpp/clova-x-server.git
   cd clova-x-server
   ```

2. Python 가상환경 생성 및 활성화  
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. 의존성 설치  
   ```bash
   pip install -r requirements.txt
   ```

4. 환경 변수 설정  
   필요한 API 키, 설정값 등을 환경 변수 또는 설정 파일로 준비해야 함.

5. 서버 실행  
   ```bash
   # 예: uvicorn 또는 flask run 등의 커맨드
   python -m app.main
   ```

### 도커 실행

1. Docker로 실행 (선택사항)  
   ```bash
   # 도커 이미지 빌드
   docker build -t clova-x-server .

   # 도커 컨테이너 실행
   docker run -d --name clova-x-server -e API_KEY=<your_key> -p 8000:8000 clova-x-server
   ```

## 환경 설정

### 운영 환경

| 변수 이름 | 설명 | 예시 |
|---|---|---|
| `CLOVA_API_KEY` | CLOVA Studio API 인증 키 | `"abcdef123456..."` |
| 기타 키 / 엔드포인트 | 모델 이름, 베이스 URL, 타임아웃 등 | `"https://clovastudio.stream.ntruss.com/v1/openai"` |

(필요한 모든 환경 변수 목록은 코드 내 문서 또는 설정 파일 참조)

### 개발 환경
> .env 환경 설정 파일
```properties
CLOVA_API_KEY=your_api_key_here
HYPERCLOVA_PRIMARY_KEY=your_primary_key_here
HYPERCLOVA_REQUEST_ID=your_request_id_here
```

## 사용 방법

- 클라이언트 → 서버 요청 형식  
- 서버가 CLOVA API 또는 HyperCLOVA X 모델 호출하는 방식  
- 입력/출력 예시  

```json
POST /api/chat
{
  "messages": [
    { "role": "system", "content": "..." },
    { "role": "user", "content": "..." }
  ]
}
```

응답 예:

```json
{
  "reply": "..."
}
```

- 기타 기능: 스크립트를 통한 배치 처리, 로그 관리 등.
