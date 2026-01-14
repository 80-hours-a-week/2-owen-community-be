from typing import Dict, List, Optional
from datetime import datetime
import uuid


class CommentModel:
    """댓글 데이터 관리 Model"""

    def __init__(self):
        # 메모리 기반 댓글 저장소
        self.comments_db: Dict[str, Dict] = {}
        self.next_comment_id = 1

    def get_next_comment_id(self) -> str:
        """다음 댓글 ID 생성 (UUID 사용)"""
        comment_id = str(uuid.uuid4())
        return comment_id

    def create_comment(self, post_id: str, user_id: str, user_nickname: str, content: str) -> Dict:
        """댓글 생성"""
        comment_id = self.get_next_comment_id()

        comment_data = {
            "comment_id": comment_id,
            "post_id": post_id,
            "user_id": user_id,
            "user_nickname": user_nickname,
            "content": content,
            "created_at": datetime.now().isoformat(),
            "updated_at": None
        }

        self.comments_db[comment_id] = comment_data
        return comment_data.copy()

    def get_comments_by_post(self, post_id: str) -> List[Dict]:
        """특정 게시글의 모든 댓글 조회 (최신순)"""
        post_comments = [
            comment for comment in self.comments_db.values()
            if comment["post_id"] == post_id
        ]

        # 최신순 정렬
        return sorted(post_comments, key=lambda x: x["created_at"], reverse=True)

    def get_comment_by_id(self, comment_id: str) -> Optional[Dict]:
        """ID로 댓글 조회"""
        return self.comments_db.get(comment_id)

    def update_comment(self, comment_id: str, content: str) -> Optional[Dict]:
        """댓글 수정"""
        if comment_id not in self.comments_db:
            return None

        comment = self.comments_db[comment_id]
        comment["content"] = content
        comment["updated_at"] = datetime.now().isoformat()

        return comment.copy()

    def delete_comment(self, comment_id: str) -> bool:
        """댓글 삭제"""
        if comment_id in self.comments_db:
            del self.comments_db[comment_id]
            return True
        return False

    def get_comments_by_user(self, user_id: str) -> List[Dict]:
        """특정 사용자의 모든 댓글 조회"""
        return [
            comment for comment in self.comments_db.values()
            if comment["user_id"] == user_id
        ]

    def get_comments_count_by_post(self, post_id: str) -> int:
        """특정 게시글의 댓글 수 조회"""
        return len([
            comment for comment in self.comments_db.values()
            if comment["post_id"] == post_id
        ])

    def delete_comments_by_post(self, post_id: str) -> int:
        """특정 게시글의 모든 댓글 삭제 (게시글 삭제 시 사용)"""
        comments_to_delete = [
            comment_id for comment_id, comment in self.comments_db.items()
            if comment["post_id"] == post_id
        ]

        for comment_id in comments_to_delete:
            del self.comments_db[comment_id]

        return len(comments_to_delete)

    def get_total_comments_count(self) -> int:
        """전체 댓글 수 조회"""
        return len(self.comments_db)


# Model 인스턴스 생성
comment_model = CommentModel()