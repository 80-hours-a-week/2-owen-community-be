"""
사용자 관련 Pydantic 모델
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):
    """사용자 생성 요청 모델"""
    username: str = Field(..., min_length=3, max_length=50, description="사용자 이름")
    email: str = Field(..., description="이메일 주소")
    password: str = Field(..., min_length=6, description="비밀번호")
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "username": "hong_gildong",
                    "email": "hong@example.com",
                    "password": "secure123"
                }
            ]
        }
    }


class UserResponse(BaseModel):
    """사용자 응답 모델"""
    id: int
    username: str
    email: str
    created_at: datetime
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": 1,
                    "username": "hong_gildong",
                    "email": "hong@example.com",
                    "created_at": "2026-01-06T15:30:00"
                }
            ]
        }
    }


class UserUpdate(BaseModel):
    """사용자 수정 요청 모델"""
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[str] = None
    password: Optional[str] = Field(None, min_length=6)


class LoginRequest(BaseModel):
    """로그인 요청 모델"""
    email: str
    password: str
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "email": "hong@example.com",
                    "password": "secure123"
                }
            ]
        }
    }

