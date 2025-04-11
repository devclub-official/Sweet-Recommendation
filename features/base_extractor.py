from abc import ABC, abstractmethod

class Recommender(ABC):
    
    @abstractmethod
    def preprocess(self, dataframe):
        pass
    
    @abstractmethod
    def infer(self, user_id: int):
        pass

    
