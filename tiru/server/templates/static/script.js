var io_param = window.location.protocol + '//' + document.domain + ':' + location.port
var socket = io.connect(
    io_param, {transports: ['websocket']}
);

var IMAGE_WIDTH = 640;

// Returns 'connect' data from test_connect function
socket.on('connect', function () {
    console.log("Connected...!", socket.connected, 'at', io_param)
    socket.on('disconnect', () => {
        console.log("Disconnected...!", socket.connected)
    })
});


socket.on('stream_image', function (image_dict) {
    // For <img id="image_id" src=...>
    console.log("Received img!") 
    // Modify image.data 
    var image = new Image();
    image.src = image_dict.data;
    var _width = IMAGE_WIDTH;
    var _height = image.height * IMAGE_WIDTH / image.width;;
    // Modify stats 
    var image_str = image_dict.stats 
    image_str += `<br>pixel: (${image.height}, ${image.width}) / `;
    image_str += `(${_height.toFixed(1)}, ${_width.toFixed(1)})`;
    // Add image to DOM 
    var image_el = document.getElementById("image_id")  
    image_el.setAttribute('src', image.src);
    image_el.setAttribute('width', _width);
    image_el.setAttribute('height', _height);
    document.getElementById("image_text_id").innerHTML = image_str;
    console.log(image_str)
});


socket.on('stream_text', function (text) {
    // For <img id="photo" width="400" height="300">
    console.log("Received text!") 
    const parsed_text = "<h3>" + text + "</h3>"; 
    var text_el = document.getElementById("div_text_id")
    text_el.innerHTML = parsed_text;   
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

