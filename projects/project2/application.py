import os
import datetime

from flask import Flask, jsonify, render_template, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

## messages in each channel
channel_list = {
    "General": [["", "Hello! Welcome to quick chat!", "7/24/2018 00:00"],
                ["", "Please enjoy our webpage!", "7/24/2018 00:00"]
    ]
}

## list of channels
channels = {"General": ""}

##Index
@app.route("/")
def index():
    return render_template("index.html")
    ##'selected' set to the last channel user visited

## Loading the list of channels
@socketio.on("channel")
def channel():
    emit("done", list(channels.keys()), broadcast=True)

## Creating a new channel and adding it to the channel_list
@socketio.on("create")
def create(data):
    channelName = data["name"]
    displayName = data["user"]
    channelName = channelName.title()
    if (check(channelName, list(channels.keys())) == False):
        emit("created", ["false"], broadcast=True)
    else:
        channels[channelName] = displayName
        channel_list[channelName] = []
        emit("created", list(channels.keys()), broadcast=True)

##Check function - checks if the item already exists in the list
def check(newItem, list):
    validity = True
    for item in list:
        if item == newItem:
            validity = False
    return validity

## Getting messages from channel_list dictionary
@socketio.on("getMessages")
def getMessages(data):
    selection = data["selected"]
    message = channel_list[selection]
    emit("messageLoaded", [message, selection], broadcast=True)

## Adding new messages to storage
@socketio.on('submit message')
def submit(data):
    msg = data["msg"]
    displayname = data["displayname"]
    channel = data["channel"]
    time = datetime.datetime.today().strftime('%m/%d/%Y %H:%M')
    ## If number of stored messages is 100, then it deletes the first item to store the new item
    if len(channel_list[channel]) >= 100:
        channel_list[channel].pop(0)
    newArray = [displayname, msg, time]
    channel_list[channel].append(newArray)
    emit('submission complete',[newArray, channel], broadcast=True)
