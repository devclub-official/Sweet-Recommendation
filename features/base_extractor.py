# features/base_extractor.py
from abc import ABC, abstractmethod

class FeatureExtractor(ABC):
    @abstractmethod
    def extract(self, data):
        pass
    
    @property
    def feature_names(self):
        pass

