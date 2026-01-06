"""
FastAPI 커뮤니티 백엔드 메인 애플리케이션
"""
from fastapi import FastAPI
from datetime import datetime

# 라우터 임포트
from app.routes import response_examples, user_routes, post_examples

# FastAPI 앱 인스턴스 생성
app = FastAPI(
    title="Owen Community API",
    description="FastAPI 기반 커뮤니티 백엔드 API",
    version="0.1.0"
)

# 라우터 등록
app.include_router(response_examples.router)
app.include_router(user_routes.router)
app.include_router(post_examples.router)


# 루트 엔드포인트
@app.get("/")
async def root():
    """
    루트 경로 - API 상태 확인
    """
    return {
        "message": "Owen Community API에 오신 것을 환영합니다!",
        "status": "running",
        "timestamp": datetime.now().isoformat()
    }


# 헬스체크 엔드포인트
@app.get("/health")
async def health_check():
    """
    헬스체크 - 서버 상태 확인
    """
    return {
        "status": "healthy",
        "service": "owen-community-backend",
        "timestamp": datetime.now().isoformat()
    }


# API 정보 엔드포인트
@app.get("/api/info")
async def api_info():
    """
    API 정보 조회
    """
    return {
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


# 테스트용 GET 엔드포인트
@app.get("/api/test")
async def test_endpoint():
    """
    테스트용 엔드포인트
    """
    return {
        "success": True,
        "message": "GET 요청이 성공적으로 처리되었습니다!",
        "data": {
            "test": "Hello from FastAPI",
            "method": "GET",
            "timestamp": datetime.now().isoformat()
        }
    }


# 파라미터를 받는 GET 엔드포인트
@app.get("/api/greet/{name}")
async def greet_user(name: str):
    """
    사용자 이름으로 인사하는 엔드포인트
    """
    return {
        "success": True,
        "message": f"안녕하세요, {name}님!",
        "timestamp": datetime.now().isoformat()
    }


# 쿼리 파라미터를 받는 GET 엔드포인트
@app.get("/api/search")
async def search(q: str = None, limit: int = 10):
    """
    검색 엔드포인트 (쿼리 파라미터 예제)
    """
    return {
        "success": True,
        "query": q,
        "limit": limit,
        "message": f"'{q}' 검색 결과" if q else "검색어를 입력하세요",
        "results": []
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

