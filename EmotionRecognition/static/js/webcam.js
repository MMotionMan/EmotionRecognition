let imageCapture;
let xhr = new XMLHttpRequest();
const url = 'http://localhost:8080/get_first_mode_result/';
const url_mode = "http://localhost:8080/send_mode/";
const url_frame = "http://localhost:8080/set_next_frame/";
const url_frame_get = "http://localhost:8080/get_next_emotion/";



(function() {
    let video = null;
    let click_button = null;
    let canvas = null;
    let mediaDevice = null;
    let webcam_stream = null
    let mode = -1;

    let emotions = new Map();
    emotions.set("none", "None");
    emotions.set("angry", "Angry");
    emotions.set("disgust", "Disgust");
    emotions.set("fear", "Fear");
    emotions.set("happy", "Happy");
    emotions.set("sad", "Sad");
    emotions.set("surprise", "Surprise");
    emotions.set("noface", "NoFace");

    let smile_emotions_codes = new Map();
    smile_emotions_codes.set("none", "&#x1F921");
    smile_emotions_codes.set("angry", "&#x1F621");
    smile_emotions_codes.set("disgust", "&#x1F922");
    smile_emotions_codes.set("fear", "&#x1F628");
    smile_emotions_codes.set("happy", "&#x1F642");
    smile_emotions_codes.set("sad", "&#x1F622");
    smile_emotions_codes.set("surprise", "&#x1F626");
    smile_emotions_codes.set("noface", "&#x1F636");



    function turnOnWebcam() {
        mediaDevice = navigator.mediaDevices.getUserMedia({video: true, audio: false});
        mediaDevice.then(function(stream) {
            video.srcObject = stream;
            webcam_stream = stream
            video.width = 800;
            video.height = 300;
            video.play();

            const track = stream.getVideoTracks()[0];
            imageCapture = new ImageCapture(track);
        })
            .catch(function(err) {
                console.log("An error occurred: " + err);
            });
    }

    function startup() {
        video = document.getElementById('video');
        click_button = document.querySelector("#click-photo");
        canvas = document.querySelector("#canvas");

        document.getElementById("mode1").addEventListener("click", function () {
            mode = 1;
        })
        document.getElementById("mode21").addEventListener("click", function () {
            mode = 21;
            turnOnWebcam();
        })
        document.getElementById("mode22").addEventListener("click", function () {
            mode = 22
            webcam_stream.getTracks().forEach(function(track) {
                track.stop();
            });
        })
        document.getElementById("mode31").addEventListener("click", function () {
            mode = 31
            turnOnWebcam();
        })
        document.getElementById("mode32").addEventListener("click", function () {
            mode = 32
            webcam_stream.getTracks().forEach(function(track) {
                track.stop();
            });
        })

        document.getElementById("make-result-button").addEventListener("click", async function () {

            sendToServer({"mode": mode}, url_mode)

            if (mode == 1) {
                // document.getElementById("emotion-test").innerHTML += smile_emotions_codes.get(getEmotion());
            }

            if (mode == 21 || mode == 31){
                // imageCapture.grabFrame().then(imageBitmap => {
                // const canvas = document.querySelector('#grabFrameCanvas');
                //     drawCanvas(canvas, imageBitmap);
                //     sendToServer({"image": canvas.getContext('2d').getImageData(0, 0, imageBitmap.width, imageBitmap.height).data}, url_frame);
                // }).catch(error => console.log(error));

                sendFrames();
                //
                let i = 0
                while (true) {
                    let emotion = JSON.parse(getEmotion(url_frame_get)).get(emotion);
                    let a = smile_emotions_codes.get(emotion);
                    console.log(a)
                    document.getElementById("emotion-test").innerHTML += a;
                }


                // imageCapture.grabFrame().then(imageBitmap => {
                //     const canvas = document.querySelector('#grabFrameCanvas');
                //     drawCanvas(canvas, imageBitmap);
                //     sendToServer(canvas.getContext('2d').getImageData(0, 0, imageBitmap.width, imageBitmap.height).data, url);
                // }).catch(error => console.log(error));

            }
        })
    }
    window.addEventListener('load', startup, false);
})();

function myLoop() {         //  create a loop function
  setTimeout(function() {   //  call a 3s setTimeout when the loop is called
    console.log('hello');   //  your code here
    i++;                    //  increment the counter
    if (i < 10) {           //  if the counter < 10, call the loop function
      myLoop();             //  ..  again which will trigger another
    }                       //  ..  setTimeout()
  }, 3000)
}

function sendFrames() {
    console.log("SendFrames")
    setTimeout(function() {
        imageCapture.grabFrame().then(imageBitmap => {
            const canvas = document.querySelector('#grabFrameCanvas');
            drawCanvas(canvas, imageBitmap);
            sendToServer({"image": canvas.getContext('2d').getImageData(0, 0, imageBitmap.width, imageBitmap.height).data.join(" ")},
                url_frame);
        }).catch(error => console.log(error));
        sendFrames();
    },100);
}

function getEmotions(url) {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', url, true)
    let data = null
    xhr.send();
    return xhr.responseText;
}

function getEmotion(url) {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', url, false)
    let data = null
    xhr.send();
    if (xhr.status != 200) {
        return -1;
    } else {
        return xhr.responseText;
    }
}

function onGrabFrameButtonClick() {
    // imageCapture.grabFrame()
    //     .then(imageBitmap => {
    //         sendFrame(imageBitmap);
    //     })
    //     .catch(error => ChromeSamples.log(error));

    imageCapture.grabFrame()
        .then(imageBitmap => {
            const canvas = document.querySelector('#grabFrameCanvas');
            drawCanvas(canvas, imageBitmap);
            sendToServer({"image" : canvas.getContext('2d').getImageData(0, 0, imageBitmap.width, imageBitmap.height).data},);
        })
        .catch(error => console.log(error));

}

function drawCanvas(canvas, img) {
    canvas.width = getComputedStyle(canvas).width.split('px')[0];
    canvas.height = getComputedStyle(canvas).height.split('px')[0];
    let ratio  = Math.min(canvas.width / img.width, canvas.height / img.height);
    let x = (canvas.width - img.width * ratio) / 2;
    let y = (canvas.height - img.height * ratio) / 2;
    canvas.getContext('2d').clearRect(0, 0, canvas.width, canvas.height);
    canvas.getContext('2d').drawImage(img, 0, 0, img.width, img.height,
        x, y, img.width * ratio, img.height * ratio);
}

// "http://localhost:8080/send_frame/"

function sendToServer(obj, url) {
    const data = JSON.stringify(obj);
    xhr.open("POST", url, false)
    xhr.setRequestHeader("Content-Type", "application/json")
    xhr.send(data)
}