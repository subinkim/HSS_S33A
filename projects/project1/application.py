import os
import json

from flask import Flask, session, render_template, request, jsonify, redirect, url_for
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import requests

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

@app.route("/")
def index():
    return render_template("index.html", message="Complete the form below.", login = session.get("logged_in",))

#Register - make an account
@app.route("/register", methods=["POST", "HEAD", "GET"])
def register():
    name = request.form.get('name')
    username = request.form.get('username')
    password = request.form.get('password')
    if (name is None) or (username is None) or (password is None):
        return render_template("index.html", message = "Please fill in all the required fields.")
    elif len(username) < 6:
        return render_template("index.html", message="Your username has to be 6 characters or longer.", login = session.get("logged_in"))
    elif len(password) < 8:
        return render_template("index.html", message="Your password has to be 8 characters or longer.", login=session.get("logged_in"))
    else:
        if db.execute("SELECT * FROM users WHERE username = :user", {"user": username}).rowcount != 0:
            return render_template("index.html", message = "Username already exists. Please choose another username.")
        else:
            db.execute("INSERT INTO users (username, password, name) VALUES (:username, :password, :name)", {"username": username, "password":password, "name":name})
            db.commit()
            return render_template("login.html", login = session.get("logged_in"), message = "Please sign in.")

#Once you register, website redirects you to login page
@app.route("/registered_users")
def registered_users():
    return render_template("login.html", login = session.get("logged_in"))

#Login
@app.route("/login", methods=["POST", "HEAD", "GET"])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    if (username is None) or (password is None):
        return render_template("login.html", message = "Please fill in all the required fields.", login = session.get("logged_in"))

    if db.execute("SELECT * FROM users WHERE username = :user", {"user": username}).rowcount == 0:
        return render_template("index.html", message = "Username does not exist. Please sign up.", login = session.get("logged_in"))

    if db.execute("SELECT * FROM users WHERE username = :user AND password = :password", {"user": username, "password": password}).rowcount == 0:
        return render_template("login.html", message = "Wrong password!", login = session.get("logged_in"))

    session["logged_in"] = True
    session["username"] = username
    locations = db.execute("SELECT * FROM locations ORDER BY zipcode ASC").fetchall()
    return render_template("locations.html", locations=locations, login=session.get("logged_in"))

#Initial locations page, which lists all the places available for search
@app.route("/locations_initial")
def locations_initial():
    locations = db.execute("SELECT * FROM locations ORDER BY zipcode ASC").fetchall()
    return render_template("locations.html", locations=locations, login=session.get("logged_in"))

#Once you perform a search
@app.route("/locations", methods=["POST", "HEAD", "GET"])
def locations():
    zipcode = request.form.get('zipcode')
    city = request.form.get('city').upper()
    if not(zipcode is None) and city is None:
        locations = db.execute("SELECT * FROM locations WHERE zipcode LIKE :zipcode ORDER BY zipcode ASC", {"zipcode": f"%{zipcode}%"}).fetchall()
    elif zipcode is None and not(city is None):
        locations = db.execute("SELECT * FROM locations WHERE city LIKE :city ORDER BY zipcode ASC", {"city": f"%{city}%"}).fetchall()
    else:
        locations = db.execute("SELECT * FROM locations WHERE zipcode LIKE :zipcode AND city LIKE :city ORDER BY zipcode ASC", {"zipcode": f"%{zipcode}%", "city": f"%{city}%"}).fetchall()

    if locations is None:
        return render_template("error.html", message="No such location.")
    return render_template("locations.html", locations=locations, login=session.get("logged_in"))

#Location page that shows more info about the location you have chosen
@app.route("/location/<zipcode>", methods=["POST", "HEAD", "GET"])
def location(zipcode):
    loc = db.execute("SELECT * FROM locations WHERE zipcode = :zipcode", {"zipcode": zipcode}).fetchone()
    latitude = loc['latitude']
    longitude = loc['longitude']
    weather = requests.get(f"https://api.darksky.net/forecast/afc0556993caa66315c99a1440d8252c/{latitude},{longitude}").json()
    weather = weather["currently"]
    zipcode = loc['zipcode']
    return render_template("location.html", location=loc, login=session.get("logged_in"), weather = weather)

#Comment
@app.route("/comment/<zipcode>", methods=["POST", "HEAD", "GET"])
def comment(zipcode):
    comment = request.form.get('comment')
    if comment == "":
        return render_template("error.html", message="Please enter a text into textbox to submit a comment.")
    loc = db.execute("SELECT * FROM locations WHERE zipcode = :zipcode", {"zipcode": zipcode}).fetchone()
    latitude = loc['latitude']
    longitude = loc['longitude']
    weather = requests.get(f"https://api.darksky.net/forecast/afc0556993caa66315c99a1440d8252c/{latitude},{longitude}").json()
    weather = weather["currently"]
    commentList = loc['comment']
    if commentList == None:
        commentList.append(comment)
    elif commentList[0] == None:
        commentList[0] = comment
    else:
        commentList.append(comment)
    if session.get("logged_in") is True:
        db.execute("UPDATE locations SET comment = :commentList WHERE zipcode = :zipcode", {"commentList": commentList, "zipcode": loc['zipcode']})
        db.commit()
        return redirect(url_for('location', zipcode=loc[0]))
    else:
        return render_template("error.html", message = "You cannot write comments.")

#Check_in
@app.route("/check_in/<zipcode>", methods=["POST", "HEAD", "GET"])
def check_in(zipcode):
    loc = db.execute("SELECT * FROM locations WHERE zipcode = :zipcode", {"zipcode": zipcode}).fetchone()
    latitude = loc['latitude']
    longitude = loc['longitude']
    weather = requests.get(f"https://api.darksky.net/forecast/afc0556993caa66315c99a1440d8252c/{latitude},{longitude}").json()
    weather = weather["currently"]
    username = session.get("username")
    user = db.execute("SELECT * FROM users WHERE username = :username", {"username": username}).fetchone()
    check = user['check_in']
    valid = True
    for x in range(0, len(check)):
        if check[x] == zipcode:
            valid = False
            return render_template("error.html", message="You already checked in.")
            break
    if session.get("logged_in") and valid == True:
        check.append(zipcode)
        db.execute("UPDATE locations SET check_in = check_in + 1 WHERE zipcode = :zipcode", {"zipcode": zipcode})
        db.execute("UPDATE users SET check_in = :check WHERE username = :username", {"check": check, "username": username})
        db.commit()
        return redirect(url_for('location', zipcode=loc['zipcode']))
    else:
        return render_template("error.html", message = "You are not signed in. Please log in to check_in.")

#API
@app.route("/api/<zipcode>")
def locations_api(zipcode):
    location = db.execute("SELECT * FROM locations WHERE zipcode = :zip ORDER BY zipcode ASC", {"zip": zipcode}).fetchone()
    if location is None:
        return jsonify({"error": "Invalid zipcode"}), 404

    return jsonify({
            "place_name": location.city.lower().title(),
            "zipcode": location.zipcode,
            "state": location.state,
            "latitude": float(location.latitude),
            "longitude": float(location.longitude),
            "population": location.population,
            "check_ins": location.check_in
    })

#Logout
@app.route("/log_out")
def log_out():
    session["logged_in"] = False
    session.clear()
    return render_template("index.html", message="Logged out!")