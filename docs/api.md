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
- **[GET] /api/schedule**
- **[GET] /api/gate**
- **[GET] /api/boarding-id**

요청이 성공적으로 처리되면 200 상태 코드를 반환한다.

### 티켓

티켓 구매 API(/ticket)

- **[GET] /api/region**
  - 지역 요청(대도시)

Response: 서버는 요청에 대해 현재 선택한 도시 정보를 반환하고 페이지 이동 메시지를 전송한다.

Example:

```json
{
  "region": "서울시"
}
```

- **[GET] /api/small-region**
  - 지역 요청(소도시) 

Response: 서버는 요청에 대해 현재 선택한 도시 정보를 반환하고 페이지 이동 메시지를 전송한다.

Example:

```json
{
  "small_region": "강남구"
}
```

- **[GET] /api/bus-stop**
  - 버스 정류장 요청

Response: 서버는 요청에 대해 현재 선택한 정류장 정보를 반환하고 페이지 이동 메시지를 전송한다.

Example:

```json
{
  "bus_stop": "강남역"
}
```

- **[GET] /api/bus**
  - 선택한 버스 요청
- **[GET] /api/schedule**
  - 버스 시간표 요청
- **[POST] /api/cnt**
  - 인원수 선택 요청 
- **[POST] /api/purchase**
  - 티켓 구매 요청 

### 일반(질문, 정보 데스크, 초기 화면)

화면 전환 요청 API(/general)

- **[GET] /api/question**
- **[GET] /api/info-desk**
- **[GET] /api/initial**
- **[GET] /api/re-question**

Response: 요청이 성공적으로 처리되면 200 상태 코드를 반환한다.

### 언어

언어 선택 API(/multiLanguage)

- **[GET] /api/language**

Response: 서버는 요청에 대해 현재 서버의 LANGUAGE_CODE 설정을 반환하고 페이지 이동 메시지를 전송한다.

Example:

```json
{
  "id": "en-us"
}
```

### 환불

환불 요청 API(/refund)

- **[GET] /api/ticket**
- **[POST] /api/refund**

Response: 요청이 성공적으로 처리되면 200 상태 코드를 반환한다.

### Websocket

창구 직원용(/flutter), Mediapipe 클라이언트와의 양방향 통신을 위한 API(/ws)

- **/ws/js**
- **/ws/flutter**