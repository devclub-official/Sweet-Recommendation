from typing import List, Optional
from sqlalchemy.orm import Session
from data.models import Recommendation, Team, TeamMembership, User

class RecommendationRepository:
    def __init__(self, data_source):
        self.data_source = data_source
        # 추천 결과를 메모리/DB에서 불러오도록 구현 필요

    def get_recommendations_by_user_id(self, user_id: int, count: int = 5) -> List[int]:
        """사용자 ID로 추천 목록 조회"""
        # DB에서 추천 결과 조회
        recommendations = self.data_source.get_data(
            lambda session: session.query(Recommendation)
                .filter(Recommendation.source_id == user_id, Recommendation.type == 'user')
                .order_by(Recommendation.score.desc())
                .limit(count)
                .all()
        )
        
        if recommendations:
            return [rec.target_id for rec in recommendations]
        
        # 추천 결과가 없으면 빈 리스트 반환
        return []
    
    def get_team_recommendations(self, team_id: int, count: int = 5) -> List[int]:
        """팀 ID로 상대 팀 추천 목록 조회"""
        # DB에서 팀 추천 결과 조회
        recommendations = self.data_source.get_data(
            lambda session: session.query(Recommendation)
                .filter(Recommendation.source_id == team_id, Recommendation.type == 'team')
                .order_by(Recommendation.score.desc())
                .limit(count)
                .all()
        )
        
        if recommendations:
            return [rec.target_id for rec in recommendations]
        
        return []
    
    def save_user_recommendations(self, user_id: int, recommended_ids: List[int], scores: List[float]):
        """사용자 추천 결과 저장"""
        def save_recommendations(session):
            # 기존 추천 삭제
            session.query(Recommendation).filter(
                Recommendation.source_id == user_id,
                Recommendation.type == 'user'
            ).delete()
            
            # 새로운 추천 저장
            for target_id, score in zip(recommended_ids, scores):
                rec = Recommendation(
                    source_id=user_id,
                    target_id=target_id,
                    type='user',
                    score=score
                )
                session.add(rec)
            
            session.commit()
        
        self.data_source.execute(save_recommendations)
    
    def save_team_recommendations(self, team_id: int, recommended_team_ids: List[int], scores: List[float]):
        """팀 추천 결과 저장"""
        def save_recommendations(session):
            # 기존 추천 삭제
            session.query(Recommendation).filter(
                Recommendation.source_id == team_id,
                Recommendation.type == 'team'
            ).delete()
            
            # 새로운 추천 저장
            for target_id, score in zip(recommended_team_ids, scores):
                rec = Recommendation(
                    source_id=team_id,
                    target_id=target_id,
                    type='team',
                    score=score
                )
                session.add(rec)
            
            session.commit()
        
        self.data_source.execute(save_recommendations)
    
    def get_user_match_history(self, user_id: int) -> List[int]:
        """사용자의 이전 매칭 히스토리 조회 (중복 추천 방지용)"""
        # TODO: 실제 매칭 히스토리 테이블에서 조회
        # 지금은 빈 리스트 반환
        return []
    