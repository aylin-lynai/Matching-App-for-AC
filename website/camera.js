document.getElementById('StartButton').addEventListener('click', function() {
    window.location.href = 'TestPicturePage.html'; 
});

document.addEventListener('DOMContentLoaded', function() {
    const videoElement = document.getElementById('videoElement');

    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
       
        const constraints = {
            video: true, 
            audio: false 
        };

  
        navigator.mediaDevices.getUserMedia(constraints)
        .then(function(stream) {  videoElement.srcObject = stream;
            videoElement.play();
        })
        .catch(function(error) {
            console.error("Error accessing media devices.", error);
        });
    } else {
        alert('Your browser does not support media devices.');
        return;
    }
});
