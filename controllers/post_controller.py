from typing import List, Dict, Union
from datetime import datetime
from uuid import UUID
from models import post_model
from utils.exceptions import PostNotFoundError, ForbiddenError, ValidationError
from utils.error_codes import ErrorCode

# --- Controller (Business Logic) ---
class PostController:
    """게시글 관련 비즈니스 로직"""
    def __init__(self):
        # 임시 사용자 정보 (인증 구현 전까지 하드코딩)
        # 하이브리드 방식에 맞춰 내부적으로는 문자열 형식을 기본으로 사용하거나 
        # Union 타입을 지원하도록 설정합니다.
        self.MOCK_USER_ID = "00000000-0000-0000-0000-000000000001"
        self.MOCK_USER_NICKNAME = "테스트유저"

    def get_all_posts(self):
        """게시글 목록 조회 로직"""
        posts_data = post_model.get_posts()
        return posts_data

    def get_post_by_id(self, post_id: Union[UUID, str]):
        """게시글 상세 조회 로직"""
        post = post_model.get_post_by_id(post_id)
        if not post:
            raise PostNotFoundError(str(post_id))

        # 조회수 증가
        post_model.increment_view_count(post_id)

        return post

    def create_post(self, req: Dict):
        """게시글 생성 로직"""
        # 입력값 검증
        title = req.get("title", "").strip()
        content = req.get("content", "").strip()

        if not title:
            raise ValidationError(ErrorCode.TITLE_TOO_SHORT, {"field": "title"})
        if not content:
            raise ValidationError(ErrorCode.EMPTY_CONTENT, {"field": "content"})

        # Model을 통해 게시글 생성 (author_id는 내부 MOCK 사용)
        post_data = post_model.create_post(
            title=title,
            content=content,
            author_id=self.MOCK_USER_ID,
            author_nickname=self.MOCK_USER_NICKNAME
        )

        return post_data

    def update_post(self, post_id: Union[UUID, str], req: Dict):
        """게시글 수정 로직"""
        post = post_model.get_post_by_id(post_id)
        if not post:
            raise PostNotFoundError(str(post_id))

        # 권한 확인 (작성자 확인)
        # Model에서 넘어온 author_id(str)와 MOCK_USER_ID(str) 비교
        if post["author_id"] != self.MOCK_USER_ID:
            raise ForbiddenError(ErrorCode.NOT_OWNER, {"resource": "게시글"})

        # 입력값 검증
        title = req.get("title", "").strip()
        content = req.get("content", "").strip()

        if not title:
            raise ValidationError(ErrorCode.TITLE_TOO_SHORT, {"field": "title"})
        if not content:
            raise ValidationError(ErrorCode.EMPTY_CONTENT, {"field": "content"})

        # Model을 통해 게시글 수정
        updated_post = post_model.update_post(
            post_id=post_id,
            title=title,
            content=content
        )

        return updated_post

    def delete_post(self, post_id: Union[UUID, str]):
        """게시글 삭제 로직"""
        post = post_model.get_post_by_id(post_id)
        if not post:
            raise PostNotFoundError(str(post_id))

        # 권한 확인
        if post["author_id"] != self.MOCK_USER_ID:
            raise ForbiddenError(ErrorCode.NOT_OWNER, {"resource": "게시글"})

        # 게시글 삭제 시 관련 댓글들도 함께 삭제
        from models import comment_model
        comment_model.delete_comments_by_post(post_id)

        # Model을 통해 게시글 삭제
        post_model.delete_post(post_id)

        return post

# 컨트롤러 인스턴스 생성
post_controller = PostController()
