from typing import List, Optional
from sqlalchemy.orm import Session
# TODO: Recommendation 테이블 추가
# from data.models import Recommendation

class RecommendationRepository:
    def __init__(self, data_source):
        self.data_source = data_source

    def get_recommendations_by_user_id(self, user_id: int):
        """사용자 ID로 추천 목록 조회"""

        # TODO: 추천 임베딩은 벡터DB에서 추출
        # recommendations = self.data_source.get_data(
        #     lambda session: session.query(Recommendation).filter(Recommendation.user_id == user_id).all()
        # )

        recommendations = [1,2,3,4] # sample user_ids

        # TODO: 추천 목록 중에 모임 참여 불가능한 사용자 필터링


        return recommendations
    