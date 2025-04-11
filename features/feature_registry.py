class FeatureRegistry:
    def __init__(self):
        self.extractors = {}
    
    def register(self, name, extractor):
        self.extractors[name] = extractor
        
    def get_extractor(self, name):
        return self.extractors.get(name)
    
    def extract_all(self, data):
        features = {}
        for name, extractor in self.extractors.items():
            features[name] = extractor.extract(data)
        return features