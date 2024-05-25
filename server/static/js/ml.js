
    const videoElement = document.getElementById('video');
    const canvasElement = document.getElementById('output');
    const canvasCtx = canvasElement.getContext('2d');
    function sendDataToServer(data) {
      socket.send(JSON.stringify(data));
    }

    const hands = new Hands({locateFile: (file) => {
      return `https://cdn.jsdelivr.net/npm/@mediapipe/hands/${file}`;
    }});
    hands.setOptions({
      maxNumHands: 2,
      modelComplexity: 1,
      minDetectionConfidence: 0.5,
      minTrackingConfidence: 0.5
    });
    hands.onResults(onResults);

    const camera = new Camera(videoElement, {
      onFrame: async () => {
        await hands.send({image: videoElement});
      },
      width: 800,
      height: 480
    });
    camera.start();

    // WebSocket 연결 열기
    const socket = new WebSocket('ws://localhost:8000/ws/js/');

    // 메시지 이벤트 핸들러 추가
    // dicsonnect가 아니라 나중에는 해당하는 모듈로 이동시키기.
    socket.onmessage = function(event) {
        const data = JSON.parse(event.data);
        const message = data.message;
        if (message === 'disconnect') {
          // 웹소켓 연결 끊기
          socket.close();
          // 5초 후에 request_ticket 페이지로 이동
          setTimeout(function() {
              window.location.href = 'http://localhost:8000/refund/request_ticket';
          }, 1000);
          const messageElement = document.getElementById('message');
          messageElement.textContent = message;
        }
        console.log('http://localhost:8000/' + message);
        window.location.href = 'http://localhost:8000/' + message;
    };

    function onResults(results) {
      canvasCtx.save();
      canvasCtx.clearRect(0, 0, canvasElement.width, canvasElement.height);
      canvasCtx.drawImage(results.image, 0, 0, canvasElement.width, canvasElement.height);
      if (results.multiHandLandmarks) {
        for (const landmarks of results.multiHandLandmarks) {
          drawConnectors(canvasCtx, landmarks, HAND_CONNECTIONS, {color: '#00FF00', lineWidth: 5});
          drawLandmarks(canvasCtx, landmarks, {color: '#FF0000', lineWidth: 2});

          // Send hand landmarks data to Django server via WebSocket
          for (const [handId, landmarks] of results.multiHandLandmarks.entries()) {
            const handData = {
                "handId" : handId,
                "landmarks" : landmarks
            };
            const jsonString = JSON.stringify(handData);
            sendDataToServer(jsonString);
          }
        }
      }
      canvasCtx.restore();
    }
