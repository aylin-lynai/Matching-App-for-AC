document.getElementById('startButton').addEventListener('click', function() {
    window.location.href = 'TestPicturePage.html'; // This assumes your second HTML file is named 
});
function openVideoWindow() {
    // 打开一个新窗口
    const videoWindow = window.open('', 'VideoWindow', 'width=300,height=200');

    // 向新窗口添加基础的HTML结构
    videoWindow.document.write(`
        <html>
        <head><title>Video Stream</title></head>
        <body>
            <h1>Video Stream Window</h1>
            <video id="videoElement" autoplay playsinline></video>
        </body>
        </html>
    `);

    // 请求摄像头权限并播放视频
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        const constraints = { video: true, audio: false };

        navigator.mediaDevices.getUserMedia(constraints)
            .then(function(stream) {
                const videoElement = videoWindow.document.getElementById('videoElement');
                videoElement.srcObject = stream;
            })
            .catch(function(error) {
                console.error("Error accessing media devices.", error);
                videoWindow.alert('Error accessing camera.');
            });
    } else {
        videoWindow.alert('Your browser does not support media devices.');
    }
}
