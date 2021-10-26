console.log("test")
// Create WebSocket connection.
const socket = new WebSocket('ws://dgscore.ddns.net:5000');

// Connection opened
socket.addEventListener('open', function (event) {
    console.log('Connected to the WS Server!')
});

// Connection closed
socket.addEventListener('close', function (event) {
    console.log('Disconnected from the WS Server!')
});

// Listen for messages
socket.addEventListener('message', function (event) {
    console.log('Message from server ', event.data);
});
// Send a msg to the websocket
const sendMsg = () => {
    socket.send('Hello from Client1!');
}