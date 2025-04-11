from .config import get_config
from .data.data_source import SQLAlchemyDataSource
from .data.user_repository import UserRepository
from .data.feed_repository import FeedRepository
from .features.feature_registry import FeatureRegistry
from .features.user_features import UserFeatureExtractor
from .features.activity_features import ActivityFeatureExtractor
from .models.model_registry import ModelRegistry
from .models.similarity_model import SimilarityModel
from .scheduler.updater import ModelUpdater

def create_recommendation_system(session_factory):
    config = get_config()
    
    # 데이터 소스 초기화
    data_source = SQLAlchemyDataSource(session_factory)
    
    # 리포지토리 초기화
    user_repo = UserRepository(data_source)
    feed_repo = FeedRepository(data_source)
    
    # 특성 추출기 등록
    feature_registry = FeatureRegistry()
    feature_registry.register('user_features', UserFeatureExtractor())
    feature_registry.register('activity_features', ActivityFeatureExtractor())
    
    # 모델 등록
    model_registry = ModelRegistry()
    model_registry.register(
        'similarity',
        SimilarityModel(feature_weights=config.get('feature_weights'))
    )
    
    # 모델 업데이터 생성
    updater = ModelUpdater(
        data_source=data_source,
        feature_registry=feature_registry,
        model_registry=model_registry,
        config=config
    )
    
    return {
        'user_repository': user_repo,
        'feed_repository': feed_repo,
        'feature_registry': feature_registry,
        'model_registry': model_registry,
        'updater': updater
    }
