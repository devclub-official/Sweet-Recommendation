### FitMate Cold Start 해결을 위한 온보딩 설계 요구사항
#### 배경
- 신규 사용자는 활동 데이터(피드)가 없어 추천 시스템이 적절한 운동 메이트를 찾기 어렵기 때문에, 가입 시 필수 정보를 수집하여 초기 추천을 제공해야 함.
#### 필수 수집 정보 (온보딩 설문)
1. 기본 정보
- 나이대 (필수)
선택지: 10대 / 20대 / 30대 / 40대 / 50대 이상  
이유: 비슷한 나이대끼리 운동하는 것을 선호  
성별 (필수)  
- 선택지: 남성 / 여성
이유: 성별 다양성을 고려한 팀 구성. 성별은 다양할 수록 좋을수도?
활동 지역 (필수)
- 선택지: 서울 / 경기 / 인천 / 부산 / 대구 / 대전 / 광주 / 제주
이유: 오프라인 모임을 위한 지역 매칭  
2. 운동 선호도
- 선호하는 운동 종목 (필수, 복수 선택 가능)
선택지: 러닝 / 헬스 / 요가 / 필라테스 / 수영 / 자전거 / 등산  
이유: 같은 운동을 즐기는 사람끼리 매칭  
- 주로 운동하는 시간대 (필수)
선택지: 새벽(5-7시) / 아침(7-9시) / 점심(11-14시) / 저녁(17-20시) / 심야(20시 이후)  
이유: 비슷한 시간대에 운동하는 사람끼리 매칭  
- 평균 운동 시간 (필수)
선택지: 30분 미만 / 30분-1시간 / 1-2시간 / 2시간 이상  
이유: 운동 강도와 지속성이 비슷한 사람끼리 매칭  
3. 그룹 선호도
선호하는 운동 그룹 인원 (필수)  
선택지: 2-3명 / 4-5명 / 6-8명 / 8명 이상  
이유: 적절한 그룹 사이즈 매칭  
#### UX/UI 제안사항
1. 단계별 온보딩
- 진행률 표시 (Progress Bar)
2. 스킵 불가 설계
- 필수/옵션 항목 구분 필요
- "나중에 하기" 옵션 - 추천을 받기 위해서는 설문을 진행해야함.
- 완료하지 않으면 서비스 이용 불가

#### 추가 고려사항
- 프로필 수정
- 언제든지 온보딩 정보 수정 가능
- 수정 시 추천 결과 즉시 업데이트

#### 선택적 추가 정보
- 운동 목표 (다이어트/근력증가/건강유지 등)
- 운동 경력
- 선호하는 운동 파트너 성향

#### 개발 참고사항
- 수집된 정보는 User 테이블의 다음 필드에 저장됩니다: age_group, gender, region, preferred_group_size
- 운동 선호도는 첫 피드 작성 유도를 통해 Feed 테이블에 저장
- Cold Start 사용자도 기본 정보만으로 추천 가능하도록 구현 완료