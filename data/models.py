from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
import enum

# Read Only
Base = declarative_base()

class Visibility(enum.Enum):
    PUBLIC = "public"
    PRIVATE = "private"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    username = Column(String)
    password = Column(String)
    bio = Column(String)
    profile_image = Column(String)
    # TODO: age
    # TODO: gender
    # TODO: favorite_workout_type
    age_group = Column(String)  # '10대', '20대', '30대', '40대', '50대이상'
    gender = Column(String)  # 'M', 'F'
    region = Column(String)  # '서울', '경기', '인천', '부산' 등
    preferred_group_size = Column(Integer)  # 선호하는 운동 그룹 인원수

    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class Feed(Base):
    __tablename__ = "feeds"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    title = Column(String)
    content = Column(String)
    visibility = Column(Enum(Visibility))
    image = Column(String)
    exercise_type = Column(String)  # '러닝', '헬스', '요가', '필라테스', '수영' 등
    exercise_time = Column(String)  # '새벽', '아침', '점심', '저녁', '심야'
    workout_duration = Column(Integer)  # 운동 시간(분)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    # TODO: location


# Team 모델
class Team(Base):
    __tablename__ = "teams"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    skill_level = Column(Integer)  # 팀 실력 수준
    preferred_workout_type = Column(String)
    location = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


# TeamMembership 모델
class TeamMembership(Base):
    __tablename__ = "team_memberships"
    id = Column(Integer, primary_key=True)
    team_id = Column(Integer, ForeignKey('teams.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    role = Column(String)  # e.g., 'leader', 'member'
    joined_at = Column(DateTime)


# MatchHistory 모델
class MatchHistory(Base):
    __tablename__ = "match_histories"
    id = Column(Integer, primary_key=True)
    team1_id = Column(Integer, ForeignKey('teams.id'))
    team2_id = Column(Integer, ForeignKey('teams.id'))
    status = Column(String)  # 'pending', 'accepted', 'rejected', 'completed'
    match_date = Column(DateTime)
    created_at = Column(DateTime)


# Recommendation 모델
class Recommendation(Base):
    __tablename__ = "recommendations"
    id = Column(Integer, primary_key=True)
    source_id = Column(Integer)  # user_id 또는 team_id
    target_id = Column(Integer)  # 추천된 user_id 또는 team_id
    type = Column(String)  # 'user' 또는 'team'
    score = Column(Float)
    created_at = Column(DateTime)
