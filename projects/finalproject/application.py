import os
import json
import datetime

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

#Index page where new users can register
@app.route("/")
def index():
    return render_template("index.html", message="Complete the form below.", login = session.get("logged_in",))

#Register - make an account
@app.route("/register", methods=["POST"])
def register():
    if request.method == "POST":
        #Get data from the form
        firstname = request.form.get('firstname').title()
        lastname = request.form.get('lastname').title()
        username = request.form.get('username').lower()
        password = request.form.get('password')

        # Check if inputs match the criteria
        if (firstname is None) or (lastname is None) or (username is None) or (password is None):
            return render_template("index.html", message = "Please fill in all the required fields.", login=session.get("logged_in"))
        elif len(username) < 6:
            return render_template("index.html", message="Your username has to be 6 characters or longer.", login = session.get("logged_in"))
        elif len(password) < 8:
            return render_template("index.html", message="Your password has to be 8 characters or longer.", login=session.get("logged_in"))

        # Insert new user into database
        else:
            if db.execute("SELECT * FROM users WHERE username = :user", {"user": username}).rowcount != 0:
                return render_template("index.html", message = "Username already exists. Please choose another username.", login=session.get("logged_in"))
            else:
                db.execute("INSERT INTO users (firstname, lastname, username, password, saved, liked) VALUES (:first, :last, :username, :password, :saved, :liked)", {"first": firstname, "last": lastname, "username": username, "password":password, "saved": [], "liked": []})
                db.commit()
                return render_template("login.html", login = session.get("logged_in"), message = "Please sign in.")

#Login
@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')

        #Check if the user entered username and password
        if (username is None) or (password is None):
            return render_template("login.html", message = "Please fill in all the required fields.", login = session.get("logged_in"))

        #Check if credentials are correct
        if db.execute("SELECT * FROM users WHERE username = :user", {"user": username}).rowcount == 0:
            return render_template("index.html", message = "Username does not exist. Please sign up.", login = session.get("logged_in"))
        if db.execute("SELECT * FROM users WHERE username = :user AND password = :password", {"user": username, "password": password}).rowcount == 0:
            return render_template("login.html", message = "Wrong password!", login = session.get("logged_in"))

        #Session is used to remember the user unless they log out from the website
        session["logged_in"] = True
        session["username"] = username
        cities = db.execute("SELECT * FROM cities ORDER BY population DESC").fetchall()
        return render_template("cities.html", cities = cities, login=session.get("logged_in"))
    else:
        return render_template("login.html", login=session.get("logged_in"))

#Logout - clear the session when users log out
@app.route("/log_out")
def log_out():
    session["logged_in"] = False
    session.clear()
    return redirect(url_for('index'))

#Search page where users can find a city they want
@app.route("/cities", methods=["POST", "GET"])
def cities():
    #When method == "POST", search result is returned
    if request.method == "POST":
        city = request.form.get('city').lower()
        state = request.form.get('state')
        cities = db.execute("SELECT * FROM cities WHERE state = :state AND city LIKE :city ORDER BY city ASC", {"city": f"%{city}%", "state": state}).fetchall()
        return render_template("cities.html", cities=cities, login=session.get("logged_in"))
    else:
        cities = db.execute("SELECT * FROM cities ORDER BY city ASC").fetchall()
        return render_template("cities.html", cities=cities, login=session.get("logged_in"))

#Detailed information about the chosen city
@app.route("/city/<city>", methods=["GET"])
def city(city):
    cityResult = db.execute("SELECT * FROM cities WHERE city = :city", {"city": city}).fetchone()
    description = db.execute("SELECT * FROM descriptions WHERE city = :city", {"city": city}).fetchall()
    comments = db.execute("SELECT * FROM comments WHERE city = :city", {"city": city}).fetchone()
    username = session.get("username")

    ##Checking if the city is saved or not
    saves = db.execute("SELECT * FROM users WHERE username =:username", {"username": username}).fetchone()
    saved = False
    if not(saves is None):
        saves = saves["saved"]
        if city in saves:
            saved = True

    #Get weather data
    latitude = cityResult['latitude']
    longitude = cityResult['longitude']
    weather = requests.get(f"https://api.darksky.net/forecast/afc0556993caa66315c99a1440d8252c/{latitude},{longitude}").json()
    weather = weather["currently"]

    #calculate the average of the ratings
    ratings = {"food": 0, "safety": 0, "tour": 0, "clean":0, "people":0, "overall": 0}
    if len(comments['comments']) != 0:
        length = len(comments['comments'])

        ##add all the ratings by their categories
        for i in range(0, length):
            ratings['food'] += int(comments['food'][i])
            ratings['safety'] += int(comments['safety'][i])
            ratings['tour'] += int(comments['tour'][i])
            ratings['clean'] += int (comments['clean'][i])
            ratings['people'] += int (comments['people'][i])

        ## calculate their average
        ratings['food'] = int(round(ratings['food']/length,0))
        ratings['safety'] = int(round(ratings['safety']/length,0))
        ratings['tour'] = int(round(ratings['tour']/length,0))
        ratings['clean'] = int(round(ratings['clean']/length,0))
        ratings['people'] = int(round(ratings['people']/length,0))
        ratings['overall'] = (ratings['food'] + ratings['safety'] + ratings['tour'] + ratings['clean'] + ratings['people'])/5
        ratings['overall'] = int(round(ratings['overall'], 0))

        return render_template("city.html", city=cityResult, descriptions=description, ratings=ratings, comments=comments, username=username, saved=saved, login=session.get("logged_in"), weather=weather)

    else:
        return render_template("city.html", city=cityResult, descriptions=description, ratings=ratings, comments=comments, username=username, saved=saved, ratingMessage="(No data)", login=session.get("logged_in"), weather=weather, message="Fill in all fields.")


#When the user leaves comment on the city
@app.route("/comment/<city>", methods=["POST", "GET"])
def comment(city):
    if request.method == "POST":
        #Get user inputs from the form
        foodRating = str(request.form.get("foodRating"))
        safetyRating = str(request.form.get("safetyRating"))
        tourRating = str(request.form.get("tourRating"))
        cleanRating = str(request.form.get("cleanRating"))
        peopleRating = str(request.form.get("peopleRating"))
        comment = request.form.get("comment")
        time = datetime.datetime.today().strftime('%m/%d/%Y')

        comments = db.execute("SELECT * FROM comments WHERE city = :city", {"city": city}).fetchone()

        #Checking if the user filled every field
        if foodRating == "" or safetyRating == "" or tourRating == "" or cleanRating == "" or peopleRating == "" or comment == "":
            return redirect(url_for('city', city=city))

        #get data from the database
        commentList = comments['comments']
        userList = comments['usernames']
        timeList = comments['time']
        foodRatingList = comments['food']
        safetyRatingList = comments['safety']
        tourRatingList = comments['tour']
        cleanRatingList = comments['clean']
        peopleRatingList = comments['people']

        #add new data to the list
        commentList.append(comment)
        userList.append(session.get("username"))
        timeList.append(time)
        foodRatingList.append(foodRating)
        safetyRatingList.append(safetyRating)
        tourRatingList.append(tourRating)
        cleanRatingList.append(cleanRating)
        peopleRatingList.append(peopleRating)

        #Update the database
        db.execute("UPDATE comments SET comments= :comment, usernames= :username, time= :time, food= :food, safety= :safety, clean= :clean, people= :people, tour= :tour WHERE city= :city", {"comment": commentList, "username": userList, "time": timeList, "city": city, "tour": tourRatingList, "safety": safetyRatingList, "clean": cleanRatingList, "people": peopleRatingList, "food": foodRatingList})
        db.commit()
        return redirect(url_for('city', city=city))
    else:
        return redirect(url_for('city', city=city))

@app.route("/save/<city>", methods=["POST"])
def save(city):
    # append the city to 'saved' array on database to prevent user saving the same city twice
    saved = db.execute("SELECT * FROM users WHERE username=:username", {"username":session.get("username")}).fetchone()
    savedList = saved['saved']
    savedList.append(city)
    db.execute("UPDATE users SET saved = :saved WHERE username=:username", {"saved": savedList, "username":session.get("username")})
    db.execute("UPDATE comments SET saves = saves + 1 WHERE city = :city", {"city": city})
    db.commit()
    return redirect(url_for('city', city=city))

@app.route("/schedules", methods=["GET", "POST"])
def schedules():
    scheduleList = []
    if request.method == "POST":
        # get 'username', 'city', 'likes' from data in schedules database
        schedules = db.execute("SELECT * FROM schedules ORDER BY likes DESC").fetchall()
        city = request.form.get('city')
        for i in range(0,len(schedules)):
            if city in schedules[i]['city']:
                scheduleList.append([schedules[i]['username'], schedules[i]['city'], schedules[i]['likes']])
        return render_template("schedules.html", login=session.get("logged_in"), schedules=scheduleList)
    else:
        # Get all data and create new array with 'username', 'city', 'likes'
        schedules = db.execute("SELECT * FROM schedules ORDER BY likes DESC").fetchall()
        for i in range(0,len(schedules)):
            scheduleList.append([schedules[i]['username'], schedules[i]['city'], schedules[i]['likes'], schedules[i]['id']])
        return render_template("schedules.html", login=session.get("logged_in"), schedules=scheduleList)

@app.route("/schedule", methods=["GET", "POST"])
def schedule():
    if request.method == "POST":
        checked = []
        # Check which checkboxes have been checked
        for checkbox in ['cb1', 'cb2', 'cb3', 'cb4', 'cb5', 'cb6', 'cb7', 'cb8', 'cb9', 'cb10', 'cb11', 'cb12']:
            value = request.form.get(checkbox)
            if value:
                checked.append(value)

        # Check if the user checked at least one of the boxes
        if checked == []:
            return render_template("schedule.html", message="Please check at least one of the boxes.", login=session.get("logged_in"))

        # Check if user entered a description
        description = request.form.get('description')
        if description == "":
            return render_template("schedule.html", message="Please write description of your trip.", login=session.get('logged_in'))
        db.execute("INSERT INTO schedules (username, city, info, usernames, comments, times, likes) VALUES (:user, :city, :info, :users, :comments, :times, :likes)", {"user": session.get("username"), "city":checked, "info": description, "users": [], "comments": [], "times": [], "likes": 0})
        db.commit()
        return redirect(url_for('schedules'))
    else:
        return render_template("schedule.html", login=session.get("logged_in"))

@app.route("/read/<postId>", methods=['GET'])
def read(postId):
    # Get schedule from schedules database that matches the postId
    schedules = db.execute("SELECT * FROM schedules WHERE id =:id", {"id": postId}).fetchone()

    # Check if the user already liked the schedule or not
    likes = db.execute("SELECT * FROM users WHERE username = :user", {"user": session.get("username")}).fetchone()
    likes = likes['liked']
    liked = False
    if postId in likes:
        liked = True
    return render_template("read.html", schedules = schedules, liked = liked, login=session.get("logged_in"), message="Fill in all fields.", username=session.get("username"))

@app.route("/like/<postId>", methods=["POST", "GET"])
def like(postId):
    if request.method == "POST":
        # Getting 'liked' array from users database and updating with a new array with new data appended to it
        liked = db.execute("SELECT * FROM users WHERE username=:username", {"username":session.get("username")}).fetchone()
        liked = liked['liked']
        liked.append(postId)
        db.execute("UPDATE users SET liked = :liked WHERE username=:username", {"liked": liked, "username":session.get("username")})
        db.execute("UPDATE schedules SET likes = likes + 1 WHERE id = :id", {"id": postId})
        db.commit()
        return redirect(url_for('read', postId=postId))
    else:
        return redirect(url_for('read', postId=postId))

@app.route('/addComment/<postId>', methods=["POST", "GET"])
def addComment(postId):
    if request.method == "POST":
        #Get user inputs from the form
        comment = request.form.get('comment')
        schedule = db.execute("SELECT * FROM schedules WHERE id = :id", {"id": postId}).fetchone()
        time = datetime.datetime.today().strftime('%m/%d/%Y')

        #Checking if the user filled every field
        if comment == "":
            return redirect(url_for('read', postId=postId))

        #get data from the database
        comments = schedule['comments']
        usernames = schedule['usernames']
        times = schedule['times']

        #add new data to the lists
        comments.append(comment)
        usernames.append(session.get("username"))
        times.append(time)

        #Update the database
        db.execute("UPDATE schedules SET comments= :comment, usernames= :username, times= :time WHERE id= :id", {"comment": comments, "username": usernames, "time": times, "id": postId})
        db.commit()
        return redirect(url_for('read', postId=postId))
    else:
        return redirect(url_for('read', postId=postId))

@app.route("/mypage", methods=["GET", "POST"])
def mypage():
    ####CITIES
    # Get saved cities from users database
    username = session.get("username")
    saved = db.execute("SELECT * FROM users WHERE username =:username", {"username": username}).fetchone()
    if saved is None:
        saved = []
    else:
        saved = saved['saved']

    # Get comments user left on cities
    comments = db.execute("SELECT * FROM comments").fetchall()
    commentList = []
    for comment in comments:
        if username in comment['usernames']:
            for i in range(0,len(comment['usernames'])):
                if comment['usernames'][i] == username:
                    newArray = [comment['comments'][i], comment['time'][i], comment['city']]
                    commentList.append(newArray)

    ###SCHEDULES
    # Get schedules that the user has shared
    schedules = db.execute("SELECT * FROM schedules WHERE username=:username", {"username": username}).fetchall()
    trips = []
    cities =[]

    # Store 'info' and 'city' in schedule to separate arrays
    for i in range(0,len(schedules)):
        trips.append([schedules[i]['info']])
        cities.append(schedules[i]['city'])

    # Get comments user left on schedules
    scheduleComments = db.execute("SELECT * FROM schedules").fetchall()
    scheduleCommentList = []
    for comment in scheduleComments:
        if username in comment[2]:
            for i in range(0,len(comment[2])):
                if comment[2][i] == username:
                    newArray = [comment[3][i], comment[5], comment[0], comment[7]]
                    scheduleCommentList.append(newArray)

    # Get list of schedules user liked
    liked = db.execute("SELECT * FROM users WHERE username =:username", {"username": username}).fetchone()
    if liked is None:
        liked = []
    else:
        liked = liked['liked']
    return render_template("mypage.html", saved=saved, comments=commentList, username=username, login=session.get("logged_in"), liked=liked, trips=trips, cities=cities, schedules=scheduleCommentList)

@app.route('/unsave/<city>', methods=["POST"])
def unsave(city):
    saves = db.execute("SELECT * FROM users WHERE username =:username", {"username": session.get("username")}).fetchone()
    saves = saves['saved']
    saves.remove(city)
    db.execute("UPDATE users SET saved = :saved WHERE username =:username", {"saved": saves, "username": session.get("username")})
    db.execute("UPDATE comments SET saves = saves - 1 WHERE city =:city", {"city": city})
    db.commit()
    return redirect(url_for('mypage'))

@app.route('/remove/<postId>', methods=["POST"])
def remove(postId):
    likes = db.execute("SELECT * FROM users WHERE username =:username", {"username": session.get("username")}).fetchone()
    likes = likes['liked']
    likes.remove(postId)
    db.execute("UPDATE users SET liked =:liked WHERE username =:username", {"liked": likes, "username": session.get("username")})
    db.execute("UPDATE schedules SET likes = likes - 1 WHERE id =:id", {"id": postId})
    db.commit()
    return redirect(url_for('mypage'))