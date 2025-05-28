import numpy as np
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
from .base_extractor import FeatureExtractor

class UserFeatureExtractor(FeatureExtractor):
    def __init__(self):
        self.gender_encoder = LabelEncoder()
        self.age_encoder = LabelEncoder()
        self.region_encoder = LabelEncoder()
        self._feature_names = []
        
    def fit(self, users):
        """데이터에 맞게 인코더 학습"""
        genders = [u.gender for u in users if u.gender]
        ages = [u.age_group for u in users if u.age_group]
        regions = [u.region for u in users if u.region]
        
        if genders:
            self.gender_encoder.fit(genders)
        if ages:
            self.age_encoder.fit(ages)
        if regions:
            self.region_encoder.fit(regions)
            
        # feature 이름 설정
        self._feature_names = [
            'gender_encoded',
            'age_group_encoded', 
            'region_encoded',
            'preferred_group_size'
        ]
        
    def extract(self, data):
        """사용자 데이터에서 특성 추출"""
        users = data.get('users', [])
        if not users:
            return {}
            
        # 먼저 fit 수행
        self.fit(users)
            
        # 사용자 ID별 특성 벡터 생성
        user_features = {}
        
        for user in users:
            features = []
            
            # 성별 인코딩
            if user.gender:
                try:
                    gender_encoded = self.gender_encoder.transform([user.gender])[0]
                    features.append(gender_encoded)
                except:
                    features.append(0)
            else:
                features.append(0)
                
            # 나이대 인코딩
            if user.age_group:
                try:
                    age_encoded = self.age_encoder.transform([user.age_group])[0]
                    features.append(age_encoded)
                except:
                    features.append(0)
            else:
                features.append(0)
                
            # 지역 인코딩
            if user.region:
                try:
                    region_encoded = self.region_encoder.transform([user.region])[0]
                    features.append(region_encoded)
                except:
                    features.append(0)
            else:
                features.append(0)
                
            # 선호 그룹 사이즈
            features.append(user.preferred_group_size or 4)
            
            user_features[user.id] = np.array(features)
            
        return user_features
    
    @property
    def feature_names(self):
        return self._feature_names
