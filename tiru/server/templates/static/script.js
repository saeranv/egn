var io_param = window.location.protocol + '//' + document.domain + ':' + location.port
var socket = io.connect(
    io_param, {transports: ['websocket']}
);

// Returns 'connect' data from test_connect function
socket.on('connect', function () {
    console.log("Connected...!", socket.connected, 'at', io_param)
    socket.on('disconnect', () => {
        console.log("Disconnected...!", socket.connected)
    })
});


socket.on('stream_image', function (image_uri) {
    // For <img id="photo" width="400" height="300">
    console.log("Received img!") 
    document.getElementById("image_id").setAttribute('src', image_uri);
});


socket.on('stream_text', function (text) {
    // For <img id="photo" width="400" height="300">
    console.log("Received text!") 
    document.getElementById("text_id").innerHTML = text;
});

// window.onload = function () {
//     var canvas = document.getElementById('canvas');
//     var context = canvas.getContext('2d');
//     context.fillStyle = "#FF0000";                                                  
//     context.fillRect(0, 0, 150, 75);                                                
// }
// named div
//const video = document.getElementById("img_1");
//video.width = 400;
//video.height = 300;


// sends 'image' data to receive_image function
// data = base64 image string?
// const FPS = 10;
// setInterval(() => {
//     w = video.width
//     h = video.height;
//     context.drawImage(video, 0, 0, w, h);
//     var data = canvas.toDataURL('image/jpeg', 0.5);
//     context.clearRect(0, 0, w, h);
//     socket.emit('image', data);
// }, 1000 / FPS);

// Returns processed_image receives_image function
// returned data of image is set to id=photo
//socket.on('processed_image', function (image) {
//    photo.setAttribute('src', image);
//});

//const FPS = 10;
//setInterval(() => {
//    socket.emit('process_image');
//}, 1000 / FPS);

