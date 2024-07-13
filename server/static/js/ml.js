import {
    HandLandmarker,
    FilesetResolver
} from "https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@0.10.0";


let handLandmarker = undefined;
let runningMode = "IMAGE";
let webcamRunning = false;


const video = document.getElementById('webcam');
const canvasElement = document.getElementById('output_canvas');
const canvasCtx = canvasElement.getContext('2d');


// HandLandmarker 클래스를 초기화합니다.
const createHandLandmarker = async () => {
    const vision = await FilesetResolver.forVisionTasks(
        "https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@0.10.0/wasm"
    );
    handLandmarker = await HandLandmarker.createFromOptions(vision, {
        baseOptions: {
            modelAssetPath: `https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task`,
            delegate: "GPU"
        },
        runningMode: runningMode,
        numHands: 2
    });
    startWebcam(); // 페이지가 열리면 비디오 자동 시작
};
createHandLandmarker();

// 웹캠이 지원되는지 확인합니다.
const hasGetUserMedia = () => !!navigator.mediaDevices?.getUserMedia;

// 웹캠을 활성화하고 스트림을 시작하는 함수입니다.
const startWebcam = () => {
    if (!handLandmarker) {
        console.log("Wait! HandLandmarker not loaded yet.");
        return;
    }

    webcamRunning = true;

    // getUsermedia 파라미터.
    const constraints = {
        video: true
    };

    // 웹캠 스트림을 활성화합니다.
    navigator.mediaDevices.getUserMedia(constraints).then((stream) => {
        video.srcObject = stream;
        video.addEventListener("loadeddata", predictWebcam);
    });
};

let lastVideoTime = -1;
let results = undefined;
let count = 1;

// 웹캠 스트림에서 이미지를 연속적으로 가져와서 감지하는 함수입니다.
async function predictWebcam() {
    canvasElement.style.width = video.videoWidth + 'px';
    canvasElement.style.height = video.videoHeight + 'px';
    canvasElement.width = video.videoWidth;
    canvasElement.height = video.videoHeight;

    // 스트림 감지를 시작합니다.
    if (runningMode === "IMAGE") {
        runningMode = "VIDEO";
        await handLandmarker.setOptions({ runningMode: "VIDEO" });
    }
    let startTimeMs = performance.now();
    if (lastVideoTime !== video.currentTime) {
        lastVideoTime = video.currentTime;
        results = handLandmarker.detectForVideo(video, startTimeMs);
    }
    canvasCtx.save();
    canvasCtx.clearRect(0, 0, canvasElement.width, canvasElement.height);
    if (results.landmarks) {
        // 손 랜드마크 데이터를 정제하여 서버로 전송
        if(results.landmarks.length > 0) {
            sendHandData(results.landmarks);
        }

        for (const landmarks of results.landmarks) {

            drawConnectors(canvasCtx, landmarks, HAND_CONNECTIONS, {
                color: "#00FF00",
                lineWidth: 5
            });
            drawLandmarks(canvasCtx, landmarks, { color: "#FF0000", lineWidth: 2 });
        }
    }

    canvasCtx.restore();

    // 브라우저가 준비되면 이 함수를 다시 호출하여 예측을 계속합니다.
    if (webcamRunning === true) {
        window.requestAnimationFrame(predictWebcam);
    }
}


// 이미지 클릭 시 감지하는 코드 (변경 없음)
const imageContainers = document.getElementsByClassName("detectOnClick");
for (let i = 0; i < imageContainers.length; i++) {
    imageContainers[i].children[0].addEventListener("click", handleClick);
}

async function handleClick(event) {
    if (!handLandmarker) {
        console.log("Wait for handLandmarker to load before clicking!");
        return;
    }

    if (runningMode === "VIDEO") {
        runningMode = "IMAGE";
        await handLandmarker.setOptions({ runningMode: "IMAGE" });
    }

    const allCanvas = event.target.parentNode.getElementsByClassName("canvas");
    for (var i = allCanvas.length - 1; i >= 0; i--) {
        const n = allCanvas[i];
        n.parentNode.removeChild(n);
    }

    const handLandmarkerResult = handLandmarker.detect(event.target);
    console.log(handLandmarkerResult.handednesses[0][0]);
    const canvas = document.createElement("canvas");
    canvas.setAttribute("class", "canvas");
    canvas.setAttribute("width", event.target.naturalWidth + "px");
    canvas.setAttribute("height", event.target.naturalHeight + "px");
    canvas.style =
        "left: 0px;" +
        "top: 0px;" +
        "width: " +
        event.target.width +
        "px;" +
        "height: " +
        event.target.height +
        "px;";

    event.target.parentNode.appendChild(canvas);
    const cxt = canvas.getContext("2d");
    for (const landmarks of handLandmarkerResult.landmarks) {
        drawConnectors(cxt, landmarks, HAND_CONNECTIONS, {
            color: "#00FF00",
            lineWidth: 5
        });
        drawLandmarks(cxt, landmarks, { color: "#FF0000", lineWidth: 1 });
    }
}

    // 데이터 버퍼와 타이머 변수를 추가합니다.
let dataBuffer = [];
let sendInterval = 50; // 100ms마다 데이터를 보냅니다.
let lastSendTime = 0;
let isProcessing = false; // 데이터 처리 중 여부를 나타내는 플래그

 // sendHandData 함수를 수정합니다.
function sendHandData(landmarkData) {
    const currentTime = Date.now();
    dataBuffer.push({
        timestamp: currentTime,
        landmarks: landmarkData
    });

    // 버퍼가 30개 이상 쌓이거나, 마지막 전송 후 100ms가 지났을 때 데이터를 전송합니다. dataBuffer.length >= 30 ||
    if ((currentTime - lastSendTime >= sendInterval && dataBuffer.length > 0)) {
        if (!isProcessing) {
            isProcessing = true;
            const dataToSend = [...dataBuffer];
            dataBuffer = [];
            lastSendTime = currentTime;

            fetch('/handML/api/hand-data', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(dataToSend)
            })
                .then(response => response.json())
                .then(data => {
                    isProcessing = false;
                })
                .catch((error) => {
                    isProcessing = false;
                });
        }
    }
}