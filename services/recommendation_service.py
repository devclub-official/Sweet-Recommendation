from typing import List, Dict
import numpy as np
from features.feature_registry import FeatureRegistry
from features.activity_features import ActivityFeatureExtractor
from features.user_features import UserFeatureExtractor
from models.similarity_model import SimilarityModel
from data.user_repository import UserRepository
from data.feed_repository import FeedRepository
from data.recommendation_repository import RecommendationRepository
from data.data_source import SQLAlchemyDataSource
from data.models import Team, TeamMembership, User

class RecommendationService:
    def __init__(self, session_factory):
        self.session_factory = session_factory
        self.feature_registry = FeatureRegistry()
        self.feature_registry.register('activity', ActivityFeatureExtractor())
        self.feature_registry.register('user', UserFeatureExtractor())
        
    def _get_repositories(self, session):
        """세션에서 필요한 리포지토리들을 가져옵니다"""
        data_source = SQLAlchemyDataSource(session)
        return {
            'user_repo': UserRepository(data_source),
            'feed_repo': FeedRepository(data_source),
            'recommendation_repo': RecommendationRepository(data_source)
        }
    
    def generate_user_recommendations(self):
        """모든 사용자에 대한 추천을 생성하고 DB에 저장합니다"""
        session = self.session_factory()
        try:
            repos = self._get_repositories(session)
            
            # 데이터 로드
            users = repos['user_repo'].get_all_users()
            feeds = repos['feed_repo'].get_all_feeds()
            
            if not users:
                print("No users found to generate recommendations")
                return
            
            # Feature 추출
            data = {'users': users, 'feeds': feeds}
            features = self.feature_registry.extract_all(data)
            
            # 모델 학습
            model = SimilarityModel(
                feature_weights={'activity': 1.0, 'user': 1.0}
            )
            model.train(features)
            
            # 각 사용자에 대해 추천 생성 및 저장
            for user in users:
                # 매칭 히스토리 가져오기 (중복 추천 방지)
                excluded_ids = repos['recommendation_repo'].get_user_match_history(user.id)
                
                # 추천 생성
                recommended_ids = model.recommend(user.id, count=5, excluded_ids=excluded_ids)
                
                if recommended_ids:
                    # 추천 점수 가져오기
                    scores = []
                    for rec_id in recommended_ids:
                        score = model.similarity_matrix.get(user.id, {}).get(rec_id, 0.0)
                        scores.append(score)
                    
                    # DB에 저장
                    repos['recommendation_repo'].save_user_recommendations(
                        user.id, recommended_ids, scores
                    )
                    
            print(f"Generated recommendations for {len(users)} users")
            
        finally:
            session.close()
    
    def generate_team_recommendations(self):
        """모든 팀에 대한 상대 팀 추천을 생성하고 DB에 저장합니다"""
        session = self.session_factory()
        try:
            repos = self._get_repositories(session)
            
            # 팀 데이터 로드
            teams = session.query(Team).all()
            if not teams:
                print("No teams found to generate recommendations")
                return
            
            # 각 팀의 멤버들의 평균 feature를 계산
            team_features = {}
            
            for team in teams:
                # 팀 멤버 가져오기
                members = session.query(User).join(TeamMembership).filter(
                    TeamMembership.team_id == team.id
                ).all()
                
                if members:
                    # 멤버들의 피드 가져오기
                    member_ids = [m.id for m in members]
                    feeds = repos['feed_repo'].get_feeds_by_user_ids(member_ids)
                    
                    # Feature 추출
                    data = {'users': members, 'feeds': feeds}
                    features = self.feature_registry.extract_all(data)
                    
                    # 팀 평균 feature 계산
                    team_vector = []
                    for feature_name, feature_set in features.items():
                        member_vectors = [feature_set[uid] for uid in member_ids if uid in feature_set]
                        if member_vectors:
                            avg_vector = np.mean(member_vectors, axis=0)
                            team_vector.append(avg_vector)
                    
                    if team_vector:
                        team_features[team.id] = np.concatenate(team_vector)
            
            # 팀 간 유사도 계산
            team_similarity_matrix = {}
            for team_id, vector in team_features.items():
                similarities = {}
                for other_id, other_vector in team_features.items():
                    if team_id != other_id:
                        from sklearn.metrics.pairwise import cosine_similarity
                        sim = cosine_similarity([vector], [other_vector])[0][0]
                        similarities[other_id] = sim
                team_similarity_matrix[team_id] = similarities
            
            # 각 팀에 대해 추천 생성 및 저장
            for team_id, similarities in team_similarity_matrix.items():
                if similarities:
                    # 상위 5개 팀 추천
                    recommended_team_ids = sorted(
                        similarities.keys(),
                        key=lambda x: similarities[x],
                        reverse=True
                    )[:5]
                    
                    scores = [similarities[tid] for tid in recommended_team_ids]
                    
                    # DB에 저장
                    repos['recommendation_repo'].save_team_recommendations(
                        team_id, recommended_team_ids, scores
                    )
            
            print(f"Generated team recommendations for {len(teams)} teams")
            
        finally:
            session.close()
    
    def get_user_recommendations(self, user_id: int) -> List[Dict]:
        """특정 사용자의 추천 결과를 가져옵니다"""
        session = self.session_factory()
        try:
            repos = self._get_repositories(session)
            
            # 추천된 사용자 ID 가져오기
            recommended_ids = repos['recommendation_repo'].get_recommendations_by_user_id(user_id)
            
            if not recommended_ids:
                # 추천이 없으면 실시간으로 생성 (선택적)
                return []
            
            # 추천된 사용자 정보 가져오기
            recommended_users = repos['user_repo'].get_users_by_ids(recommended_ids)
            
            # 결과 포맷팅
            results = []
            for user in recommended_users:
                results.append({
                    'id': user.id,
                    'name': user.name,
                    'username': user.username,
                    'profile_image': user.profile_image,
                    'bio': user.bio,
                    'region': user.region,
                    'age_group': user.age_group
                })
            
            return results
            
        finally:
            session.close()
    
    def get_team_recommendations(self, team_id: int) -> List[Dict]:
        """특정 팀의 추천 상대 팀을 가져옵니다"""
        session = self.session_factory()
        try:
            repos = self._get_repositories(session)
            
            # 추천된 팀 ID 가져오기
            recommended_ids = repos['recommendation_repo'].get_team_recommendations(team_id)
            
            if not recommended_ids:
                return []
            
            # 추천된 팀 정보 가져오기
            recommended_teams = session.query(Team).filter(Team.id.in_(recommended_ids)).all()
            
            # 결과 포맷팅
            results = []
            for team in recommended_teams:
                results.append({
                    'id': team.id,
                    'name': team.name,
                    'description': team.description,
                    'skill_level': team.skill_level,
                    'preferred_workout_type': team.preferred_workout_type,
                    'location': team.location
                })
            
            return results
            
        finally:
            session.close() 