from routers.post_router import router as post_router
# from routers.user_router import router as user_router  # Phase 2에서 구현 예정
from routers.comment_router import router as comment_router

__all__ = ["post_router", "comment_router"]
