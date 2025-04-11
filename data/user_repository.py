from typing import List, Optional
from sqlalchemy.orm import Session
from .models import User

class UserRepository:
    def __init__(self, data_source):
        self.data_source = data_source
        
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """ID로 사용자 조회"""
        return self.data_source.get_data(
            lambda session: session.query(User).filter(User.id == user_id).first()
        )
        
    def get_users_by_ids(self, user_ids: List[int]) -> List[User]:
        """ID 목록으로 사용자 목록 조회"""
        if not user_ids:
            return []
            
        return self.data_source.get_data(
            lambda session: session.query(User).filter(User.id.in_(user_ids)).all()
        )
        
    def get_all_users(self) -> List[User]:
        """모든 사용자 조회"""
        return self.data_source.get_data(
            lambda session: session.query(User).all()
        )
