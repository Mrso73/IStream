let video;

document.addEventListener("DOMContentLoaded", () => {
    video = document.getElementById('webcam');

    video.videoWidth = window.innerWidth;
    video.videoHeight = window.innerHeight;

    setupWebcam()
});


function setupWebcam(){
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


window.addEventListener("keydown", (e) => {
    if (e.key === ' ') {
        var canvas = document.createElement("canvas");

        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        canvas.getContext("2d").drawImage(video, 0, 0);

        sendData({image: canvas.toDataURL('image/png')});
    }
})


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