# Owen Community Backend

FastAPI 기반의 커뮤니티 백엔드 API입니다. Router-Controller-Model 구조를 적용하여 프로젝트를 구성하며, 세션 기반 인증 시스템을 포함합니다.

## 주요 기능

- **인증 및 세션 관리**: 회원가입, 로그인/로그아웃, 세션 기반 인증 (Cookie)
- **게시글 CRUD**: 게시글 작성, 목록 조회, 상세 조회, 수정, 삭제 (작성자 권한 검증)
- **댓글 CRUD**: 댓글 작성, 목록 조회, 수정, 삭제 (작성자 권한 검증)
- **표준화된 API 응답**: 전역 예외 처리 및 일관된 JSON 응답 포맷
- **데이터 관리**: 인메모리 저장소 기반 데이터 영속화 시뮬레이션

## 기술 스택

- **Framework**: FastAPI (v0.128.0+)
- **Session**: Starlette SessionMiddleware (Cookie-based)
- **Validation**: Pydantic v2
- **Storage**: In-memory (User, Post, Comment)

## 프로젝트 구조

```
2-owen-community-be/
├── main.py               # 앱 초기화, 미들웨어 및 라우터 등록
├── config.py             # 환경 설정 (쿠키, 세션 등)
├── routers/              # API 엔드포인트 정의
│   ├── auth_router.py    # 인증 API
│   ├── post_router.py    # 게시글 API
│   └── comment_router.py # 댓글 API
├── controllers/          # 비즈니스 로직 처리
│   ├── auth_controller.py
│   ├── post_controller.py
│   └── comment_controller.py
├── models/               # 데이터 접근 및 관리
│   ├── user_model.py
│   ├── post_model.py
│   └── comment_model.py
└── utils/                # 공통 유틸리티
    ├── exceptions.py     # 커스텀 예외
    ├── response.py       # 표준 응답 포맷
    └── error_codes.py    # 에러/성공 코드 정의
```

## 설치 및 실행

1. **가상환경 활성화 (Conda 권장)**
   ```bash
   conda activate community
   ```

2. **의존성 설치**
   ```bash
   pip install -r requirements.txt
   ```

3. **서버 실행**
   ```bash
   uvicorn main:app --reload
   ```

## 주요 API 엔드포인트

### 인증 (Auth)
- `POST /api/auth/signup`: 회원가입
- `POST /api/auth/login`: 로그인 (세션 쿠키 발급)
- `POST /api/auth/logout`: 로그아웃 (세션 만료)
- `GET /api/auth/me`: 현재 로그인한 사용자 정보 조회

### 게시글 (Post)
- `GET /v1/posts`: 목록 조회
- `GET /v1/posts/{post_id}`: 상세 조회
- `POST /v1/posts`: 작성 (인증 필요)
- `PATCH /v1/posts/{post_id}`: 수정 (작성자 권한)
- `DELETE /v1/posts/{post_id}`: 삭제 (작성자 권한)

### 댓글 (Comment)
- `GET /v1/posts/{post_id}/comments`: 목록 조회
- `POST /v1/posts/{post_id}/comments`: 작성 (인증 필요)
- `PATCH /v1/posts/{post_id}/comments/{comment_id}`: 수정 (작성자 권한)
- `DELETE /v1/posts/{post_id}/comments/{comment_id}`: 삭제 (작성자 권한)

## 주의사항

- **보안**: 현재 로컬 개발용으로 `https_only=False` 설정이 되어 있습니다. 배포 시에는 `True`로 변경해야 합니다.
- **데이터 휘발성**: 인메모리 저장소를 사용하므로 서버 재시작 시 모든 데이터가 초기화됩니다.
- **비밀번호**: 현재 단순 비교 방식을 사용 중이며, 추후 암호화 해싱 로직 도입이 필요합니다.
