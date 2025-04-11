class ModelRegistry:
    def __init__(self):
        self.models = {}
    
    def register(self, name, model):
        """추천 모델 등록"""
        self.models[name] = model
        return self  # 메서드 체이닝 지원
        
    def get_model(self, name):
        """이름으로 모델 조회"""
        return self.models.get(name)
    
    def train_all(self, features):
        """모든 등록된 모델 학습"""
        for name, model in self.models.items():
            model.train(features)
