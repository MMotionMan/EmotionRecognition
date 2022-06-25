let imageCapture;
let xhr = new XMLHttpRequest();
const url = 'http://localhost:8080/get_first_mode_result/';
const url_mode = "http://localhost:8080/send_mode/"


(function() {
    let video = null;
    let click_button = null;
let canvas = document.querySelector("#canvas");
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

        //
        click_button = document.querySelector("#click-photo");
        canvas = document.querySelector("#canvas");
        // mediaDevice = navigator.mediaDevices.getUserMedia({video: true, audio: false})
        //
        // mediaDevice.then(function(stream) {
        //     video.srcObject = stream;
        //     webcam_stream = stream
        //     video.width = 800;
        //     video.height = 300;
        //     video.play();
        //
        //     const track = stream.getVideoTracks()[0];
        //     imageCapture = new ImageCapture(track);
        // })
        //     .catch(function(err) {
        //         console.log("An error occurred: " + err);
        //     });

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
                document.getElementById("emotion-test").innerHTML += smile_emotions_codes.get(getEmotion());
            }

            if (mode == 21 || mode == 31){



            }

            imageCapture.grabFrame().then(imageBitmap => {
                const canvas = document.querySelector('#grabFrameCanvas');
                drawCanvas(canvas, imageBitmap);
                // sendToServer(canvas.getContext('2d').getImageData(0, 0, imageBitmap.width, imageBitmap.height).data, url);
            }).catch(error => console.log(error));



            // console.log(mode)
            // //
            // sendToServer({"mode": mode}, url_mode)
            //
            // var xhr = new XMLHttpRequest();
            // xhr.open('GET', url, false)
            // let data = null
            // xhr.send();
            // if (xhr.status != 200) {
            //     alert( xhr.status + ': ' + xhr.statusText );
            // } else {
               // document.getElementById("emotion-test").innerHTML += smile_emotions_codes.get(xhr.responseText);
            // }

            // document.getElementById("result-tab").disabled = false;

            // let emotion = xhr.responseText;

            document.getElementById("emotion-test").innerHTML += smile_emotions_codes.get("angry");

        })

    }



    window.addEventListener('load', startup, false);
})();

function getEmotion() {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', url, false)
    let data = null
    xhr.send();
    if (xhr.status != 200) {
        return -1;
    } else {
        return xhr.responseText;
        // document.getElementById("emotion-test").innerHTML += smile_emotions_codes.get(xhr.responseText);
    }
}

function onGrabFrameButtonClick() {
    imageCapture.grabFrame()
        .then(imageBitmap => {
            sendFrame(imageBitmap);
        })
        .catch(error => ChromeSamples.log(error));

    imageCapture.grabFrame()
        .then(imageBitmap => {
            const canvas = document.querySelector('#grabFrameCanvas');
            drawCanvas(canvas, imageBitmap);
            // sendToServer(canvas.getContext('2d').getImageData(0, 0, imageBitmap.width, imageBitmap.height).data);
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
    xhr.open("POST", url, true)
    xhr.setRequestHeader("Content-Type", "application/json")
    xhr.send(data)
}