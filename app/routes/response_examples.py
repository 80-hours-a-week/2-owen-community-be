"""
JSONResponse 사용 예제 라우트
- 커스텀 상태 코드
- 커스텀 헤더
- 쿠키 설정
"""
from fastapi import APIRouter, Response
from fastapi.responses import JSONResponse
from datetime import datetime, timedelta

router = APIRouter(prefix="/api/examples", tags=["JSONResponse Examples"])


@router.get("/custom-status")
async def custom_status_code():
    """
    커스텀 상태 코드 예제
    - 201: Created (리소스 생성됨)
    """
    content = {
        "success": True,
        "message": "커스텀 상태 코드 201 (Created) 반환",
        "data": {"id": 1, "name": "새로운 리소스"},
        "timestamp": datetime.now().isoformat()
    }
    return JSONResponse(
        status_code=201,
        content=content
    )


@router.get("/custom-status/accepted")
async def custom_status_accepted():
    """
    202 Accepted 상태 코드 예제
    - 요청은 받았지만 처리는 완료되지 않음
    """
    content = {
        "success": True,
        "message": "요청이 접수되었습니다. 처리 중입니다.",
        "status": "processing",
        "job_id": "job-12345",
        "timestamp": datetime.now().isoformat()
    }
    return JSONResponse(
        status_code=202,
        content=content
    )


@router.get("/custom-status/no-content")
async def custom_status_no_content():
    """
    204 No Content 상태 코드 예제
    - 성공했지만 반환할 내용이 없음
    """
    return JSONResponse(
        status_code=204,
        content=None
    )


@router.get("/custom-headers")
async def custom_headers():
    """
    커스텀 헤더 추가 예제
    - X-Custom-Header: 사용자 정의 헤더
    - X-Request-ID: 요청 추적 ID
    - X-API-Version: API 버전
    """
    content = {
        "success": True,
        "message": "커스텀 헤더가 포함된 응답입니다.",
        "note": "Response Headers를 확인하세요!",
        "timestamp": datetime.now().isoformat()
    }
    
    headers = {
        "X-Custom-Header": "Owen Community API",
        "X-Request-ID": f"req-{datetime.now().timestamp()}",
        "X-API-Version": "1.0.0",
        "X-Powered-By": "FastAPI",
        "X-Developer": "Owen Team"
    }
    
    return JSONResponse(
        content=content,
        headers=headers
    )


@router.get("/set-cookie")
async def set_cookie():
    """
    쿠키 설정 예제
    - user_token: 사용자 토큰
    - session_id: 세션 ID
    """
    content = {
        "success": True,
        "message": "쿠키가 설정되었습니다!",
        "cookies_set": ["user_token", "session_id", "preferences"],
        "note": "브라우저에 쿠키가 저장되었습니다.",
        "timestamp": datetime.now().isoformat()
    }
    
    response = JSONResponse(content=content)
    
    # 쿠키 설정
    response.set_cookie(
        key="user_token",
        value="token-abc123xyz",
        max_age=3600,  # 1시간
        httponly=True,  # JavaScript 접근 불가 (보안)
        samesite="lax"
    )
    
    response.set_cookie(
        key="session_id",
        value="session-987654",
        max_age=7200,  # 2시간
        httponly=True
    )
    
    response.set_cookie(
        key="preferences",
        value="dark_mode=true;lang=ko",
        max_age=86400  # 24시간
    )
    
    return response


@router.get("/set-cookie/secure")
async def set_secure_cookie():
    """
    보안 쿠키 설정 예제
    - httponly: JavaScript 접근 차단
    - secure: HTTPS에서만 전송
    - samesite: CSRF 공격 방지
    """
    content = {
        "success": True,
        "message": "보안 쿠키가 설정되었습니다!",
        "security_features": {
            "httponly": "JavaScript 접근 차단",
            "secure": "HTTPS에서만 전송",
            "samesite": "CSRF 공격 방지"
        }
    }
    
    response = JSONResponse(content=content)
    
    # 만료 시간 설정
    expires = datetime.now() + timedelta(days=7)
    
    response.set_cookie(
        key="auth_token",
        value="secure-token-xyz789",
        expires=expires,
        httponly=True,
        secure=False,  # 로컬 테스트를 위해 False (실제로는 True)
        samesite="strict"
    )
    
    return response


@router.get("/delete-cookie")
async def delete_cookie():
    """
    쿠키 삭제 예제
    """
    content = {
        "success": True,
        "message": "쿠키가 삭제되었습니다!",
        "deleted_cookies": ["user_token", "session_id"]
    }
    
    response = JSONResponse(content=content)
    
    # 쿠키 삭제 (max_age=0)
    response.delete_cookie(key="user_token")
    response.delete_cookie(key="session_id")
    response.delete_cookie(key="preferences")
    
    return response


@router.get("/combined")
async def combined_example():
    """
    모든 기능을 결합한 예제
    - 커스텀 상태 코드: 201
    - 커스텀 헤더: 여러 개
    - 쿠키: 설정
    """
    content = {
        "success": True,
        "message": "상태 코드 + 헤더 + 쿠키 모두 포함!",
        "features": {
            "status_code": 201,
            "custom_headers": 3,
            "cookies": 1
        },
        "timestamp": datetime.now().isoformat()
    }
    
    headers = {
        "X-Custom-Header": "Combined Example",
        "X-Request-ID": f"req-combined-{datetime.now().timestamp()}",
        "X-Response-Type": "Full Featured"
    }
    
    response = JSONResponse(
        status_code=201,
        content=content,
        headers=headers
    )
    
    response.set_cookie(
        key="combined_token",
        value="token-combined-123",
        max_age=3600,
        httponly=True
    )
    
    return response


@router.get("/error-example/404")
async def error_404():
    """
    404 에러 예제
    """
    content = {
        "success": False,
        "error": "Not Found",
        "message": "요청한 리소스를 찾을 수 없습니다.",
        "status_code": 404,
        "timestamp": datetime.now().isoformat()
    }
    return JSONResponse(
        status_code=404,
        content=content
    )


@router.get("/error-example/403")
async def error_403():
    """
    403 Forbidden 에러 예제
    """
    content = {
        "success": False,
        "error": "Forbidden",
        "message": "이 리소스에 접근할 권한이 없습니다.",
        "status_code": 403,
        "timestamp": datetime.now().isoformat()
    }
    return JSONResponse(
        status_code=403,
        content=content
    )

