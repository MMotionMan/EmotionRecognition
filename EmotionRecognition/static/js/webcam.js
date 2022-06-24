
let click_button = document.querySelector("#click-photo");
let canvas = document.querySelector("#canvas");
var imageCapture;
let xhr = new XMLHttpRequest();



(function() {
    var video = null;
    var click_button = null;
    var canvas = null;

    function startup() {
        video = document.getElementById('video');
        click_button = document.querySelector("#click-photo");
        canvas = document.querySelector("#canvas");

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

    imageCapture.grabFrame()
        .then(imageBitmap => {
            sendFrame(imageBitmap);
        })
        .catch(error => ChromeSamples.log(error));

    // imageCapture.grabFrame()
    //     .then(imageBitmap => {
    //         const canvas = document.querySelector('#grabFrameCanvas');
    //         drawCanvas(canvas, imageBitmap);
    //     })
    //     .catch(error => ChromeSamples.log(error));

}

// function drawCanvas(canvas, img) {
//     canvas.width = getComputedStyle(canvas).width.split('px')[0];
//     canvas.height = getComputedStyle(canvas).height.split('px')[0];
//     let ratio  = Math.min(canvas.width / img.width, canvas.height / img.height);
//     let x = (canvas.width - img.width * ratio) / 2;
//     let y = (canvas.height - img.height * ratio) / 2;
//     canvas.getContext('2d').clearRect(0, 0, canvas.width, canvas.height);
//     canvas.getContext('2d').drawImage(img, 0, 0, img.width, img.height,
//         x, y, img.width * ratio, img.height * ratio);
// }

function sendFrame(img) {
    var data = JSON.stringify(img);
    xhr.open("POST", "", true)
    xhr.setRequestHeader("Content-Type", "application/json")
    xhr.send(data)
}

