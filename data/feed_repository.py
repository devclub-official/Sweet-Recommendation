from typing import List, Optional
from sqlalchemy.orm import Session
from .models import Feed

class FeedRepository:
    def __init__(self, data_source):
        self.data_source = data_source
        
    def get_feed_by_id(self, feed_id: int) -> Optional[Feed]:
        """ID로 피드 조회"""
        return self.data_source.get_data(
            lambda session: session.query(Feed).filter(Feed.id == feed_id).first()
        )
        
    def get_feeds_by_user_id(self, user_id: int) -> List[Feed]:
        """사용자 ID로 피드 목록 조회"""
        return self.data_source.get_data(
            lambda session: session.query(Feed).filter(Feed.user_id == user_id).all()
        )
        
    def get_all_feeds(self) -> List[Feed]:
        """모든 피드 조회"""
        return self.data_source.get_data(
            lambda session: session.query(Feed).all()
        )
