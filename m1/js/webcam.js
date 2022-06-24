(function() {
    var video = null;

    function startup() {
        video = document.getElementById('video');

        navigator.mediaDevices.getUserMedia({video: true, audio: false})
            .then(function(stream) {
                video.srcObject = stream;
                video.width = 800;
                video.height = 300;
                video.play();


            })
            .catch(function(err) {
                console.log("An error occurred: " + err);
            });
        // video.addEventListener('canplay', function(ev){
        //     if (!streaming) {
        //         height = video.videoHeight / (video.videoWidth/width);
        //
        //         if (isNaN(height)) {
        //             height = width / (4/3);
        //         }
        //
        //         video.setAttribute('width', width);
        //         video.setAttribute('height', height);
        //         streaming = true;
        //     }
        // }, false);
    }

    window.addEventListener('load', startup, false);
})();