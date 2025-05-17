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
