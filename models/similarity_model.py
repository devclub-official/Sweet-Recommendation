import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from .base_model import RecommendationModel

class SimilarityModel(RecommendationModel):
    def __init__(self, feature_weights=None, similarity_features=None, diversity_features=None):
        self.user_vectors = {}
        self.similarity_matrix = {}
        self.feature_weights = feature_weights or {}
        # 유사할수록 좋은 feature들
        self.similarity_features = similarity_features or [
            'exercise_type', 'exercise_time', 'workout_duration', 
            'age_group', 'region', 'preferred_group_size'
        ]
        # 다양성이 있으면 좋은 feature들
        self.diversity_features = diversity_features or [
            'gender', 'engagement_level'
        ]
        self.feature_indices = {}
        
    def train(self, features):
        """
        특성 데이터를 기반으로 유사도 모델 학습
        
        Args:
            features: 사용자별 특성 벡터 딕셔너리
        """
        # 모든 특성을 결합하여 사용자 벡터 생성
        user_ids = set()
        for feature_set in features.values():
            user_ids.update(feature_set.keys())
        
        # feature 인덱스 매핑 생성
        current_idx = 0
        for feature_name, feature_set in features.items():
            if feature_set:
                sample_vector = next(iter(feature_set.values()))
                feature_size = len(sample_vector)
                self.feature_indices[feature_name] = (current_idx, current_idx + feature_size)
                current_idx += feature_size
        
        # 가중치 적용 및 특성 결합
        self.user_vectors = {}
        
        for user_id in user_ids:
            combined_vector = []
            
            for feature_name, feature_set in features.items():
                if user_id in feature_set:
                    vector = feature_set[user_id]
                    # 특성 가중치 적용
                    if feature_name in self.feature_weights:
                        vector = vector * self.feature_weights[feature_name]
                    combined_vector.append(vector)
            
            # 결합된 벡터가 있으면 저장
            if combined_vector:
                self.user_vectors[user_id] = np.concatenate(combined_vector)
        
        # 유사도 행렬 계산
        self._compute_similarity_matrix()
        
    def _compute_similarity_matrix(self):
        """모든 사용자 쌍 간의 유사도 계산 (유사성과 보완성 모두 고려)"""
        self.similarity_matrix = {}
        
        for user_id, vector in self.user_vectors.items():
            similarities = {}
            
            for other_id, other_vector in self.user_vectors.items():
                if user_id != other_id:
                    # 벡터가 비어있지 않은 경우만 유사도 계산
                    if vector.size > 0 and other_vector.size > 0:
                        # 기본 코사인 유사도
                        base_sim = cosine_similarity([vector], [other_vector])[0][0]
                        
                        # 보완성 점수 계산
                        diversity_score = self._calculate_diversity_score(vector, other_vector)
                        
                        # 최종 점수 = 유사도 * 0.7 + 보완성 점수 * 0.3
                        final_score = base_sim * 0.7 + diversity_score * 0.3
                        similarities[other_id] = final_score
            
            self.similarity_matrix[user_id] = similarities
    
    def _calculate_diversity_score(self, vector1, vector2):
        """보완성 점수 계산 (다를수록 높은 점수)"""
        # 성별과 engagement_level이 다르면 보너스
        # 실제 구현에서는 feature_indices를 사용해 특정 feature 위치를 찾아 비교
        # 여기서는 간단히 벡터의 일부 요소가 다른 정도를 측정
        diff = np.abs(vector1 - vector2)
        # 차이를 0~1로 정규화
        diversity = np.mean(diff) / (np.max(diff) + 1e-6)
        return min(diversity, 1.0)
    
    def recommend(self, user_id, count=5, excluded_ids=None):
        """
        유사도 기반 추천
        
        Args:
            user_id: 추천 대상 사용자 ID
            count: 추천할 사용자 수
            excluded_ids: 제외할 사용자 ID 리스트 (매칭 히스토리)
            
        Returns:
            추천된 사용자 ID 리스트
        """
        if user_id not in self.similarity_matrix:
            return []
            
        similarities = self.similarity_matrix[user_id]
        
        # 제외할 ID 필터링
        if excluded_ids:
            similarities = {k: v for k, v in similarities.items() if k not in excluded_ids}
        
        # 유사도 기준 내림차순 정렬 후 상위 count개 선택
        recommended_ids = sorted(
            similarities.keys(),
            key=lambda x: similarities[x],
            reverse=True
        )[:count]
        
        return recommended_ids
