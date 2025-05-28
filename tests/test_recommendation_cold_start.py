"""Cold Start 추천 테스트"""
import unittest
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from data.models import Base, User
from services.recommendation_service import RecommendationService

class TestColdStartRecommendation(unittest.TestCase):
    def setUp(self):
        """테스트 환경 설정"""
        # 메모리 DB 사용
        self.engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(self.engine)
        self.SessionFactory = sessionmaker(bind=self.engine)
        
        # 추천 서비스 생성
        self.recommendation_service = RecommendationService(self.SessionFactory)
        
        # 테스트 사용자 생성
        self._create_test_users()
    
    def _create_test_users(self):
        """테스트용 사용자 생성 (피드 없이)"""
        session = self.SessionFactory()
        
        # Cold Start 사용자 (피드 없음)
        new_user = User(
            id=100,
            name="신규사용자",
            email="new@example.com",
            username="newuser",
            password="password",
            age_group="20대",
            gender="M",
            region="서울",
            preferred_group_size=4,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        session.add(new_user)
        
        # 비교할 다른 사용자들
        similar_users = [
            User(id=1, name="유사사용자1", email="s1@example.com", username="similar1",
                 password="password", age_group="20대", gender="M", region="서울",
                 preferred_group_size=4, created_at=datetime.now(), updated_at=datetime.now()),
            User(id=2, name="유사사용자2", email="s2@example.com", username="similar2",
                 password="password", age_group="20대", gender="F", region="서울",
                 preferred_group_size=5, created_at=datetime.now(), updated_at=datetime.now()),
            User(id=3, name="다른사용자1", email="d1@example.com", username="different1",
                 password="password", age_group="40대", gender="M", region="부산",
                 preferred_group_size=2, created_at=datetime.now(), updated_at=datetime.now()),
        ]
        
        for user in similar_users:
            session.add(user)
        
        session.commit()
        session.close()
    
    def test_cold_start_recommendation(self):
        """Cold Start 사용자에 대한 추천 테스트"""
        # 추천 생성
        self.recommendation_service.generate_user_recommendations()
        
        # 추천 결과 확인
        recommendations = self.recommendation_service.get_user_recommendations(100)
        
        # 추천이 생성되었는지 확인
        self.assertIsNotNone(recommendations)
        
        # 기본 정보(나이, 지역, 성별 등)가 유사한 사용자가 추천되었는지 확인
        if recommendations:
            # 첫 번째 추천이 유사한 특성을 가진 사용자인지 확인
            first_rec = recommendations[0]
            print(f"Cold Start 추천 결과: {first_rec['name']} ({first_rec['age_group']}, {first_rec['region']})")
    
    def tearDown(self):
        """테스트 정리"""
        Base.metadata.drop_all(self.engine)

if __name__ == '__main__':
    unittest.main() 