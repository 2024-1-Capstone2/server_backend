    var currentUrl = window.location.href;
// WebSocket 연결 열기
    const socket = new WebSocket('ws://localhost:8000/ws/js?origin=' + currentUrl);

    // 메시지 이벤트 핸들러 추가
    // dicsonnect가 아니라 나중에는 해당하는 모듈로 이동시키기.
    socket.onmessage = function(event) {
        const data = JSON.parse(event.data);
        const type = data.message_type;
        const message = data.message;

        console.log(message);

        if(type === 'recognized_actions'){
            const detectActionElement = document.querySelector('.detect_action');
            detectActionElement.textContent = message;
            detectActionElement.classList.add('text-sm');
        }
        if(type === 'url_move') {
            window.location.href = 'http://localhost:8000/' + message;
        }
        if(type === 'add_message'){
            if(currentUrl === 'http://localhost:8000/busInfo/question' || currentUrl === 'http://localhost:8000/busInfo/reQuestion'){
                addMessageToQuestion(message);
            }
            if(currentUrl === 'http://localhost:8000/busInfo/informationDesk'){
                addMessageInfoDesk(message);
            }
            if(currentUrl === 'http://localhost:8000/busInfo/busSchedule'){
                addMessageToBusSchedule(message);
            }
            if(currentUrl === 'http://localhost:8000/busInfo/busGuide'){
                addMessageToBusGuide(message);
            }
            if(currentUrl === 'http://localhost:8000/busInfo/busBoarding'){
                addMessageToBusBoarding(message);
            }
            if(currentUrl === 'http://localhost:8000/refund/'){
                addMessageToRefundTicket(message);
            }
            if(currentUrl === 'http://localhost:8000/refund/question'){
                addMessageToRefundQuestion(message);
            }
            if(currentUrl === 'http://localhost:8000/ticket/selectRegion'){
                addMessageToRegion(message);
            }
        }
        // if (message === 'disconnect') {
        //   // 웹소켓 연결 끊기
        //   socket.close();
        //   // 5초 후에 request_ticket 페이지로 이동
        //   setTimeout(function() {
        //       window.location.href = 'http://localhost:8000/refund/request_ticket';
        //   }, 1000);
        //   const messageElement = document.getElementById('message');
        //   messageElement.textContent = message;
        // }
    };