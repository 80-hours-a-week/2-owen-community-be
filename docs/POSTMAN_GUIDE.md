# Postman 설치 및 사용 가이드

## 📥 Postman 설치

### 방법 1: 공식 웹사이트에서 다운로드 (권장)

1. **Postman 공식 웹사이트 접속**
   - URL: https://www.postman.com/downloads/

2. **운영체제에 맞는 버전 다운로드**
   - Windows 64-bit 버전 선택
   - 다운로드 후 설치 파일 실행

3. **설치 진행**
   - 설치 마법사를 따라 진행
   - 기본 설정으로 설치 (약 2-3분 소요)

4. **Postman 실행**
   - 설치 완료 후 자동으로 실행
   - 계정 생성/로그인 (선택사항, 스킵 가능)

### 방법 2: Winget으로 설치 (Windows 11)

```powershell
winget install Postman.Postman
```

### 방법 3: Chocolatey로 설치

```powershell
choco install postman
```

---

## 🚀 FastAPI 서버 정보

### 서버 주소
- **Base URL**: `http://localhost:8000`
- **Swagger 문서**: http://localhost:8000/docs
- **ReDoc 문서**: http://localhost:8000/redoc

### 서버 상태 확인
서버가 실행 중이면 다음과 같은 메시지가 표시됩니다:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [xxxxx] using WatchFiles
```

---

## 🧪 Postman으로 GET 요청 테스트

### 테스트 1: 루트 엔드포인트

1. **Postman 실행**

2. **새 요청 생성**
   - 왼쪽 상단 "New" 버튼 클릭 → "HTTP Request" 선택
   - 또는 단축키: `Ctrl + N`

3. **요청 설정**
   - **Method**: `GET` (기본값)
   - **URL**: `http://localhost:8000/`

4. **Send 버튼 클릭**

5. **예상 응답**
```json
{
    "message": "Owen Community API에 오신 것을 환영합니다!",
    "status": "running",
    "timestamp": "2026-01-06T15:48:00.123456"
}
```

---

### 테스트 2: 헬스체크 엔드포인트

**URL**: `http://localhost:8000/health`

**예상 응답**:
```json
{
    "status": "healthy",
    "service": "owen-community-backend",
    "timestamp": "2026-01-06T15:48:00.123456"
}
```

---

### 테스트 3: API 정보 조회

**URL**: `http://localhost:8000/api/info`

**예상 응답**:
```json
{
    "name": "Owen Community API",
    "version": "0.1.0",
    "endpoints": {
        "users": "/api/users",
        "posts": "/api/posts",
        "comments": "/api/comments"
    },
    "documentation": {
        "swagger": "/docs",
        "redoc": "/redoc"
    }
}
```

---

### 테스트 4: 테스트 엔드포인트

**URL**: `http://localhost:8000/api/test`

**예상 응답**:
```json
{
    "success": true,
    "message": "GET 요청이 성공적으로 처리되었습니다!",
    "data": {
        "test": "Hello from FastAPI",
        "method": "GET",
        "timestamp": "2026-01-06T15:48:00.123456"
    }
}
```

---

### 테스트 5: 경로 파라미터 사용

**URL**: `http://localhost:8000/api/greet/Owen`

**설명**: URL의 마지막 부분에 이름을 입력하면 해당 이름으로 인사합니다.

**예상 응답**:
```json
{
    "success": true,
    "message": "안녕하세요, Owen님!",
    "timestamp": "2026-01-06T15:48:00.123456"
}
```

**다른 이름으로 시도**:
- `http://localhost:8000/api/greet/철수`
- `http://localhost:8000/api/greet/영희`

---

### 테스트 6: 쿼리 파라미터 사용

**URL**: `http://localhost:8000/api/search?q=fastapi&limit=5`

**설명**: 
- `q`: 검색어
- `limit`: 결과 개수 제한

**예상 응답**:
```json
{
    "success": true,
    "query": "fastapi",
    "limit": 5,
    "message": "'fastapi' 검색 결과",
    "results": []
}
```

**쿼리 파라미터 변경 방법**:
1. Postman의 "Params" 탭 클릭
2. Key-Value 쌍으로 파라미터 입력:
   - Key: `q`, Value: `fastapi`
   - Key: `limit`, Value: `5`

---

## 📸 Postman 사용 화면 설명

### 1. 요청 영역 (상단)
```
GET  http://localhost:8000/api/test  [Params] [Headers] [Body]  [Send]
```

### 2. 응답 영역 (하단)
- **Status**: `200 OK` (성공)
- **Time**: 응답 시간 (ms)
- **Size**: 응답 크기
- **Body**: JSON 응답 데이터 (Pretty, Raw, Preview)

---

## 💡 Postman 주요 기능

### 1. Collection 생성
요청들을 그룹화하여 관리:
1. 좌측 "Collections" 탭
2. "+" 버튼 클릭
3. Collection 이름: "Owen Community API"

### 2. 요청 저장
1. 요청 설정 후 "Save" 버튼
2. Collection 선택
3. 요청 이름 입력 (예: "Get Root")

### 3. Environment 설정
변수를 사용하여 Base URL 관리:
1. 우측 상단 톱니바퀴 아이콘
2. "Add" → Environment 이름: "Local"
3. Variable 추가:
   - Variable: `base_url`
   - Initial Value: `http://localhost:8000`
4. 요청 URL에서 사용: `{{base_url}}/api/test`

---

## 🔍 응답 코드 이해

| Status Code | 의미 | 설명 |
|------------|------|------|
| 200 OK | 성공 | 요청이 성공적으로 처리됨 |
| 404 Not Found | 찾을 수 없음 | 잘못된 경로 |
| 500 Internal Server Error | 서버 오류 | 서버 내부 오류 |

---

## 🛠️ 문제 해결

### 1. "Could not get response" 오류
**원인**: 서버가 실행되지 않음

**해결**:
```bash
# 서버 실행 확인
conda activate community
cd Assignment/Week3/2-owen-community-ds
python -m uvicorn app.main:app --reload
```

### 2. Connection Refused 오류
**원인**: 포트가 사용 중이거나 방화벽 차단

**해결**:
- 서버가 http://0.0.0.0:8000 에서 실행 중인지 확인
- Windows 방화벽에서 Python 허용 확인

### 3. 404 Not Found
**원인**: 잘못된 URL 경로

**해결**:
- URL 철자 확인
- `/docs` 에서 사용 가능한 엔드포인트 확인

---

## 📋 테스트 체크리스트

완료한 항목에 체크하세요:

- [ ] Postman 설치 완료
- [ ] FastAPI 서버 실행 확인
- [ ] 루트 엔드포인트 (`/`) 테스트
- [ ] 헬스체크 (`/health`) 테스트
- [ ] API 정보 (`/api/info`) 테스트
- [ ] 테스트 엔드포인트 (`/api/test`) 테스트
- [ ] 경로 파라미터 (`/api/greet/{name}`) 테스트
- [ ] 쿼리 파라미터 (`/api/search?q=...`) 테스트
- [ ] Swagger 문서 (`/docs`) 확인
- [ ] Collection 생성 및 요청 저장

---

## 🎯 다음 단계

1. **POST 요청 테스트**: 데이터 생성 API 구현
2. **PUT 요청 테스트**: 데이터 수정 API 구현
3. **DELETE 요청 테스트**: 데이터 삭제 API 구현
4. **Request Body 사용**: JSON 데이터 전송
5. **Collection 내보내기**: 팀원과 공유

---

## 📚 참고 자료

- [Postman 공식 문서](https://learning.postman.com/)
- [FastAPI 공식 문서](https://fastapi.tiangolo.com/)
- [HTTP 메서드 설명](https://developer.mozilla.org/ko/docs/Web/HTTP/Methods)

