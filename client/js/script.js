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
}

window.addEventListener("keydown", (e) => {
    if (e.key === ' ') {
        frame = canvas.toDataURL('frame/png');
        sendData({image: frame});
    }
})

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
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
}



function sendData(data) {
    fetch('http://127.0.0.1:8000/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => console.log('Success:', data))
    .catch((error) => console.error('Error:', error));
}

function fetchData() {
    fetch('http://127.0.0.1:8000/data')  // Adjust the URL based on your server setup
    .then(response => response.json())
    .then(data => console.log('Data:', data))
    .catch((error) => console.error('Error:', error));
}