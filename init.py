from config import get_config
from data.data_source import SQLAlchemyDataSource
from data.user_repository import UserRepository
from data.feed_repository import FeedRepository
from features.feature_registry import FeatureRegistry
from features.user_features import UserFeatureExtractor
from features.activity_features import ActivityFeatureExtractor
from models.model_registry import ModelRegistry
from models.similarity_model import SimilarityModel
from scheduler.updater import ModelUpdater

def create_recommendation_system(session_factory):
    """추천 시스템 생성 및 초기화"""
    from services.recommendation_service import RecommendationService
    import config
    
    # 세션 생성
    session = session_factory()
    data_source = SQLAlchemyDataSource(session)
    
    # Feature Registry 설정
    feature_registry = FeatureRegistry()
    feature_registry.register('activity', ActivityFeatureExtractor())
    feature_registry.register('user', UserFeatureExtractor())
    
    # Model Registry 설정
    model_registry = ModelRegistry()
    similarity_model = SimilarityModel(
        feature_weights={'activity': 1.0, 'user': 1.0}
    )
    model_registry.register('similarity', similarity_model)
    
    # Recommendation Service 생성
    recommendation_service = RecommendationService(session_factory)
    
    # Model Updater 생성 (배치 처리용)
    updater = ModelUpdater(
        data_source=data_source,
        feature_registry=feature_registry,
        model_registry=model_registry,
        recommendation_service=recommendation_service,
        config=config.DEFAULT_CONFIG
    )
    
    return {
        'recommendation_service': recommendation_service,
        'updater': updater,
        'feature_registry': feature_registry,
        'model_registry': model_registry
    }
