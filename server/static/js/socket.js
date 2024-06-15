    var currentUrl = window.location.href;
// WebSocket 연결 열기
    let socket = new WebSocket('ws://localhost:8000/ws/js?origin=' + currentUrl);

    // 메시지 이벤트 핸들러 추가
    // dicsonnect가 아니라 나중에는 해당하는 모듈로 이동시키기.
    socket.onmessage = function(event) {
        const data = JSON.parse(event.data);
        const type = data.message_type;
        const message = data.message;

        if(type === 'recognized_actions'){
            const detectActionElement = document.querySelector('.detect_action');
            detectActionElement.textContent = message;
            detectActionElement.classList.add('text-xs');
        }
        if(type === 'url_move') {
            socket.send(JSON.stringify({
                    handId: 'disconnect',
                    message: 'disconnect'
            }));
            socket.close();
            setTimeout(function() {
                window.location.href = 'http://localhost:8000/' + message;}, 1500);
        }
        if(type === 'add_message'){
            const addMessage = document.querySelector('.new-message');
            addMessage.textContent = message;
            addMessage.classList.add('text-xs');
        }
    };