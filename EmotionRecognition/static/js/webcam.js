let imageCapture;
let xhr = new XMLHttpRequest();

(function() {
    let video = null;
    let click_button = null;
    let canvas = null;
    let mediaDevice = null;
    let webcam_stream = null
    let mode = -1;

    let emotions = new Map();

    emotions.set(1, "Angry");
    emotions.set(2, "Disgust");
    emotions.set(3, "Fear");
    emotions.set(4, "Happy");
    emotions.set(5, "Sad");
    emotions.set(6, "Surprise");
    emotions.set(7, "NoFace");



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
            console.log(mode);
            var xhr = new XMLHttpRequest();
            const url = 'http://localhost:8080/get_first_mode_result/';
            var xhr = new XMLHttpRequest();
            xhr.open('GET', url, false)
            let data = null
            do {
                xhr.send()
            } while (xhr.status != 200)

            console.log(xhr.responseText)

            //sendRequest();

            // sendToServer(mode)
        })

        // navigator.mediaDevices.getUserMedia({video: true, audio: false})
        //     .then(function(stream) {
        //         video.srcObject = stream;
        //         video.width = 800;
        //         video.height = 300;
        //         video.play();
        //
        //         const track = stream.getVideoTracks()[0];
        //         imageCapture = new ImageCapture(track);
        //
        //
        //     })
        //     .catch(function(err) {
        //         console.log("An error occurred: " + err);
        //     });

    }



    window.addEventListener('load', startup, false);
})();


function onGrabFrameButtonClick() {
    // imageCapture.grabFrame()
    //     .then(imageBitmap => {
    //         sendFrame(imageBitmap);
    //     })
    //     .catch(error => ChromeSamples.log(error));

    // imageCapture.grabFrame()
    //     .then(imageBitmap => {
    //         const canvas = document.querySelector('#grabFrameCanvas');
    //         drawCanvas(canvas, imageBitmap);
    //         // sendToServer(canvas.getContext('2d').getImageData(0, 0, imageBitmap.width, imageBitmap.height).data);
    //     })
    //     .catch(error => console.log(error));

}

const res = await axios({
    method: 'get',
    url: 'http://localhost:8080/get_first_mode_result/'
});



// function makeRequest() {
//     while ()
//     var xmlHttp = new XMLHttpRequest();
//
//     xmlHttp.open( "GET", theUrl, false ); // false for synchronous request
//     xmlHttp.send( null );
//     return xmlHttp.responseText;
// }


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


// http://localhost:8080/send_mode/ - пост запрос для отправки мода
// http://localhost:8080/get_first_mode_result/ - get запрос, для получения результата из видео


function sendToServer(obj) {
    const data = JSON.stringify(obj);
    xhr.open("POST", "http://localhost:8080/send_frame/", true)
    xhr.setRequestHeader("Content-Type", "application/json")
    xhr.send(data)
}