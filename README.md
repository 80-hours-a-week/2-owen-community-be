# Owen Community API

AWS AI School 2기 3주차 과제 - FastAPI 기반 커뮤니티 백엔드 API

## 개요

FastAPI를 사용하여 Route와 Controller 패턴으로 구현한 RESTful API 서버입니다.

## 기술 스택

- Python 3.11
- FastAPI 0.128.0
- Uvicorn 0.40.0
- Pydantic 2.12.5

## 설치 및 실행

### 1. 가상환경 생성
```bash
conda create -n community python=3.11 -y
conda activate community
```

### 2. 패키지 설치
```bash
pip install -r requirements.txt
```

### 3. 서버 실행
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 4. API 문서 확인
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 프로젝트 구조

```
2-owen-community-ds/
├── app/
│   ├── main.py                    # FastAPI 앱 초기화
│   ├── models/
│   │   └── user.py                # Pydantic 데이터 모델
│   └── routes/
│       ├── response_examples.py   # JSONResponse 예제
│       ├── post_examples.py       # POST 요청 예제
│       └── user_routes.py         # 사용자 CRUD API
├── docs/                          # 학습 가이드 문서
├── postman_collections/           # Postman 테스트 컬렉션
├── pyproject.toml
├── requirements.txt
└── README.md
```

## API 엔드포인트

### JSONResponse 예제
- `GET /api/examples/custom-status` - 커스텀 상태 코드 (201)
- `GET /api/examples/custom-headers` - 커스텀 헤더 추가
- `GET /api/examples/set-cookie` - 쿠키 설정
- `GET /api/examples/delete-cookie` - 쿠키 삭제
- `GET /api/examples/combined` - 상태 코드 + 헤더 + 쿠키

### POST 요청 예제
- `POST /api/post-examples/simple` - 기본 POST 요청
- `POST /api/post-examples/echo` - 필드별 데이터 수신
- `POST /api/post-examples/with-cookie` - POST 후 쿠키 설정

### 사용자 API
- `POST /api/users` - 사용자 생성
- `GET /api/users` - 전체 사용자 조회
- `GET /api/users/{id}` - 단일 사용자 조회
- `PUT /api/users/{id}` - 사용자 정보 수정
- `DELETE /api/users/{id}` - 사용자 삭제
- `POST /api/users/login` - 로그인 (쿠키 기반)
- `POST /api/users/logout` - 로그아웃

## 테스트

### Postman 사용
1. Postman 설치: https://www.postman.com/downloads/
2. Collection 임포트: `postman_collections/Owen_Community_API_Full.postman_collection.json`
3. Base URL: `http://localhost:8000`
4. 25개 요청 테스트 실행

### Swagger UI 사용
브라우저에서 http://localhost:8000/docs 접속하여 인터랙티브 테스트

## 주요 기능

### 1. JSONResponse 커스터마이징
- HTTP 상태 코드 변경
- 커스텀 헤더 추가
- 쿠키 설정 및 삭제

### 2. 데이터 검증
- Pydantic 모델을 통한 자동 검증
- 타입 체크 및 필수 필드 검증

### 3. 쿠키 기반 인증
- httponly, samesite 옵션 적용
- 로그인/로그아웃 구현

## 문서

상세한 학습 가이드는 `docs/` 폴더 참조:
- `POSTMAN_GUIDE.md` - Postman 설치 및 사용법
- `JSONRESPONSE_GUIDE.md` - JSONResponse 활용법
- `POST_REQUEST_GUIDE.md` - POST 요청 처리

## 주의사항

- 인메모리 저장소 사용 (서버 재시작 시 데이터 초기화)
- 비밀번호 해시화 미구현 (학습용)
- HTTPS 미적용 (로컬 개발 환경)

## 라이선스

AWS AI School 2기 교육 과정
