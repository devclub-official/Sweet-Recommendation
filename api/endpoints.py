from fastapi import APIRouter, Depends, HTTPException
from typing import List
from pydantic import BaseModel
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine
from data.user_repository import UserRepository
from data.recommendation_repository import RecommendationRepository
from data.data_source import SQLAlchemyDataSource


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

# 응답 스키마 정의
class UserResponse(BaseModel):
    id: int
    name: str
    username: str
    profile_image: str = None
    bio: str = None
    
    class Config:
        orm_mode = True

# 라우터 생성
router = APIRouter()


@router.get("/api/ai/recommend-mate/{user_id}", response_model=List[UserResponse])
async def recommend_mate(user_id: int,
                         user_repo: UserRepository = Depends(get_user_repository),
                         recommendation_repo: RecommendationRepository = Depends(get_recommendation_repository)):

    user = user_repo.get_user_by_id(user_id)
    # TODO: 에러 처리
    recommendations = recommendation_repo.get_recommendations_by_user_id(user_id)
    
    return recommendations


@router.get("/api/ai/recommend-team/{team_id}", response_model=List[UserResponse])
async def recommend_team(team_id: int,
                       user_repo: UserRepository = Depends(get_user_repository),
                       recommendation_repo: RecommendationRepository = Depends(get_recommendation_repository)):
    # TODO: Implement team recommendation logic
    recommendations = recommendation_repo.get_team_recommendations(team_id)
    return recommendations