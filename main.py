from fastapi import FastAPI
from api.endpoints import router
import uvicorn
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from init import create_recommendation_system

app = FastAPI()
app.include_router(router)

# 데이터베이스 설정
engine = create_engine('sqlite:///database.db')
SessionFactory = sessionmaker(bind=engine)

# 추천 시스템 초기화
rec_system = create_recommendation_system(SessionFactory)

# 배치 처리 시작 (스케줄러)
rec_system['updater'].start()

if __name__ == "__main__":
    try:
        # 서버 시작
        uvicorn.run(app, host="0.0.0.0", port=8000)
    finally:
        # 종료 시 스케줄러 정리
        rec_system['updater'].stop()