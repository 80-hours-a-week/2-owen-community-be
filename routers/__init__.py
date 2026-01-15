from routers.post_router import router as post_router
from routers.comment_router import router as comment_router
from routers.auth_router import router as auth_router

__all__ = ["post_router", "comment_router", "auth_router"]
