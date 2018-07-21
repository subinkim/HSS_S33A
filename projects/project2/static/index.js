document.addEventListener('DOMContentLoaded', load)

function load() {
    //localStorage.clear();
    //Open new socket and request
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);
    const request = new XMLHttpRequest();

    socket.on('connect', () => {
        //Asks for username if there's not one stored in local storage
        //Username set to 'Anon user' by default if nothing is entered.
        if (!localStorage.getItem("displayName")){
            var username = prompt("Please enter your display name: ", "Anon User");
            if (username.length === 0)
                username = prompt("Enter your display name: ");
            localStorage.setItem("displayName", username);
        }
        //Displays the user's display name on webpage
        document.querySelector('#username').innerHTML = localStorage.getItem("displayName");
        socket.emit('channel');
    });

    //Gets the list of channels
    socket.on('done', response => {
        addList(response);
    });

    //When button is clicked, it triggers create method in application.py via socket.emit
    var submit = document.querySelector('#create');
    submit.addEventListener('click', function() {
        var name = "";
        name = document.querySelector('.form-control').value;
        if (name === "")
            alert("Enter channel name!");
        else
            socket.emit('create', {'name': name});
        return false;
    });

    //When application.py returns the value via socket, it is checked and then displayed
    socket.on('created', response => {
        if (response[0] === "false")
            alert("Channel name is already taken!");
        else{
            var newElement = response.pop();
            addList([newElement]);
        }
        return false;
    });

    //When messages are loaded for the selected channel
    socket.on('messageLoaded', data => {
        dict = data[0];
        name = data[1];
        showMsg(dict);
        document.querySelector('#channel_info').innerHTML = "Current channel: " + name;
    });
}

//Gets the name of the selected channel and calls the application.py function
function loadMessage(chn){
    var channel = chn;
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);
    socket.emit('getMessages', {"selected": channel});
}
