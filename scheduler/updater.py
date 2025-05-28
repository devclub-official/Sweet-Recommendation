from apscheduler.schedulers.background import BackgroundScheduler
from features.feature_registry import FeatureRegistry
from models.model_registry import ModelRegistry
from data.data_source import DataSource
from data.models import User, Feed
from services.recommendation_service import RecommendationService

class ModelUpdater:
    def __init__(
        self,
        data_source: DataSource,
        feature_registry: FeatureRegistry,
        model_registry: ModelRegistry,
        recommendation_service: RecommendationService,
        config
    ):
        self.data_source = data_source
        self.feature_registry = feature_registry
        self.model_registry = model_registry
        self.recommendation_service = recommendation_service
        self.config = config
        self.scheduler = BackgroundScheduler()
        
    def start(self):
        # 모델 업데이트 작업 스케줄링
        self.scheduler.add_job(
            self.update_models,
            'cron',
            **self.config.get('schedule_config', {'hour': '3'})
        )
        
        # 추천 생성 작업 스케줄링 (매일 새벽 4시)
        self.scheduler.add_job(
            self.generate_recommendations,
            'cron',
            hour=4,
            minute=0
        )
        
        self.scheduler.start()
        
    def update_models(self):
        """모델 재학습"""
        # 데이터 로드
        user_data = self.data_source.get_data(lambda s: s.query(User).all())
        feed_data = self.data_source.get_data(lambda s: s.query(Feed).all())
        
        # 특성 추출
        features = self.feature_registry.extract_all({
            'users': user_data,
            'feeds': feed_data
        })
        
        # 모델 재학습
        for model_name, model in self.model_registry.models.items():
            model.train(features)
    
    def generate_recommendations(self):
        """추천 생성 및 DB 저장"""
        try:
            print("Starting recommendation generation...")
            
            # 사용자 추천 생성
            self.recommendation_service.generate_user_recommendations()
            
            # 팀 추천 생성
            self.recommendation_service.generate_team_recommendations()
            
            print("Recommendation generation completed successfully")
        except Exception as e:
            print(f"Error generating recommendations: {e}")
    
    def stop(self):
        """스케줄러 중지"""
        if self.scheduler.running:
            self.scheduler.shutdown()
