let video, canvas, ctx, intervalId;

document.addEventListener("DOMContentLoaded", () => {
    video = document.getElementById('webcam');
    canvas = document.getElementById("stream");
    ctx = canvas.getContext('2d');

    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    setupWebcam();
    updateWebcam();
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



function updateWebcam(){
    window.requestAnimationFrame(updateWebcam);

    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
}



window.onresize = function(){
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
}



window.addEventListener("keydown", (e) => {
    if (e.key === ' ') {
        let frame = canvas.toDataURL('frame/png');
        sendData({image: frame});
    }
})

// -----------------------------

async function sendData(data) {
    try {

        let response = await fetch('http://127.0.0.1:8000/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        
        if (!response.ok) {
            throw new Error('sendData(): Network response was not ok');
        }

        let responseData = await response.json();
        console.log('Python backend:', responseData);

    } catch (error) {
        console.error('Error:', error);
    }

}

