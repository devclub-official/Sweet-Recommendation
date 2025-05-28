import numpy as np
from collections import defaultdict, Counter
from datetime import datetime, timedelta
from sklearn.preprocessing import LabelEncoder
from .base_extractor import FeatureExtractor

class ActivityFeatureExtractor(FeatureExtractor):
    def __init__(self):
        self.exercise_type_encoder = LabelEncoder()
        self.exercise_time_encoder = LabelEncoder()
        self._feature_names = [
            'engagement_level',
            'prime_exercise_time_encoded',
            'main_exercise_type_encoded',
            'avg_workout_duration',
            'exercise_diversity'
        ]
        
    def extract(self, data):
        """활동 데이터에서 사용자별 활동 특성 추출"""
        users = data.get('users', [])
        feeds = data.get('feeds', [])
        
        if not users or not feeds:
            return {}
            
        # 사용자별 피드 그룹화
        user_feeds = defaultdict(list)
        for feed in feeds:
            user_feeds[feed.user_id].append(feed)
        
        # 모든 운동 종류와 시간대 수집 (인코더 학습용)
        all_exercise_types = [f.exercise_type for f in feeds if f.exercise_type]
        all_exercise_times = [f.exercise_time for f in feeds if f.exercise_time]
        
        if all_exercise_types:
            self.exercise_type_encoder.fit(all_exercise_types)
        if all_exercise_times:
            self.exercise_time_encoder.fit(all_exercise_times)
        
        # 사용자별 활동 특성 계산
        activity_features = {}
        
        for user in users:
            user_id = user.id
            user_posts = user_feeds.get(user_id, [])
            
            # 1. engagement_level (피드 총 개수 기반)
            post_count = len(user_posts)
            if post_count <= 5:
                engagement_level = 1  # low
            elif post_count <= 15:
                engagement_level = 2  # mid
            else:
                engagement_level = 3  # high
            
            # 2. prime_exercise_time (가장 많이 운동한 시간대)
            exercise_times = [f.exercise_time for f in user_posts if f.exercise_time]
            if exercise_times:
                time_counter = Counter(exercise_times)
                prime_time = time_counter.most_common(1)[0][0]
                try:
                    prime_time_encoded = self.exercise_time_encoder.transform([prime_time])[0]
                except:
                    prime_time_encoded = 0
            else:
                prime_time_encoded = 0
            
            # 3. main_exercise_type (가장 많이 한 운동 종류)
            exercise_types = [f.exercise_type for f in user_posts if f.exercise_type]
            if exercise_types:
                type_counter = Counter(exercise_types)
                main_type = type_counter.most_common(1)[0][0]
                try:
                    main_type_encoded = self.exercise_type_encoder.transform([main_type])[0]
                except:
                    main_type_encoded = 0
            else:
                main_type_encoded = 0
            
            # 4. avg_workout_duration (평균 운동 시간)
            durations = [f.workout_duration for f in user_posts if f.workout_duration]
            avg_duration = np.mean(durations) if durations else 60  # 기본값 60분
            
            # 5. exercise_diversity (운동 종류의 다양성)
            unique_types = len(set(exercise_types)) if exercise_types else 0
            exercise_diversity = min(unique_types / 5, 1.0)  # 0~1 사이로 정규화

            activity_features[user_id] = np.array([
                engagement_level,
                prime_time_encoded,
                main_type_encoded,
                avg_duration,
                exercise_diversity
            ])
            
        return activity_features
    
    @property
    def feature_names(self):
        return self._feature_names
