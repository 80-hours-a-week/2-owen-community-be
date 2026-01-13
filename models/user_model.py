from typing import Dict, Optional
from datetime import datetime
import uuid


class UserModel:
    """사용자 데이터 관리 Model"""

    def __init__(self):
        # 메모리 기반 사용자 저장소
        self.users_db: Dict[str, Dict] = {}
        self.next_user_id = 1

    def get_next_user_id(self) -> str:
        """다음 사용자 ID 생성 (UUID 사용)"""
        user_id = str(uuid.uuid4())
        return user_id

    def create_user(self, email: str, password: str, nickname: str, profile_image_url: Optional[str] = None) -> Dict:
        """사용자 생성"""
        user_id = self.get_next_user_id()

        user_data = {
            "user_id": user_id,
            "email": email,
            "password": password,  # 실제로는 해싱해야 함 (Phase 4에서 구현)
            "nickname": nickname,
            "profile_image_url": profile_image_url,
            "created_at": datetime.now().isoformat(),
            "updated_at": None
        }

        self.users_db[user_id] = user_data
        return user_data.copy()

    def get_user_by_id(self, user_id: str) -> Optional[Dict]:
        """ID로 사용자 조회"""
        return self.users_db.get(user_id)

    def get_user_by_email(self, email: str) -> Optional[Dict]:
        """이메일로 사용자 조회"""
        for user in self.users_db.values():
            if user["email"] == email:
                return user
        return None

    def email_exists(self, email: str) -> bool:
        """이메일 중복 체크"""
        return self.get_user_by_email(email) is not None

    def nickname_exists(self, nickname: str) -> bool:
        """닉네임 중복 체크"""
        for user in self.users_db.values():
            if user["nickname"] == nickname:
                return True
        return False

    def update_user(self, user_id: str, update_data: Dict) -> Optional[Dict]:
        """사용자 정보 수정"""
        if user_id not in self.users_db:
            return None

        user = self.users_db[user_id]

        # 업데이트 가능한 필드들
        allowed_fields = ["nickname", "profile_image_url", "password"]
        for field in allowed_fields:
            if field in update_data:
                user[field] = update_data[field]

        user["updated_at"] = datetime.now().isoformat()
        return user.copy()

    def delete_user(self, user_id: str) -> bool:
        """사용자 삭제"""
        if user_id in self.users_db:
            del self.users_db[user_id]
            return True
        return False

    def get_all_users(self) -> list:
        """모든 사용자 조회 (관리용)"""
        return list(self.users_db.values())

    def authenticate_user(self, email: str, password: str) -> Optional[Dict]:
        """사용자 인증 (로그인용)"""
        user = self.get_user_by_email(email)
        if user and user["password"] == password:  # 실제로는 해싱 비교
            return user
        return None


# Model 인스턴스 생성
user_model = UserModel()