# Owen Community Backend

FastAPI 기반의 커뮤니티 백엔드 API입니다. Router-Controller-Model 구조를 적용하여 프로젝트를 구성합니다.

## 기능

- 게시글 CRUD (Create, Read, Update, Delete)
- 사용자 및 댓글 데이터 구조 준비 (Model 계층 완성)
- 전역 예외 처리 및 표준화된 API 응답
- 인메모리 저장소 기반 데이터 관리
- 수동 데이터 검증 (학습 목적)
- CORS 설정

## 기술 스택

- Framework: FastAPI
- Server: Uvicorn
- Validation: 수동 검증 (학습 목적)
- Storage: In-memory

## 프로젝트 구조

```
2-owen-community-be/
 main.py               # 앱 초기화 및 전역 설정
 config.py             # 환경 설정 관리
 routers/              # API 경로 및 엔드포인트 정의
 controllers/          # 비즈니스 로직 및 데이터 처리
 models/               # 데이터 관리 Model (User, Board, Comment)
 utils/                # 공통 유틸리티 (응답 포맷, 예외 정의)
 .env.example          # 환경 변수 템플릿
 requirements.txt      # 의존성 패키지 리스트
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

## Phase 3: Model 계층 추가 완료

### 완료된 작업

**Model 계층 구현:**
- `models/user_model.py`: UserModel 클래스 (사용자 CRUD 메서드)
- `models/board_model.py`: BoardModel 클래스 (게시글 CRUD 메서드)
- `models/comment_model.py`: CommentModel 클래스 (댓글 CRUD 메서드)

**Controller 리팩토링:**
- 게시글 Controller에서 직접 데이터 조작을 Model로 분리
- `post_id`를 UUID string으로 통일
- 수동 데이터 검증 적용

**아키텍처 개선:**
- Route-Controller-Model 구조 완성
- 관심사 분리 (HTTP ↔ 비즈니스 로직 ↔ 데이터 관리)
- 코드 재사용성 및 유지보수성 향상

### 구조적 이점

- **관심사 분리**: 각 계층이 명확한 책임 수행
- **유지보수성**: 한 계층 수정이 다른 계층에 미치는 영향 최소화
- **테스트 용이성**: 각 계층 독립적 테스트 가능
- **확장성**: 데이터베이스 전환 시 Model 계층만 수정

## 다음 단계

- Phase 4: 기본 인증 API 구현 (로그인/회원가입)
- Phase 5: 댓글 CRUD API 구현
- Phase 7: 쿠키 기반 세션 관리

## 주의사항

- 서버 실행 시 --reload 옵션 권장
- 모든 API 엔드포인트는 /v1 접두사 사용
- 현재 인메모리 저장소 사용으로 서버 재시작 시 데이터 초기화
