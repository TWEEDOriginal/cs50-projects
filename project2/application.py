import os

from flask import Flask, session, render_template, request, jsonify, flash, redirect
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

display_names = []
channels_created = []
channel_messages = {}
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["POST"])    
def login():
    session.clear()
    display_name = request.form.get("display_name")
    if display_name.strip() == "":
        return render_template("index.html", message="Please enter a valid display name") 
    if display_name in display_names:
        return render_template("index.html", message="Username already taken.")
    display_name = display_name.strip()
    display_names.append(display_name)
    session['display_name'] = display_name
    session.permanent = True
    
    return render_template("channels.html", channels_created = channels_created)

@app.route("/channels", methods=["POST"])
def channels():    
    channel = request.form.get("channel")
    if channel in channels_created:
        return render_template("channels.html", message="Channel name already taken.")
    channels_created.append(channel)
    channel_messages[channel]= []
    return render_template("channels.html", channels_created = channels_created)
@app.route("/channel_page", methods=["POST"])
def channel_page():    
    current_channel = request.form.get("ch")
    session['current_channel'] = current_channel
    return render_template("current_channel.html")