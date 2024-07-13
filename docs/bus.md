# 공항 버스 서비스 흐름

### 언어 선택 (multiLanguage/choice)

- 수어 동작을 통해 사용할 언어(중국어 또는 영어)를 선택합니다.

### 상황 선택 (general/question)

- 수어 동작으로 필요한 서비스(탑승장 찾기, 버스 시간표 조회, 환불, 티켓 구매, 기타(인포메이션 데스크, 재질문 등))를 선택합니다.

### 탑승장 찾기

- 탑승장 동작 인식 시:
  1. 안내원이 플러터를 통해 /busInfo/api/boardingId 엔드포인트를 호출하여 사용자 화면을 탑승장 번호 입력 페이지(busInfo/boardingId)로 전환합니다.
  2. 사용자가 버스 번호를 입력하면, 안내원은 /busInfo/api/gate 엔드포인트를 호출하여 사용자 화면을 해당 탑승장 정보 페이지(busInfo/gate)로 전환합니다. 이 페이지에는 탑승장 위치와 안내 멘트가 표시됩니다.

### 버스 시간표 조회

- 시간표 동작 인식 시:
  1. 안내원은 /busInfo/api/scheduleNum 엔드포인트를 호출하여 사용자 화면을 버스 번호 입력 페이지(busInfo/scheduleNum)로 전환합니다.
  2. 사용자가 버스 번호를 입력하면, 안내원은 /busInfo/api/schedule 엔드포인트를 호출하여 사용자 화면을 해당 버스의 시간표 페이지(busInfo/schedule)로 전환합니다.

### 환불

- 환불 동작 인식 시:
  1. 안내원은 /refund/api/ticket 엔드포인트를 호출하여 사용자 화면을 표 요청 페이지(refund/ticket)로 전환합니다.
  2. 안내원은 /refund/api/question 엔드포인트를 호출하여 사용자 화면을 재구매 여부 및 질문 페이지(refund/question)로 전환합니다.

### 티켓 구매

- 티켓 동작 및 버스 번호 인식 시(바로 이동):
  1. 안내원은 /ticket/api/bus 엔드포인트를 호출하여 사용자 화면을 버스 정보 페이지(ticket/bus)로 전환합니다. yes or no를 입력받습니다.
  2. 안내원은 /ticket/api/schedule 엔드포인트를 호출하여 사용자 화면을 버스 시간표 선택 페이지(ticket/schedule)로 전환합니다. 번호를 입력받습니다.
  3. 안내원은 /ticket/api/cnt 엔드포인트를 호출하여 사용자 화면을 인원수 입력 페이지(ticket/cnt)로 전환합니다. 인원수를 입력받습니다.
  4. 안내원은 /ticket/api/purchase 엔드포인트를 호출하여 사용자 화면을 구매 정보 확인 페이지(ticket/purchase)로 전환합니다.

- 티켓 동작 인식 후 지역 선택:
  1. 안내원은 /ticket/api/region 엔드포인트를 호출하여 사용자 화면을 시/도 선택 페이지(ticket/region)로 전환합니다. 번호를 입력받습니다.
  2. 안내원은 /ticket/api/smallRegion 엔드포인트를 호출하여 사용자 화면을 동/읍/리 선택 페이지(ticket/smallRegion)로 전환합니다. 번호를 입력받습니다.
  3. 안내원은 /ticket/api/busStop 엔드포인트를 호출하여 사용자 화면을 버스 정류장 선택 페이지(ticket/busStop)로 전환합니다. 번호를 입력받습니다.
  4. 이후 동작은 위의 동작과 동일하게 진행합니다.

### API 명세

