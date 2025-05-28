# FitMate-AI 추천 시스템 구현 가이드

## 구현 완료 사항

### 1. 데이터 모델 확장
- **User 모델**: age_group, gender, region, preferred_group_size 필드 추가
- **Feed 모델**: exercise_type, exercise_time, workout_duration 필드 추가
- **Recommendation 모델**: 추천 결과 저장용 테이블

### 2. Feature Extractor 구현
#### UserFeatureExtractor
- 성별, 나이대, 지역, 선호 그룹 사이즈를 feature로 추출
- LabelEncoder를 사용한 범주형 데이터 인코딩

#### ActivityFeatureExtractor
- engagement_level: 피드 개수 기반 (low/mid/high)
- prime_exercise_time: 가장 많이 운동한 시간대
- main_exercise_type: 가장 많이 한 운동 종류
- avg_workout_duration: 평균 운동 시간
- exercise_diversity: 운동 종류의 다양성

### 3. 추천 모델 (SimilarityModel)
- 유사도 기반 추천 (코사인 유사도)
- 유사성과 보완성을 모두 고려
  - 유사할수록 좋은 feature: 운동 종류, 시간대, 지역, 나이대 등
  - 다양성이 있으면 좋은 feature: 성별, engagement_level
- 매칭 히스토리 기반 중복 추천 방지

### 4. RecommendationService
- 사용자 추천 생성 및 DB 저장
- 팀 추천 생성 및 DB 저장
- 추천 결과 조회

### 5. API 엔드포인트
- `/api/ai/recommend-mate/{user_id}`: 운동 메이트 추천
- `/api/ai/recommend-team/{team_id}`: 상대 팀 추천

### 6. 배치 처리 (Scheduler)
- 매일 새벽 3시: 모델 재학습
- 매일 새벽 4시: 추천 결과 생성 및 DB 저장

## 사용 방법

### 1. 의존성 설치
```bash
pip install -r requirements.txt
```

### 2. 샘플 데이터 생성
```bash
python utils/data_generator.py
```

### 3. 서버 실행
```bash
python main.py
```

### 4. 추천 API 호출
```bash
# 사용자 추천
GET http://localhost:8000/api/ai/recommend-mate/1

# 팀 추천
GET http://localhost:8000/api/ai/recommend-team/1
```

## Cold Start 처리
신규 사용자의 경우 기본 정보(나이대, 성별, 지역, 선호 그룹 사이즈)만으로도 추천이 가능합니다.

## 추천 점수 계산 방식
1. 기본 코사인 유사도: 70%
2. 보완성 점수: 30%
   - 성별이 다르면 가산점
   - engagement_level이 다르면 가산점

## 향후 개선 사항
1. 매칭 히스토리 테이블 구현
2. 온라인 지표 수집 및 A/B 테스트
3. 실시간 추천 옵션
4. 추천 결과 캐싱
5. 더 정교한 feature engineering 