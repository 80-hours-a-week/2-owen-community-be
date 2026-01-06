# POST 요청 테스트 가이드

## 📬 POST 요청이란?

POST는 서버에 데이터를 **생성하거나 전송**할 때 사용하는 HTTP 메서드입니다.

### GET vs POST 비교

| 특징 | GET | POST |
|------|-----|------|
| 목적 | 데이터 조회 | 데이터 생성/전송 |
| 데이터 위치 | URL (쿼리 파라미터) | Request Body |
| 데이터 크기 | 제한적 (URL 길이) | 제한 없음 |
| 캐싱 | 가능 | 불가능 |
| 보안 | URL에 노출 | Body에 숨김 |
| 예시 | 검색, 조회 | 회원가입, 로그인, 글 작성 |

---

## 🎯 Postman에서 POST 요청 보내기

### 1단계: 기본 POST 요청

#### 1-1. 새 요청 생성
1. Postman에서 **New** → **HTTP Request**
2. Method를 **GET**에서 **POST**로 변경
3. URL 입력: `http://localhost:8000/api/post-examples/simple`

#### 1-2. Request Body 설정
1. URL 아래 **Body** 탭 클릭
2. **raw** 선택
3. 오른쪽 드롭다운에서 **JSON** 선택
4. Body에 JSON 데이터 입력:

```json
{
    "name": "홍길동",
    "age": 30,
    "city": "서울"
}
```

#### 1-3. 요청 전송
1. **Send** 버튼 클릭
2. 응답 확인 (Status: 201 Created)

**예상 응답**:
```json
{
    "success": true,
    "message": "POST 요청을 받았습니다!",
    "received_data": {
        "name": "홍길동",
        "age": 30,
        "city": "서울"
    },
    "timestamp": "2026-01-06T..."
}
```

---

## 📋 POST 요청 예제 모음

### 예제 1: 간단한 POST (Echo)

**URL**: `POST http://localhost:8000/api/post-examples/echo`

**Body** (JSON):
```json
{
    "name": "김철수",
    "age": 25,
    "email": "chulsoo@example.com"
}
```

**예상 응답** (200 OK):
```json
{
    "success": true,
    "message": "데이터를 받았습니다!",
    "received": {
        "name": "김철수",
        "age": 25,
        "email": "chulsoo@example.com"
    },
    "timestamp": "..."
}
```

---

### 예제 2: 폼 데이터 전송

**URL**: `POST http://localhost:8000/api/post-examples/form-data`

**Body** (JSON):
```json
{
    "username": "user123",
    "password": "secret",
    "remember": true
}
```

**예상 응답** (201 Created):
```json
{
    "success": true,
    "message": "폼 데이터가 처리되었습니다.",
    "form_data": {
        "username": "user123",
        "password": "secret",
        "remember": true
    },
    "data_type": "dict"
}
```

**확인사항**: Response Headers에서 `X-Form-Processed: true` 확인

---

### 예제 3: POST 후 쿠키 설정

**URL**: `POST http://localhost:8000/api/post-examples/with-cookie`

**Body** (JSON):
```json
{
    "user": "owen",
    "action": "login"
}
```

**예상 응답** (201 Created):
```json
{
    "success": true,
    "message": "데이터를 저장하고 쿠키를 설정했습니다!",
    "saved_data": {
        "user": "owen",
        "action": "login"
    },
    "timestamp": "..."
}
```

**확인사항**: 
- Response Cookies 탭에서 `last_post_time`, `post_count` 쿠키 확인

---

### 예제 4: 중첩된 JSON 데이터

**URL**: `POST http://localhost:8000/api/post-examples/nested-data`

**Body** (JSON):
```json
{
    "user": {
        "name": "이영희",
        "email": "younghee@example.com",
        "profile": {
            "age": 28,
            "city": "부산"
        }
    },
    "preferences": {
        "theme": "dark",
        "language": "ko"
    }
}
```

**예상 응답** (201 Created):
```json
{
    "success": true,
    "message": "중첩된 데이터를 처리했습니다.",
    "received_data": { /* 전송한 데이터 */ },
    "data_structure": {
        "keys": ["user", "preferences"],
        "total_fields": 2
    }
}
```

**확인사항**: Headers에서 `X-Data-Type: nested` 확인

---

## 👤 사용자 API 테스트

### 1. 사용자 생성 (회원가입)

**URL**: `POST http://localhost:8000/api/users`

**Body** (JSON):
```json
{
    "username": "hong_gildong",
    "email": "hong@example.com",
    "password": "secure123"
}
```

**예상 응답** (201 Created):
```json
{
    "success": true,
    "message": "사용자가 성공적으로 생성되었습니다.",
    "data": {
        "id": 1,
        "username": "hong_gildong",
        "email": "hong@example.com",
        "created_at": "2026-01-06T..."
    }
}
```

**확인사항**:
- Status: 201 Created
- Headers: `X-User-ID: 1`, `X-Created-At: ...`
- 비밀번호는 응답에 포함되지 않음 (보안)

---

### 2. 중복 이메일로 생성 시도

**URL**: `POST http://localhost:8000/api/users`

**Body** (같은 이메일):
```json
{
    "username": "another_user",
    "email": "hong@example.com",
    "password": "pass456"
}
```

**예상 응답** (400 Bad Request):
```json
{
    "detail": "이미 존재하는 이메일입니다."
}
```

---

### 3. 여러 사용자 생성

**사용자 2**:
```json
{
    "username": "kim_chulsoo",
    "email": "kim@example.com",
    "password": "pass789"
}
```

**사용자 3**:
```json
{
    "username": "lee_younghee",
    "email": "lee@example.com",
    "password": "mypass"
}
```

---

### 4. 모든 사용자 조회

**URL**: `GET http://localhost:8000/api/users`

**예상 응답**:
```json
{
    "success": true,
    "count": 3,
    "data": [
        {
            "id": 1,
            "username": "hong_gildong",
            "email": "hong@example.com",
            "created_at": "..."
        },
        {
            "id": 2,
            "username": "kim_chulsoo",
            "email": "kim@example.com",
            "created_at": "..."
        },
        {
            "id": 3,
            "username": "lee_younghee",
            "email": "lee@example.com",
            "created_at": "..."
        }
    ]
}
```

---

### 5. 특정 사용자 조회

**URL**: `GET http://localhost:8000/api/users/1`

**예상 응답**:
```json
{
    "success": true,
    "data": {
        "id": 1,
        "username": "hong_gildong",
        "email": "hong@example.com",
        "created_at": "..."
    }
}
```

---

### 6. 로그인

**URL**: `POST http://localhost:8000/api/users/login`

**Body** (JSON):
```json
{
    "email": "hong@example.com",
    "password": "secure123"
}
```

**예상 응답** (200 OK):
```json
{
    "success": true,
    "message": "로그인 성공!",
    "data": {
        "user_id": 1,
        "username": "hong_gildong",
        "email": "hong@example.com"
    }
}
```

**확인사항**:
- Cookies 탭에서 `auth_token`, `user_id` 쿠키 확인
- 쿠키 유효시간: 1시간

---

### 7. 잘못된 로그인

**URL**: `POST http://localhost:8000/api/users/login`

**Body**:
```json
{
    "email": "hong@example.com",
    "password": "wrongpassword"
}
```

**예상 응답** (401 Unauthorized):
```json
{
    "success": false,
    "error": "Unauthorized",
    "message": "이메일 또는 비밀번호가 올바르지 않습니다."
}
```

---

### 8. 사용자 정보 수정

**URL**: `PUT http://localhost:8000/api/users/1`

**Body** (JSON):
```json
{
    "username": "hong_updated",
    "email": "hong_new@example.com"
}
```

**예상 응답**:
```json
{
    "success": true,
    "message": "사용자 정보가 수정되었습니다.",
    "data": {
        "id": 1,
        "username": "hong_updated",
        "email": "hong_new@example.com",
        "updated_at": "..."
    }
}
```

---

### 9. 로그아웃

**URL**: `POST http://localhost:8000/api/users/logout`

**Body**: 없음

**예상 응답**:
```json
{
    "success": true,
    "message": "로그아웃되었습니다."
}
```

**확인사항**: Cookies가 삭제됨

---

### 10. 사용자 삭제

**URL**: `DELETE http://localhost:8000/api/users/1`

**예상 응답**:
```json
{
    "success": true,
    "message": "사용자 'hong_updated'가 삭제되었습니다.",
    "deleted_user_id": 1
}
```

---

## 📊 Postman Collection 업데이트

기존 Collection에 POST 요청들을 추가하세요:

### POST Examples 폴더
1. Simple POST
2. Echo POST
3. Form Data POST
4. POST with Cookie
5. Nested Data POST

### Users API 폴더
1. Create User (POST)
2. Get All Users (GET)
3. Get User by ID (GET)
4. Login (POST)
5. Logout (POST)
6. Update User (PUT)
7. Delete User (DELETE)

---

## 🔍 Postman 고급 기능

### 1. Environment 변수 사용

Environment에 변수 추가:
```
base_url = http://localhost:8000
user_id = 1
auth_token = token-abc123
```

요청 URL에서 사용:
```
{{base_url}}/api/users/{{user_id}}
```

### 2. Tests 탭으로 자동 검증

**Tests 탭에 코드 추가**:
```javascript
// 상태 코드 확인
pm.test("Status code is 201", function () {
    pm.response.to.have.status(201);
});

// JSON 응답 확인
pm.test("Response has success field", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.success).to.eql(true);
});

// 사용자 ID를 변수로 저장
var jsonData = pm.response.json();
pm.environment.set("user_id", jsonData.data.id);
```

### 3. Pre-request Script로 동적 데이터

**Pre-request Script 탭**:
```javascript
// 랜덤 이메일 생성
var randomEmail = "user" + Math.floor(Math.random() * 10000) + "@example.com";
pm.environment.set("random_email", randomEmail);
```

**Body에서 사용**:
```json
{
    "email": "{{random_email}}"
}
```

---

## 🎯 실습 과제

### Level 1: 기본
- [ ] 간단한 POST 요청 3개 성공
- [ ] 사용자 1명 생성
- [ ] 생성한 사용자 조회

### Level 2: 중급
- [ ] 사용자 3명 생성
- [ ] 로그인/로그아웃 테스트
- [ ] 사용자 정보 수정
- [ ] 쿠키 확인

### Level 3: 고급
- [ ] 중첩 JSON 데이터 전송
- [ ] Environment 변수 설정
- [ ] Tests 스크립트 작성
- [ ] Collection Runner로 일괄 테스트

---

## 🛠️ 문제 해결

### 422 Unprocessable Entity 오류
**원인**: Body 데이터 형식이 잘못됨

**해결**:
- Body 탭에서 **raw** 선택
- 오른쪽 드롭다운에서 **JSON** 선택
- JSON 형식 확인 (쉼표, 따옴표)

### 400 Bad Request
**원인**: 필수 필드 누락 또는 데이터 검증 실패

**해결**:
- 모든 필수 필드 포함 확인
- 데이터 타입 확인 (문자열, 숫자)
- 최소/최대 길이 확인

### 401 Unauthorized
**원인**: 인증 정보 없음 또는 잘못됨

**해결**:
- 로그인 먼저 수행
- 쿠키가 설정되었는지 확인

---

## 📚 다음 학습 내용

1. **Request 헤더 추가** - Authorization, Content-Type
2. **File Upload** - 이미지, 문서 업로드
3. **Batch Requests** - Collection Runner
4. **API 인증** - JWT 토큰
5. **Error Handling** - 다양한 에러 응답

---

## ✅ 테스트 체크리스트

### JSONResponse 예제
- [ ] 커스텀 상태 코드 (201, 202, 204)
- [ ] 커스텀 헤더 확인
- [ ] 쿠키 설정 확인
- [ ] 쿠키 삭제 확인
- [ ] 모든 기능 결합 테스트

### POST 요청 예제
- [ ] Simple POST
- [ ] Echo POST
- [ ] Form Data POST
- [ ] POST with Cookie
- [ ] Nested Data POST

### 사용자 API
- [ ] 사용자 생성 (201 Created)
- [ ] 중복 이메일 에러 (400)
- [ ] 모든 사용자 조회
- [ ] 특정 사용자 조회
- [ ] 로그인 성공 (쿠키 설정)
- [ ] 로그인 실패 (401)
- [ ] 사용자 정보 수정
- [ ] 로그아웃 (쿠키 삭제)
- [ ] 사용자 삭제

모든 테스트를 완료하면 POST 요청 마스터! 🎉

