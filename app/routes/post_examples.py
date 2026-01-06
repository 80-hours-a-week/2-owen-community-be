"""
POST 요청 예제 라우트
"""
from fastapi import APIRouter, Body
from fastapi.responses import JSONResponse
from datetime import datetime
from typing import Dict, Any

router = APIRouter(prefix="/api/post-examples", tags=["POST Examples"])


@router.post("/simple")
async def simple_post(data: Dict[str, Any] = Body(...)):
    """
    간단한 POST 요청 예제
    - 모든 JSON 데이터를 받아서 에코
    """
    return JSONResponse(
        status_code=201,
        content={
            "success": True,
            "message": "POST 요청을 받았습니다!",
            "received_data": data,
            "timestamp": datetime.now().isoformat()
        }
    )


@router.post("/echo")
async def echo_post(
    name: str = Body(...),
    age: int = Body(...),
    email: str = Body(...)
):
    """
    필드별로 데이터를 받는 POST 예제
    """
    return JSONResponse(
        status_code=200,
        content={
            "success": True,
            "message": "데이터를 받았습니다!",
            "received": {
                "name": name,
                "age": age,
                "email": email
            },
            "timestamp": datetime.now().isoformat()
        }
    )


@router.post("/form-data")
async def form_data_example(data: Dict[str, Any]):
    """
    폼 데이터 처리 예제
    """
    return JSONResponse(
        status_code=201,
        content={
            "success": True,
            "message": "폼 데이터가 처리되었습니다.",
            "form_data": data,
            "data_type": str(type(data).__name__)
        },
        headers={
            "X-Form-Processed": "true",
            "X-Data-Count": str(len(data))
        }
    )


@router.post("/with-cookie")
async def post_with_cookie(data: Dict[str, Any]):
    """
    POST 요청 후 쿠키 설정 예제
    """
    content = {
        "success": True,
        "message": "데이터를 저장하고 쿠키를 설정했습니다!",
        "saved_data": data,
        "timestamp": datetime.now().isoformat()
    }
    
    response = JSONResponse(
        status_code=201,
        content=content
    )
    
    # 쿠키 설정
    response.set_cookie(
        key="last_post_time",
        value=datetime.now().isoformat(),
        max_age=3600
    )
    
    response.set_cookie(
        key="post_count",
        value="1",
        max_age=3600
    )
    
    return response


@router.post("/nested-data")
async def nested_data_post(data: Dict[str, Any]):
    """
    중첩된 JSON 데이터 처리 예제
    """
    return JSONResponse(
        status_code=201,
        content={
            "success": True,
            "message": "중첩된 데이터를 처리했습니다.",
            "received_data": data,
            "data_structure": {
                "keys": list(data.keys()),
                "total_fields": len(data)
            }
        },
        headers={
            "X-Data-Type": "nested",
            "X-Processing-Time": "0.001s"
        }
    )

