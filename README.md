# Owen Community Backend

FastAPI 기반의 커뮤니티 백엔드 API입니다. Router-Controller-Model 구조를 적용하여 프로젝트를 구성합니다.

## 기능

- 게시글 CRUD (Create, Read, Update, Delete)
- 댓글 CRUD (Create, Read, Update, Delete)
- 전역 예외 처리 및 표준화된 API 응답
- 인메모리 저장소 기반 데이터 관리
- Router-Controller-Model 아키텍처
- CORS 설정

## 기술 스택

- Framework: FastAPI
- Server: Uvicorn
- Validation: Pydantic 자동 검증 (UUID 타입 지원)
- Storage: In-memory

## 프로젝트 구조

```
2-owen-community-be/
├── main.py               # 앱 초기화 및 전역 설정
├── config.py             # 환경 설정 관리
├── routers/              # API 경로 및 엔드포인트 정의
│   ├── post_router.py    # 게시글 API
│   └── comment_router.py # 댓글 API
├── controllers/          # 비즈니스 로직 및 데이터 처리
│   ├── post_controller.py
│   └── comment_controller.py
├── models/               # 데이터 관리 (User, Post, Comment)
│   ├── user_model.py
│   ├── post_model.py
│   └── comment_model.py
└── utils/                # 공통 유틸리티 (응답 포맷, 예외 정의)
    ├── exceptions.py
    └── response.py
```

## 설치 및 실행

1. 의존성 설치
   ```bash
   pip install -r requirements.txt
   ```

2. 서버 실행
   ```bash
   uvicorn main:app --reload
   ```

## 주요 API 엔드포인트

### 공통
- GET /health: 서버 상태 확인

### 게시글 (Post)
- GET /v1/posts: 게시글 목록 조회
- GET /v1/posts/{post_id}: 게시글 상세 조회
- POST /v1/posts: 게시글 생성
- PATCH /v1/posts/{post_id}: 게시글 수정
- DELETE /v1/posts/{post_id}: 게시글 삭제

### 댓글 (Comment)
- GET /v1/posts/{post_id}/comments: 댓글 목록 조회
- POST /v1/posts/{post_id}/comments: 댓글 작성
- PATCH /v1/posts/{post_id}/comments/{comment_id}: 댓글 수정
- DELETE /v1/posts/{post_id}/comments/{comment_id}: 댓글 삭제

## API 응답 포맷

### 성공 응답
```json
{
  "status": "success",
  "code": "GET_POSTS_SUCCESS",
  "data": [],
  "status_code": 200
}
```

### 에러 응답
```json
{
  "status": "error",
  "code": "NOT_FOUND",
  "details": { "resource": "게시글" },
  "status_code": 404
}
```

## 구현 완료

- Router-Controller-Model 아키텍처 완성
- 게시글 및 댓글 CRUD API 구현
- 인메모리 데이터 저장소 (User, Post, Comment)
- 표준화된 API 응답 및 에러 처리
- UUID 타입 기반 Path Parameter 자동 검증
- 데이터 무결성 확보 (falsy 값 처리)

## 다음 단계

- 게시글/댓글 API에 실제 사용자 인증 통합
- 파일 업로드 기능 구현
- 게시글 좋아요 기능 구현

## 주의사항

- 서버 실행 시 --reload 옵션 권장
- 모든 API 엔드포인트는 /v1 접두사 사용
- Path Parameter는 UUID 형식을 사용하며 자동 검증됨
- 현재 인메모리 저장소 사용으로 서버 재시작 시 데이터 초기화
