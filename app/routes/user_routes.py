"""
사용자 관련 라우트
"""
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from datetime import datetime
from typing import List

from app.models.user import UserCreate, UserResponse, UserUpdate, LoginRequest

router = APIRouter(prefix="/api/users", tags=["Users"])

# 인메모리 데이터 저장소 (간단한 구현)
users_db = {}
user_id_counter = {"value": 1}


@router.post("", response_model=UserResponse, status_code=201)
async def create_user(user: UserCreate):
    """
    사용자 생성 (POST 요청)
    - username: 사용자 이름 (3-50자)
    - email: 이메일 주소
    - password: 비밀번호 (6자 이상)
    """
    # 이메일 중복 확인
    for existing_user in users_db.values():
        if existing_user["email"] == user.email:
            raise HTTPException(
                status_code=400,
                detail="이미 존재하는 이메일입니다."
            )
    
    # 사용자 생성
    user_id = user_id_counter["value"]
    user_id_counter["value"] += 1
    
    new_user = {
        "id": user_id,
        "username": user.username,
        "email": user.email,
        "password": user.password,  # 실제로는 해시화해야 함
        "created_at": datetime.now()
    }
    
    users_db[user_id] = new_user
    
    # 응답 (비밀번호 제외)
    response_data = {
        "id": new_user["id"],
        "username": new_user["username"],
        "email": new_user["email"],
        "created_at": new_user["created_at"]
    }
    
    # 커스텀 헤더 포함
    headers = {
        "X-User-ID": str(user_id),
        "X-Created-At": new_user["created_at"].isoformat()
    }
    
    return JSONResponse(
        status_code=201,
        content={
            "success": True,
            "message": "사용자가 성공적으로 생성되었습니다.",
            "data": {
                "id": response_data["id"],
                "username": response_data["username"],
                "email": response_data["email"],
                "created_at": response_data["created_at"].isoformat()
            }
        },
        headers=headers
    )


@router.get("")
async def get_users():
    """
    모든 사용자 조회
    """
    users_list = []
    for user in users_db.values():
        users_list.append({
            "id": user["id"],
            "username": user["username"],
            "email": user["email"],
            "created_at": user["created_at"].isoformat()
        })
    
    return JSONResponse(
        content={
            "success": True,
            "count": len(users_list),
            "data": users_list
        }
    )


@router.get("/{user_id}")
async def get_user(user_id: int):
    """
    특정 사용자 조회
    """
    if user_id not in users_db:
        return JSONResponse(
            status_code=404,
            content={
                "success": False,
                "error": "User Not Found",
                "message": f"ID {user_id}인 사용자를 찾을 수 없습니다."
            }
        )
    
    user = users_db[user_id]
    return JSONResponse(
        content={
            "success": True,
            "data": {
                "id": user["id"],
                "username": user["username"],
                "email": user["email"],
                "created_at": user["created_at"].isoformat()
            }
        }
    )


@router.post("/login")
async def login(login_data: LoginRequest):
    """
    로그인 (POST 요청)
    - 성공 시 쿠키에 토큰 설정
    """
    # 사용자 찾기
    user_found = None
    for user in users_db.values():
        if user["email"] == login_data.email and user["password"] == login_data.password:
            user_found = user
            break
    
    if not user_found:
        return JSONResponse(
            status_code=401,
            content={
                "success": False,
                "error": "Unauthorized",
                "message": "이메일 또는 비밀번호가 올바르지 않습니다."
            }
        )
    
    # 로그인 성공
    token = f"token-{user_found['id']}-{datetime.now().timestamp()}"
    
    content = {
        "success": True,
        "message": "로그인 성공!",
        "data": {
            "user_id": user_found["id"],
            "username": user_found["username"],
            "email": user_found["email"]
        }
    }
    
    response = JSONResponse(content=content)
    
    # 쿠키에 토큰 설정
    response.set_cookie(
        key="auth_token",
        value=token,
        max_age=3600,  # 1시간
        httponly=True,
        samesite="lax"
    )
    
    response.set_cookie(
        key="user_id",
        value=str(user_found["id"]),
        max_age=3600
    )
    
    return response


@router.post("/logout")
async def logout():
    """
    로그아웃 (쿠키 삭제)
    """
    content = {
        "success": True,
        "message": "로그아웃되었습니다."
    }
    
    response = JSONResponse(content=content)
    response.delete_cookie(key="auth_token")
    response.delete_cookie(key="user_id")
    
    return response


@router.put("/{user_id}")
async def update_user(user_id: int, user_update: UserUpdate):
    """
    사용자 정보 수정 (PUT 요청)
    """
    if user_id not in users_db:
        return JSONResponse(
            status_code=404,
            content={
                "success": False,
                "error": "User Not Found",
                "message": f"ID {user_id}인 사용자를 찾을 수 없습니다."
            }
        )
    
    user = users_db[user_id]
    
    # 수정할 필드만 업데이트
    if user_update.username:
        user["username"] = user_update.username
    if user_update.email:
        user["email"] = user_update.email
    if user_update.password:
        user["password"] = user_update.password
    
    user["updated_at"] = datetime.now()
    
    return JSONResponse(
        content={
            "success": True,
            "message": "사용자 정보가 수정되었습니다.",
            "data": {
                "id": user["id"],
                "username": user["username"],
                "email": user["email"],
                "updated_at": user["updated_at"].isoformat()
            }
        }
    )


@router.delete("/{user_id}")
async def delete_user(user_id: int):
    """
    사용자 삭제 (DELETE 요청)
    """
    if user_id not in users_db:
        return JSONResponse(
            status_code=404,
            content={
                "success": False,
                "error": "User Not Found",
                "message": f"ID {user_id}인 사용자를 찾을 수 없습니다."
            }
        )
    
    deleted_user = users_db.pop(user_id)
    
    return JSONResponse(
        content={
            "success": True,
            "message": f"사용자 '{deleted_user['username']}'가 삭제되었습니다.",
            "deleted_user_id": user_id
        }
    )

