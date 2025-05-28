from fastapi import APIRouter, Depends, HTTPException
from typing import List
from pydantic import BaseModel
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine
from data.user_repository import UserRepository
from data.recommendation_repository import RecommendationRepository
from data.data_source import SQLAlchemyDataSource
from services.recommendation_service import RecommendationService


def get_session():
    engine = create_engine('sqlite:///database.db')
    session_factory = sessionmaker(bind=engine)
    session = session_factory()
    try:
        yield session
    finally:
        session.close()

def get_user_repository(session: Session = Depends(get_session)):
    data_source = SQLAlchemyDataSource(session)
    return UserRepository(data_source)

def get_recommendation_repository(session: Session = Depends(get_session)):
    data_source = SQLAlchemyDataSource(session)
    return RecommendationRepository(data_source)

def get_recommendation_service():
    engine = create_engine('sqlite:///database.db')
    session_factory = sessionmaker(bind=engine)
    return RecommendationService(session_factory)

# 응답 스키마 정의
class UserResponse(BaseModel):
    id: int
    name: str
    username: str
    profile_image: str = None
    bio: str = None
    region: str = None
    age_group: str = None
    
    class Config:
        orm_mode = True

class TeamResponse(BaseModel):
    id: int
    name: str
    description: str = None
    skill_level: int = None
    preferred_workout_type: str = None
    location: str = None
    
    class Config:
        orm_mode = True

# 라우터 생성
router = APIRouter()


@router.get("/api/ai/recommend-mate/{user_id}", response_model=List[UserResponse])
async def recommend_mate(user_id: int,
                         user_repo: UserRepository = Depends(get_user_repository),
                         recommendation_service: RecommendationService = Depends(get_recommendation_service)):
    """사용자에게 운동 메이트를 추천합니다"""
    # 사용자 존재 확인
    user = user_repo.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # 추천 결과 가져오기
    recommendations = recommendation_service.get_user_recommendations(user_id)
    
    return recommendations


@router.get("/api/ai/recommend-team/{team_id}", response_model=List[TeamResponse])
async def recommend_team(team_id: int,
                       recommendation_service: RecommendationService = Depends(get_recommendation_service)):
    """팀에게 상대 팀을 추천합니다"""
    # 추천 결과 가져오기
    recommendations = recommendation_service.get_team_recommendations(team_id)
    
    if not recommendations:
        raise HTTPException(status_code=404, detail="No recommendations found")
    
    return recommendations