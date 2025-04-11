import numpy as np
from collections import defaultdict
from .base_extractor import FeatureExtractor

class ActivityFeatureExtractor(FeatureExtractor):
    def __init__(self):
        self._feature_names = [
            'post_count',
            'post_frequency',
            'engagement_level'
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
        
        # 사용자별 활동 특성 계산
        activity_features = {}
        
        for user in users:
            user_id = user.id
            user_posts = user_feeds.get(user_id, [])
            
            # 게시물 수
            post_count = len(user_posts)
            
            # 게시 빈도 (최근 30일 기준)
            # 실제 구현 시 날짜 계산 로직 필요
            post_frequency = post_count / 30
            
            # 간단한 참여도 점수 (예시)
            engagement_level = post_count * 0.7 + post_frequency * 0.3
            
            # TODO: 위치 정보
            # TODO: 운동 시간대

            activity_features[user_id] = np.array([
                post_count,
                post_frequency,
                engagement_level
            ])
            
        return activity_features
    
    @property
    def feature_names(self):
        return self._feature_names
