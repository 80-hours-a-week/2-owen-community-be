from typing import List, Dict
from datetime import datetime
from models import board_model
from utils.exceptions import NotFoundError, ForbiddenError

# --- Controller (Business Logic) ---
class PostController:
    def __init__(self):
        # Phase 3: Model 계층 사용
        # 임시 사용자 정보 (인증 구현 전까지 하드코딩)
        self.MOCK_USER_ID = "user_001"  # UUID 형식으로 변경
        self.MOCK_USER_NICKNAME = "테스트유저"

    def get_all_posts(self):
        """게시글 목록 조회 로직"""
        posts_data = board_model.get_posts()
        return posts_data

    def get_post_by_id(self, post_id: str):
        """게시글 상세 조회 로직"""
        post = board_model.get_post_by_id(post_id)
        if not post:
            raise NotFoundError("게시글")

        # 조회수 증가
        board_model.increment_view_count(post_id)

        return post

    def create_post(self, req: Dict):
        """게시글 생성 로직"""
        # 입력값 검증 (제목과 내용이 비어있는지 확인)
        title = req.get("title", "").strip()
        content = req.get("content", "").strip()

        if not title:
            raise ForbiddenError("제목은 비어있을 수 없습니다")
        if not content:
            raise ForbiddenError("내용은 비어있을 수 없습니다")

        # Model을 통해 게시글 생성
        post_data = board_model.create_post(
            title=title,
            content=content,
            author_id=self.MOCK_USER_ID,
            author_nickname=self.MOCK_USER_NICKNAME
        )

        return post_data

    def update_post(self, post_id: str, req: Dict):
        """게시글 수정 로직"""
        post = board_model.get_post_by_id(post_id)
        if not post:
            raise NotFoundError("게시글")

        # TODO: Phase 7에서 세션 기반 권한 확인 추가
        if post["author_id"] != self.MOCK_USER_ID:
            raise ForbiddenError("게시글 작성자만 수정할 수 있습니다")

        # 입력값 검증
        title = req.get("title", "").strip()
        content = req.get("content", "").strip()

        if not title:
            raise ForbiddenError("제목은 비어있을 수 없습니다")
        if not content:
            raise ForbiddenError("내용은 비어있을 수 없습니다")

        # Model을 통해 게시글 수정
        updated_post = board_model.update_post(
            post_id=post_id,
            title=title,
            content=content
        )

        return updated_post

    def delete_post(self, post_id: str):
        """게시글 삭제 로직"""
        post = board_model.get_post_by_id(post_id)
        if not post:
            raise NotFoundError("게시글")

        # TODO: Phase 7에서 세션 기반 권한 확인 추가
        if post["author_id"] != self.MOCK_USER_ID:
            raise ForbiddenError("게시글 작성자만 삭제할 수 있습니다")

        # 게시글 삭제 시 관련 댓글들도 함께 삭제
        from models import comment_model
        deleted_comments_count = comment_model.delete_comments_by_post(post_id)

        # Model을 통해 게시글 삭제
        board_model.delete_post(post_id)

        return post

# 컨트롤러 인스턴스 생성
post_controller = PostController()


