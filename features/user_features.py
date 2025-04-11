import numpy as np
from sklearn.preprocessing import OneHotEncoder
from .base_extractor import FeatureExtractor

class UserFeatureExtractor(FeatureExtractor):
    def __init__(self):
        self.encoders = {}
        self._feature_names = []
        
    def fit(self, users):
        """데이터에 맞게 인코더 학습"""
        # 향후 성별, 선호 운동 유형 등의 범주형 변수에 대한 인코더 준비
        # 현재는 구현된 필드가 없으므로 패스
        pass
        
    def extract(self, data):
        """사용자 데이터에서 특성 추출"""
        users = data.get('users', [])
        if not users:
            return np.array([])
            
        # 사용자 ID별 특성 벡터 생성
        user_features = {}
        
        for user in users:
            # 현재는 제한된 특성이 있으므로 기본 특성만 추출
            # TODO: 향후 age, gender, favorite_workout_type 등 추가되면 확장
            features = []
            user_features[user.id] = np.array(features) if features else np.array([])
            
        return user_features
    
    @property
    def feature_names(self):
        return self._feature_names
