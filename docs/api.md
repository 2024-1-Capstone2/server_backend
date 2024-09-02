# API

- **데이터 포맷:** JSON, HTML
- **프로토콜:** RESTful API, HTTP, WebSocket

## API 목록

- **버스 정보**
- **티켓**
- **환불**
- **언어 선택**
- **동작 인식**
- **WebSocket**
- **일반**

## API 상세

### 버스 정보

화면 전환 요청 API(/bus)

- **[GET] /api/schedule-num**
  - ![스크린샷 2024-09-02 142712](https://github.com/user-attachments/assets/3ed03041-7eb6-48c7-85c8-c1744b336bf9)

- **[GET] /api/schedule**
  - ![스크린샷 2024-09-02 142610](https://github.com/user-attachments/assets/63b5ecc5-d1b2-47c0-90e8-fad6137b5cf3)

- **[GET] /api/gate**
  - ![스크린샷 2024-09-02 142531](https://github.com/user-attachments/assets/0ed8df5d-6a46-4707-9f2e-71a967428f54)

- **[GET] /api/boarding-id**
  - ![스크린샷 2024-09-02 142321](https://github.com/user-attachments/assets/a7ff42fb-8ebf-43a3-ba29-4fa06d7b180c)

### 티켓

티켓 구매 API(/ticket)

- **[GET] /api/region**
  - 지역(대도시)
  - ![스크린샷 2024-09-02 150710](https://github.com/user-attachments/assets/0e1a6387-66b8-469b-8b5b-3ab77f913d5d)

- **[GET] /api/small-region**
  - 지역(소도시)
  - ![스크린샷 2024-09-02 150722](https://github.com/user-attachments/assets/7d1f1d7c-11a8-4840-813f-c7399ad0d64f)

- **[GET] /api/bus-stop**
  - 버스 정류장
  - ![스크린샷 2024-09-02 150732](https://github.com/user-attachments/assets/3e56b531-05f2-4793-8532-19ec7a0950c4)

- **[GET] /api/bus**
  - 선택한 버스 정보
  - ![스크린샷 2024-09-02 150746](https://github.com/user-attachments/assets/82c2d70e-bd61-455d-b902-d977f7e1af25)

- **[GET] /api/schedule**
  - 버스 시간표
  - ![스크린샷 2024-09-02 150756](https://github.com/user-attachments/assets/026ac521-c593-4e72-b5d5-0e7cd39f9810)

- **[GET] /api/cnt**
  - 인원수 정보
  - ![스크린샷 2024-09-02 150807](https://github.com/user-attachments/assets/5e64bded-e230-48d6-b10c-f292182d0454)

- **[GET] /api/purchase**
  - 티켓 구매 요청 

### 일반(질문, 정보 데스크, 초기 화면)

화면 전환 요청 API(/general)

- **[GET] /api/question**
  - ![스크린샷 2024-09-02 143352](https://github.com/user-attachments/assets/5c646843-3492-4d67-88ed-8bd8b5cc35b6)

- **[GET] /api/info-desk**
  - ![스크린샷 2024-09-02 143515](https://github.com/user-attachments/assets/ee4b0114-bac6-414e-af96-b1b7dc68c4b3)

- **[GET] /api/initial**
  - Response: 요청이 성공적으로 처리되면 200 상태 코드를 반환한다.

- **[GET] /api/re-question**
  - ![스크린샷 2024-09-02 143503](https://github.com/user-attachments/assets/6f087ba5-e338-4a28-924b-8d38fa9cf8bf)

### 언어

언어 선택 API(/multiLanguage)

- **[GET] /api/language**
  - ![스크린샷 2024-09-02 143731](https://github.com/user-attachments/assets/b1528189-bcbd-4737-8120-b5b909350dfe)

Response: 서버는 요청에 대해 현재 서버의 LANGUAGE_CODE 설정을 반환하고 페이지 이동 메시지를 전송한다.

### 환불

환불 요청 API(/refund)

- **[GET] /api/question**
  - ![스크린샷 2024-09-02 144140](https://github.com/user-attachments/assets/fd8d0418-8b45-47ac-99b5-54af8403e180)

- **[GET] /api/ticket**
  - ![스크린샷 2024-09-02 144152](https://github.com/user-attachments/assets/c2658160-5695-4bec-983e-006ec7131a32)


Response: 요청이 성공적으로 처리되면 200 상태 코드를 반환한다.

### Websocket

창구 직원용(/flutter), Mediapipe 클라이언트와의 양방향 통신을 위한 API(/ws)

- **/ws/js**
- **/ws/flutter**
