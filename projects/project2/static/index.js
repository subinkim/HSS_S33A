document.addEventListener('DOMContentLoaded', load)

function load() {
    //localStorage.clear();
    //Open new socket and request
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);
    localStorage.setItem("changed", "true");

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
        var channel = "";
        if (!localStorage.getItem("lastChannel")){
            localStorage.setItem("lastChannel", "General");
            channel = "General";
        }
        else{
            channel = localStorage.getItem("lastChannel");
        }
        document.querySelector('title').innerHTML = 'Quick Chat: ' + channel;
        loadMessage(channel);
        return false;
    });

    //When button is clicked, it triggers create method in application.py via socket.emit
    var create = document.querySelector('#create');
    create.addEventListener('click', function() {
        var name = "";
        name = document.querySelector('.form-control').value;
        if (name === "")
            alert("Enter channel name!");
        else
            socket.emit('create', {'name': name, 'user': localStorage.getItem("displayName")});
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
        list = data[0];
        name = data[1];
        showMsg(list, name);
        //sets titles
        document.querySelector('title').innerHTML = 'Quick Chat: ' + name;
        document.querySelector('#channel_info').innerHTML = 'Quick chat @ ' + name;
        //change values in local storage
        localStorage.setItem("lastChannel", name);
        localStorage.setItem("changed","false");
    });

    var submit = document.querySelector('#submit');
    submit.addEventListener('click', function () {
        var msg = "";
        msg = document.querySelector('textarea').value;
        var displayname = document.querySelector('#username').innerHTML;
        var channel = localStorage.getItem("lastChannel");

        //checking if the user entered the message
        if (msg === ""){
            alert("Enter message!");
            return false;
        }
        else {
            //displaying the message
            socket.emit('submit message', {"msg": msg, "displayname": displayname, "channel": channel});
        }
    });

    //When new message is successfully submitted
    socket.on('submission complete', data => {
        list = data[0];
        chn = data[1];
        showMsg(list, chn);
    });

    //Responds to select function --> changes the styles
    document.querySelector('#change-colour').onchange = function (){
        var message = document.querySelectorAll('.msg');
        for (var i = 0; i < message.length; i++){
            message[i].style.color = this.value;
        }
    };
    document.querySelector('#change-font-family').onchange = function(){
        var message = document.querySelectorAll('.msg');
        for (var i = 0; i < message.length; i++){
            message[i].style.fontFamily = this.value;
        }
    };
    document.querySelector('#change-bg-colour').onchange = function(){
        var message = document.querySelectorAll('.msg');
        for (var i = 0; i < message.length; i++){
            message[i].style.backgroundColor = this.value;
        }
    };
}

//Gets the name of the selected channel and calls the application.py function
function loadMessage(chn){
    if (localStorage.getItem("changed") === "true" || chn !== localStorage.getItem("lastChannel")){
        var channel = chn;
        var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);
        socket.emit('getMessages', {"selected": channel});
    }
}
