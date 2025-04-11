import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from .base_model import RecommendationModel

class SimilarityModel(RecommendationModel):
    def __init__(self, feature_weights=None):
        self.user_vectors = {}
        self.similarity_matrix = {}
        self.feature_weights = feature_weights or {}
        
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
        """모든 사용자 쌍 간의 유사도 계산"""
        self.similarity_matrix = {}
        
        for user_id, vector in self.user_vectors.items():
            similarities = {}
            
            for other_id, other_vector in self.user_vectors.items():
                if user_id != other_id:
                    # 벡터가 비어있지 않은 경우만 유사도 계산
                    if vector.size > 0 and other_vector.size > 0:
                        sim = cosine_similarity([vector], [other_vector])[0][0]
                        similarities[other_id] = sim
            
            self.similarity_matrix[user_id] = similarities
    
    def recommend(self, user_id, count=5):
        """
        유사도 기반 추천
        
        Args:
            user_id: 추천 대상 사용자 ID
            count: 추천할 사용자 수
            
        Returns:
            추천된 사용자 ID 리스트
        """
        if user_id not in self.similarity_matrix:
            return []
            
        similarities = self.similarity_matrix[user_id]
        
        # 유사도 기준 내림차순 정렬 후 상위 count개 선택
        recommended_ids = sorted(
            similarities.keys(),
            key=lambda x: similarities[x],
            reverse=True
        )[:count]
        
        return recommended_ids
