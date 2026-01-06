# JSONResponse 학습 가이드

## 📚 JSONResponse란?

FastAPI의 `JSONResponse`는 HTTP 응답을 세밀하게 제어할 수 있는 클래스입니다.

### 주요 기능
1. **커스텀 상태 코드** 설정
2. **커스텀 헤더** 추가
3. **쿠키** 설정 및 삭제
4. **응답 내용** 완전 제어

---

## 🎯 1. 커스텀 상태 코드 (Status Code)

### HTTP 상태 코드란?
서버가 클라이언트의 요청을 어떻게 처리했는지 알려주는 3자리 숫자입니다.

### 주요 상태 코드

| 코드 | 이름 | 의미 | 사용 시기 |
|------|------|------|-----------|
| 200 | OK | 성공 | 일반적인 성공 응답 |
| 201 | Created | 생성됨 | 새 리소스 생성 성공 |
| 202 | Accepted | 수락됨 | 요청은 받았지만 처리 중 |
| 204 | No Content | 내용 없음 | 성공했지만 반환할 내용 없음 |
| 400 | Bad Request | 잘못된 요청 | 요청 데이터가 잘못됨 |
| 401 | Unauthorized | 인증 필요 | 로그인이 필요함 |
| 403 | Forbidden | 금지됨 | 권한이 없음 |
| 404 | Not Found | 찾을 수 없음 | 리소스가 존재하지 않음 |
| 500 | Internal Server Error | 서버 오류 | 서버 내부 오류 |

### 예제 코드

```python
from fastapi.responses import JSONResponse

@app.get("/custom-status")
async def custom_status():
    return JSONResponse(
        status_code=201,
        content={"message": "리소스가 생성되었습니다!"}
    )
```

### Postman 테스트
**URL**: `GET http://localhost:8000/api/examples/custom-status`

**예상 응답**: Status `201 Created`

---

## 🏷️ 2. 커스텀 헤더 (Custom Headers)

### HTTP 헤더란?
클라이언트와 서버 간 추가 정보를 전달하는 메타데이터입니다.

### 사용 예시
- API 버전 정보
- 요청 추적 ID
- 캐싱 정책
- CORS 설정
- 커스텀 메타데이터

### 예제 코드

```python
@app.get("/custom-headers")
async def custom_headers():
    content = {"message": "커스텀 헤더가 포함되었습니다"}
    
    headers = {
        "X-Custom-Header": "My Value",
        "X-API-Version": "1.0.0",
        "X-Request-ID": "req-12345"
    }
    
    return JSONResponse(
        content=content,
        headers=headers
    )
```

### Postman에서 확인하기
1. **URL**: `GET http://localhost:8000/api/examples/custom-headers`
2. **Send** 클릭
3. 응답 하단의 **Headers** 탭 클릭
4. `X-Custom-Header`, `X-API-Version` 등 확인

**팁**: 커스텀 헤더는 보통 `X-`로 시작합니다.

---

## 🍪 3. 쿠키 (Cookie) 설정

### 쿠키란?
서버가 클라이언트(브라우저)에 저장하는 작은 데이터 조각입니다.

### 사용 목적
- 사용자 인증 (로그인 상태 유지)
- 세션 관리
- 사용자 설정 저장
- 추적 및 분석

### 쿠키 속성

| 속성 | 설명 | 예제 |
|------|------|------|
| `key` | 쿠키 이름 | "auth_token" |
| `value` | 쿠키 값 | "abc123xyz" |
| `max_age` | 유효 시간 (초) | 3600 (1시간) |
| `expires` | 만료 날짜/시간 | datetime 객체 |
| `httponly` | JavaScript 접근 차단 | True (보안) |
| `secure` | HTTPS에서만 전송 | True (프로덕션) |
| `samesite` | CSRF 방지 | "lax", "strict" |

### 예제 코드

```python
from fastapi.responses import JSONResponse

@app.get("/set-cookie")
async def set_cookie():
    content = {"message": "쿠키가 설정되었습니다!"}
    
    response = JSONResponse(content=content)
    
    # 쿠키 설정
    response.set_cookie(
        key="user_token",
        value="token-abc123",
        max_age=3600,      # 1시간
        httponly=True,     # XSS 공격 방지
        samesite="lax"     # CSRF 공격 방지
    )
    
    return response
```

### 보안 쿠키 설정

```python
from datetime import datetime, timedelta

@app.get("/set-secure-cookie")
async def set_secure_cookie():
    content = {"message": "보안 쿠키 설정"}
    response = JSONResponse(content=content)
    
    expires = datetime.now() + timedelta(days=7)
    
    response.set_cookie(
        key="auth_token",
        value="secure-token-xyz",
        expires=expires,
        httponly=True,    # JavaScript 접근 불가
        secure=True,      # HTTPS만 (프로덕션)
        samesite="strict" # 같은 사이트만
    )
    
    return response
```

### 쿠키 삭제

```python
@app.get("/delete-cookie")
async def delete_cookie():
    response = JSONResponse(content={"message": "쿠키 삭제됨"})
    response.delete_cookie(key="user_token")
    return response
```

### Postman에서 쿠키 확인

1. **URL**: `GET http://localhost:8000/api/examples/set-cookie`
2. **Send** 클릭
3. 응답 하단의 **Cookies** 탭 클릭
4. 설정된 쿠키 확인 (localhost 도메인)

**브라우저에서 테스트**:
- 브라우저에서 URL 접속
- F12 → Application 탭 → Cookies → localhost:8000
- 저장된 쿠키 확인

---

## 🔄 4. 모든 기능 결합 예제

```python
@app.get("/combined")
async def combined():
    content = {
        "success": True,
        "message": "상태 코드 + 헤더 + 쿠키 모두 포함!",
        "data": {"id": 1, "name": "테스트"}
    }
    
    # 커스텀 헤더
    headers = {
        "X-Custom-Header": "Combined",
        "X-Request-ID": "req-001"
    }
    
    # 상태 코드 201 + 헤더
    response = JSONResponse(
        status_code=201,
        content=content,
        headers=headers
    )
    
    # 쿠키 추가
    response.set_cookie(
        key="session_id",
        value="session-123",
        max_age=3600
    )
    
    return response
```

---

## 📝 Postman 테스트 예제

### 테스트 1: 커스텀 상태 코드
```
Method: GET
URL: http://localhost:8000/api/examples/custom-status
Expected: Status 201 Created
```

### 테스트 2: 202 Accepted
```
Method: GET
URL: http://localhost:8000/api/examples/custom-status/accepted
Expected: Status 202 Accepted
Body: {"status": "processing", "job_id": "..."}
```

### 테스트 3: 204 No Content
```
Method: GET
URL: http://localhost:8000/api/examples/custom-status/no-content
Expected: Status 204 (응답 Body 없음)
```

### 테스트 4: 커스텀 헤더
```
Method: GET
URL: http://localhost:8000/api/examples/custom-headers
Check: Response Headers 탭
- X-Custom-Header: Owen Community API
- X-Request-ID: req-...
- X-API-Version: 1.0.0
```

### 테스트 5: 쿠키 설정
```
Method: GET
URL: http://localhost:8000/api/examples/set-cookie
Check: Cookies 탭
- user_token (1시간 유효)
- session_id (2시간 유효)
- preferences (24시간 유효)
```

### 테스트 6: 보안 쿠키
```
Method: GET
URL: http://localhost:8000/api/examples/set-cookie/secure
Check: Cookies 탭
- auth_token (7일 유효, httponly, samesite=strict)
```

### 테스트 7: 쿠키 삭제
```
Method: GET
URL: http://localhost:8000/api/examples/delete-cookie
Result: 이전에 설정된 쿠키가 삭제됨
```

### 테스트 8: 모든 기능 결합
```
Method: GET
URL: http://localhost:8000/api/examples/combined
Check:
- Status: 201 Created
- Headers: X-Custom-Header, X-Request-ID
- Cookies: combined_token
```

### 테스트 9: 404 에러
```
Method: GET
URL: http://localhost:8000/api/examples/error-example/404
Expected: Status 404 Not Found
Body: {"success": false, "error": "Not Found"}
```

### 테스트 10: 403 에러
```
Method: GET
URL: http://localhost:8000/api/examples/error-example/403
Expected: Status 403 Forbidden
Body: {"success": false, "error": "Forbidden"}
```

---

## 💡 실전 활용 예제

### 1. 사용자 로그인 (쿠키 사용)

```python
@app.post("/login")
async def login(email: str, password: str):
    # 인증 로직
    if valid_user:
        response = JSONResponse(
            content={"success": True, "message": "로그인 성공"}
        )
        response.set_cookie(
            key="auth_token",
            value="generated-token",
            max_age=86400,  # 24시간
            httponly=True
        )
        return response
```

### 2. API 버전 관리 (헤더 사용)

```python
@app.get("/api/users")
async def get_users():
    headers = {
        "X-API-Version": "2.0.0",
        "X-Deprecated": "false"
    }
    return JSONResponse(
        content={"users": [...]},
        headers=headers
    )
```

### 3. 비동기 작업 수락 (202 상태 코드)

```python
@app.post("/api/process")
async def process_data(data: dict):
    # 백그라운드 작업 시작
    job_id = start_background_job(data)
    
    return JSONResponse(
        status_code=202,
        content={
            "message": "작업이 시작되었습니다",
            "job_id": job_id,
            "status_url": f"/api/jobs/{job_id}"
        }
    )
```

---

## 🔍 디버깅 팁

### Postman에서 확인할 사항

1. **Status 탭**: 상태 코드 확인
2. **Body 탭**: 응답 내용 (Pretty/Raw/Preview)
3. **Headers 탭**: 응답 헤더 확인
4. **Cookies 탭**: 설정된 쿠키 확인
5. **Time**: 응답 시간

### 브라우저 개발자 도구

1. F12 → Network 탭
2. 요청 클릭
3. Headers, Response, Cookies 확인

---

## 📚 참고 자료

- [FastAPI JSONResponse 문서](https://fastapi.tiangolo.com/advanced/custom-response/)
- [HTTP 상태 코드](https://developer.mozilla.org/ko/docs/Web/HTTP/Status)
- [HTTP 헤더](https://developer.mozilla.org/ko/docs/Web/HTTP/Headers)
- [HTTP 쿠키](https://developer.mozilla.org/ko/docs/Web/HTTP/Cookies)

---

## ✅ 학습 체크리스트

- [ ] JSONResponse 기본 사용법 이해
- [ ] 커스텀 상태 코드 설정 (200, 201, 202, 204, 404, 403)
- [ ] 커스텀 헤더 추가 (`X-` 접두사)
- [ ] 쿠키 설정 (`set_cookie`)
- [ ] 쿠키 보안 옵션 이해 (httponly, secure, samesite)
- [ ] 쿠키 삭제 (`delete_cookie`)
- [ ] 모든 기능을 결합한 응답 생성
- [ ] Postman으로 각 기능 테스트
- [ ] 브라우저 개발자 도구로 확인

모든 예제를 Postman에서 직접 테스트해보세요! 🚀

