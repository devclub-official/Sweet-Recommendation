from abc import ABC, abstractmethod

class RecommendationModel(ABC):
    @abstractmethod
    def train(self, features):
        pass
        
    @abstractmethod
    def recommend(self, user_id, count=5):
        pass

class RecommendationStrategy:
    def __init__(self, strategy_config, model_registry):
        self.strategy_config = strategy_config
        self.model_registry = model_registry
        
    def get_recommendations(self, user_id, user_context=None):
        strategy_name = self._determine_strategy(user_id, user_context)
        model = self.model_registry.get_model(strategy_name)
        return model.recommend(user_id)
        
    def _determine_strategy(self, user_id, user_context):
        # 사용자 상황에 맞는 전략 결정 로직
        # 초보자, 중급자, 고급자 등 상황별 전략
        pass