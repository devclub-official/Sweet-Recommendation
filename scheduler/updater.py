from apscheduler.schedulers.background import BackgroundScheduler
from ..features.feature_registry import FeatureRegistry
from ..models.model_registry import ModelRegistry
from ..data.data_source import DataSource
from ..data.models import User, Feed

class ModelUpdater:
    def __init__(
        self,
        data_source: DataSource,
        feature_registry: FeatureRegistry,
        model_registry: ModelRegistry,
        config
    ):
        self.data_source = data_source
        self.feature_registry = feature_registry
        self.model_registry = model_registry
        self.config = config
        self.scheduler = BackgroundScheduler()
        
    def start(self):
        self.scheduler.add_job(
            self.update_models,
            'cron',
            **self.config.get('schedule_config', {'hour': '3'})
        )
        self.scheduler.start()
        
    def update_models(self):
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
