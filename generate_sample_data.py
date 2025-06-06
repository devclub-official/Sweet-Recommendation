"""테스트용 샘플 데이터 생성 유틸리티"""
import random
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from data.models import Base, User, Feed, Team, TeamMembership, Recommendation, Visibility

# 샘플 데이터 정의
REGIONS = ['서울', '경기', '인천', '부산', '대구', '대전', '광주']
AGE_GROUPS = ['10대', '20대', '30대', '40대', '50대이상']
EXERCISE_TYPES = ['러닝', '헬스', '요가', '필라테스', '수영', '자전거', '등산']
EXERCISE_TIMES = ['새벽', '아침', '점심', '저녁', '심야']
GENDERS = ['M', 'F']

def generate_sample_data():
    """샘플 데이터 생성"""
    engine = create_engine('sqlite:///database.db')
    Base.metadata.create_all(engine)
    
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        # 기존 데이터 삭제 (역순으로 삭제하여 외래키 제약 방지)
        session.query(TeamMembership).delete()
        session.query(Team).delete()
        session.query(Feed).delete()
        session.query(Recommendation).delete()
        session.query(User).delete()
        session.commit()
        
        # 1. 사용자 생성 (1000명)
        users = []
        for i in range(1, 1001):
            user = User(
                id=i,
                name=f"사용자{i}",
                email=f"user{i}@example.com",
                username=f"user{i}",
                password="password",
                bio=f"안녕하세요, 사용자{i}입니다.",
                profile_image=f"profile_{i}.jpg",
                age_group=random.choice(AGE_GROUPS),
                gender=random.choice(GENDERS),
                region=random.choice(REGIONS),
                preferred_group_size=random.randint(2, 8),
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            users.append(user)
            session.add(user)
        
        # 2. 피드 생성 (각 사용자당 0~20개)
        feed_id = 1
        for user in users:
            num_feeds = random.randint(0, 20)
            for j in range(num_feeds):
                # 주 운동 종목 설정 (80% 확률로 같은 운동)
                main_exercise = random.choice(EXERCISE_TYPES)
                if random.random() < 0.8:
                    exercise_type = main_exercise
                else:
                    exercise_type = random.choice(EXERCISE_TYPES)
                
                feed = Feed(
                    id=feed_id,
                    user_id=user.id,
                    title=f"{exercise_type} 운동 완료!",
                    content=f"오늘도 {exercise_type} 운동을 열심히 했습니다.",
                    visibility=Visibility.PUBLIC,
                    image=f"feed_{feed_id}.jpg",
                    exercise_type=exercise_type,
                    exercise_time=random.choice(EXERCISE_TIMES),
                    workout_duration=random.randint(30, 120),
                    created_at=datetime.now() - timedelta(days=random.randint(0, 30)),
                    updated_at=datetime.now()
                )
                session.add(feed)
                feed_id += 1
        
        # 3. 팀 생성 (10개)
        teams = []
        for i in range(1, 11):
            team = Team(
                id=i,
                name=f"팀{i}",
                description=f"함께 운동하는 팀{i}입니다.",
                skill_level=random.randint(1, 5),
                preferred_workout_type=random.choice(EXERCISE_TYPES),
                location=random.choice(REGIONS),
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            teams.append(team)
            session.add(team)
        
        # 4. 팀 멤버십 생성 (각 팀당 3-6명)
        membership_id = 1
        assigned_users = set()
        for team in teams:
            num_members = random.randint(3, 6)
            available_users = [u for u in users if u.id not in assigned_users]
            
            if len(available_users) >= num_members:
                members = random.sample(available_users, num_members)
                
                for idx, member in enumerate(members):
                    membership = TeamMembership(
                        id=membership_id,
                        team_id=team.id,
                        user_id=member.id,
                        role='leader' if idx == 0 else 'member',
                        joined_at=datetime.now()
                    )
                    session.add(membership)
                    assigned_users.add(member.id)
                    membership_id += 1
        
        session.commit()
        print("샘플 데이터 생성 완료!")
        print(f"- 사용자: {len(users)}명")
        print(f"- 피드: {feed_id - 1}개")
        print(f"- 팀: {len(teams)}개")
        print(f"- 팀 멤버십: {membership_id - 1}개")
        
    except Exception as e:
        session.rollback()
        print(f"데이터 생성 중 오류 발생: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    generate_sample_data() 