"""
추천 시스템 설정
"""

DEFAULT_CONFIG = {
    # 스케줄러 설정
    'schedule_config': {
        'hour': '3',  # 매일 새벽 3시에 실행
        'minute': '0'
    },
    
    # 특성 가중치 설정
    'feature_weights': {
        'user_features': 1.0,
        'activity_features': 2.0,  # 활동 특성에 더 높은 가중치
    },
    
    # 추천 전략 설정
    'strategy_config': {
        'default': 'similarity',
        'new_user': 'popular',
        'inactive_user': 'motivational'
    },
    
    # 추천 개수 설정
    'recommendation_count': 5
}

def get_config():
    """설정 로드 및 반환"""
    # 실제 구현 시 환경변수나 설정 파일에서 로드
    return DEFAULT_CONFIG
