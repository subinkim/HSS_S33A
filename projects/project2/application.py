import os

from flask import Flask, jsonify, render_template, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

## messages in each channel
channel_list = {"General": ["Hello! Welcome to quick chat!", "Please enjoy our service!"]}

## list of channels
channels = ["General"]

##Index
@app.route("/")
def index():
    return render_template("index.html")
    ##'selected' set to the last channel user visited

## Loading the list of channels
@socketio.on("channel")
def channel():
    emit("done", channels, broadcast=True)

## Creating a new channel and adding it to the channel_list
@socketio.on("create")
def create(data):
    channelName = data["name"]
    channelName = channelName.title()
    if (check(channelName, channels) == False):
        emit("created", ["false"], broadcast=True)
    else:
        channels.append(channelName)
        channel_list[channelName] = []
        emit("created", channels, broadcast=True)

##Check function - checks if the item already exists in the list
def check(newItem, list):
    validity = True
    for item in list:
        if item == newItem:
            validity = False
    return validity

## Getting messages from channel_list dictionary
@socketio.on('getMessages')
def getMessages(data):
    selection = data["selected"]
    message = channel_list["selection"]
    emit("messageLoaded", [message, selection], broadcast=True)
