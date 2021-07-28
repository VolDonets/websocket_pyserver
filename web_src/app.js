var wsAddress = document.location.host;
wsAddress = wsAddress.substring(0, wsAddress.length - 4);
wsAddress = "ws://" + wsAddress + "6789";
var minus = document.querySelector('.minus'),
    plus = document.querySelector('.plus'),
    value = document.querySelector('.value'),
    users = document.querySelector('.users'),
    websocket = new WebSocket(wsAddress);
minus.onclick = function (event) {
    websocket.send(JSON.stringify({action: 'minus'}));
}
plus.onclick = function (event) {
    websocket.send(JSON.stringify({action: 'plus'}));
}
websocket.onmessage = function (event) {
    data = JSON.parse(event.data);
    switch (data.type) {
        case 'state':
            value.textContent = data.value;
            break;
        case 'users':
            users.textContent = (
                data.count.toString() + " user" +
                (data.count == 1 ? "" : "s"));
            break;
        default:
            console.error(
                "unsupported event", data);
    }
};
