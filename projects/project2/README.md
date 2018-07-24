# Project 2

S-33A: Web Programming with Python and JavaScript

#1 Display Name prompt
When you open the webpage, it prompts you to enter a display name unless you already have one. This is stored
in the local storage of the browser so that the user does not need to type in the display name again.

#2 Layout explained
The top bar, right below the title div, contains 4 containers. The first container displays your information,
i.e. your display name. The second container displays the list of channels that you can join, which is fetched
from application.py. The third container has an input field where you can type in the name of a new channel
you want to create. When you press 'create channel', the new channel is added to the list of channels and
you can access it. The last container has the list of options that you can choose from, in order to change
the styling of the channels and text boxes.
Below the top bar, there is a message area, where you can see the messages sent to the chat room. When you
first enter the webpage, it shows you the messages of the channel that you were in last time before you left.
In between h4 tags, there is a name of a title. There's also a text area with send button, where you can send
new messages to the channel.

#3 Variables explained
1) localStorage.setItem("changed", "true") in index.js
At the very beginning of JS load() function, I set localStorage variable "changed" to "true". This is used to
check if you switched to another channel or not. Without this, the messages can be loaded twice, for instance,
when you are currently in 'general' channel and you click on 'general' again, which loads the messages once
more.

2) channel_list in application.py
As you can see, channel_list is a dictionary that has a channel name as its key and a two-dimensional array as
its value for the keys. Each message is formatted into an array [username, message, time] and then stored into
an array which stores all the messages. Two values in "General" channel are examples of the values stored.

3) channels in application.py
Channels is a separate list that stores the list of channels created by the users and also the username
of the user who created the channel. The reason why it stores the username is because this webpage also
shows the list of channels created by the user.

#4 Functions explained
1) create channel sequence
(1) create.addEventListener('click') in index.js
This function is triggered when create channel button is clicked. It checks if the user entered the name for
the new channel and if the user did, then it sends it to application.py via socket.io.
(2) create(data) in application.py
This function checks if the channel name already exists via check function and adds the new channel to the
dictionaries if not.
(3) addList(list) in index.html <script></script>
This function receives a list returned from create(data) and appends the channel name to the list of channels
displayed on the webpage.

2) load message sequence
(1) loadMessage(chn) in index.js
When li element with class 'list-item' (which is the name of channel) is clicked, this function in javascript
file is triggered. This checks if the channel that you have clicked on is different from your current channel,
and if it is, then it loads the messages by calling getMessages function in application.py via socket.io.
(2) getMessages(data) in application.py
It fetches the messages in channel_list dictionary using the name of the channel passed by loadMessage in
index.js.
(3) socket.on('messageLoaded') in index.js
It responds to socket.emit('messageLoaded') in application.py and passes the returned list to showMsg()
function in index.html <script></script>. It also sets the page title and the channel title according to
the name of the channel.
(4) showMsg(list, chn) in index.html <script></script>
It first checks if the user is trying to enter a channel different from the current channel. If it is, then
it resets the contents in message list, then iterates over for loop to append the messages to the list.

3) submit message sequence
(1) submit.addEventListener('click', function()) in index.js
When a button with id 'submit' is clicked, this function is triggered. It first gets the new message from the
text area and checks if the user entered the message. Then it socket.emits to application.py, with the new
message and the user & channel info.
(2) submit(data) in application.py
On submit, submit function in python file is called. It gets the current time from python datetime library,
and stores it in a special format that I have assigned. Then it checks if the current number of messages
stored is 100 or bigger. If it is, then it removes the first item using pop() function. Then it stores the
new inputs in an array format, in a channel_list dictionary.
(3) showMsg(list, chn)
The response from python is then passed into showMsg function in JS to perform appropriate function.

#5 Unique feature of the webpage
1) change settings
Users can change message font colour, text box colour and message font-family by choosing one of the options.
This has been implemented with javascript, using document.querySelector('#').onchange = () => {} function.
