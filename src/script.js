let video, canvas, ctx;

window.onload = function(){
    video = document.getElementById('webcam');
    canvas = document.getElementById("stream");
    ctx = canvas.getContext('2d');

    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    canvasSetup();
    canvasUpdate();
}

window.onresize = function(){
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    position();
}

function canvasSetup(){
    if (!video.srcObject) {
        navigator.mediaDevices.getUserMedia({ video: true })
            .then(function(stream) {
                video.srcObject = stream;
            })
            .catch(function(err) {
                console.error("Error accessing the webcam:", err);
            });
    }
}

function canvasUpdate(){
    window.requestAnimationFrame(canvasUpdate);

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    ctx.fillStyle = "blue";
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
}
