let click_button = document.querySelector("#click-photo");
let canvas = document.querySelector("#canvas");
let imageCapture;
let xhr = new XMLHttpRequest();
var mode = -1;

(function() {
    let video = null;
    let click_button = null;
    let canvas = null;

    function startup() {
        video = document.getElementById('video');
        click_button = document.querySelector("#click-photo");
        canvas = document.querySelector("#canvas");

        document.getElementById("mode1").addEventListener("click", function () {
            mode = 1;
        })


        document.getElementById("mode21").addEventListener("click", function () {
            mode = 21
        })

        document.getElementById("mode22").addEventListener("click", function () {
            mode = 22
        })

        document.getElementById("mode31").addEventListener("click", function () {
            mode = 31
        })

        document.getElementById("mode32").addEventListener("click", function () {
            mode = 32
        })


        document.getElementById("make-result-button").addEventListener("click", function () {
            sendToServer(mode)
        })

        navigator.mediaDevices.getUserMedia({video: true, audio: false})
            .then(function(stream) {
                video.srcObject = stream;
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

    window.addEventListener('load', startup, false);
})();


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


function sendToServer(obj) {
    const data = JSON.stringify(obj);
    xhr.open("POST", "http://localhost:8080/send_frame/", true)
    xhr.setRequestHeader("Content-Type", "application/json")
    xhr.send(data)
}