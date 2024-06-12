document.addEventListener('DOMContentLoaded', function() {
    const videoElement = document.getElementById('videoElement');

    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        // 定义要获取的媒体类型
        const constraints = {
            video: true, // 请求视频
            audio: false // 如果需要音频，可以设置为true
        };

        // 请求摄像头权限
        navigator.mediaDevices.getUserMedia(constraints)
        .then(function(stream) {
            // 将视频流绑定到video元素上
            videoElement.srcObject = stream;
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
