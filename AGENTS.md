## Purpose
- 사용자의 운동 피드 정보와 개인 정보를 기반으로 함께 운동하기 적합한 팀원들을 추천해주는 시스템, 그리고 팀별로 수준이 비슷한 상대팀을 매칭해주는 추천 시스템 개발.
- 운동 피드 정보에 담긴 내용은 engagement_level, prime_exercise_time_encoded, main_exercise_type_encoded, avg_workout_duration, exercise_diversity
- 개인 정보에 담긴 내용은 gender_encoded, age_group_encoded, region_encoded, preferred_group_size

## System Architecture
### Endpoint
- `/api/ai/recommend-mate/{user_id}`: 백엔드에서 사용자 id를 받으면, 미리 저장해둔 추천 목록(다른 user id)을 리턴
- `/api/ai/recommend-team/{team_id}`: 백엔드에서 팀 id를 받으면, 미리 저장해둔 추천 목록(다른 팀 id)을 리턴

### 추천 모델 동작 방식
- scheduler를 통해 주기적으로 데이터 학습 및 추천 업데이트 후 DB 저장. 기존에 매칭되었던 사용자일 경우 중복 제외될 수 있도록 처리 필요. Endpoint에서는 저장되어있는 DB에서 읽어오는 역할만 수행.

## 폴더 구조
### api
- 엔드포인트 정리 ( `/api/ai/recommend-mate/{user_id}`, `/api/ai/recommend-team/{team_id}`)
### data
- DB ORM 관련 코드
### features
- 추천 모델에 사용할 데이터 피쳐. user와 feed 정보로 나뉨.
### models
- 추천 모델
### scheduler
- 크론잡 정의. 추천 목록 및 데이터 피쳐 업데이트.

