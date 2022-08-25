import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

# Imports from spotipy library, a library that allows python access to the Spotify API
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Initializes song, album, release, and popularity as global variables that are empty lists so the can be used and updated by all functions
song = []
album = []
release = []
popularity = []

# Uses the spotipy library to access the spotify API and stores code snippet in sp.
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials())

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///songs.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Initial page of the site, shown when the site is first accessed as long as the user is logged in
@app.route("/")
@login_required
def index():
    # Goes to main html page, storing variables for songs, albums, release_dates, and popularity_list.
    return render_template("index.html", songs = song[:5], albums = album[:5], release_dates=release[:5], popularity_list = popularity[:5])

# Login page for the site, shows up if the user is not yet logged in
@app.route("/login", methods=["GET", "POST"])
def login():
    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/search")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

# Code for the register page if the user clicks register because they are not already logged in
@app.route("/register", methods=["GET", "POST"])
def register():
    # Checks for POST method
    if request.method == "POST":

        # Sets username, password, and confirmation to user input
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Checks that username is not null
        if not username:
            return apology("must provide username")
        
        # Checks that password is not null
        if not password:
            return apology("must provide password")
        
        # Checks that confirmation is not null
        if not confirmation:
            return apology("must provide confirmation")

        # Additional element chosen was to add requirements for letters, numbers and special characters to the password
        # Creates a counter for the number of special characters
        specchar_counter = 0

        # Iterates over each letter in the password and increments specchar_counter if it is a special character
        for letter in password:
            if ((33 <= ord(letter) or ord(letter) <= 47) or (58 <= ord(letter) or ord(letter) <= 64)):
                specchar_counter += 1

        # If there are no special characters, returns an error message
        if (specchar_counter == 0):
            return apology("Please use special characters in your password")

        # Creates a counter for the number of letters
        regchar_counter = 0

        # Iterates over each letter in the password and increments regchar_counter if it is an alphabetic letter
        for letter in password:
            if (65 <= ord(letter.upper()) or ord(letter.upper()) <= 90):
                regchar_counter += 1

        # If there are no alphabetic letters, returns an error message
        if (regchar_counter == 0):
            return apology("Please use letters in your password")

        # Creates a counter for the amount of numbers
        num_counter = 0

        # Iterates over each letter in the password and increments num_counter if it is a number
        for letter in password:
            if (48 <= ord(letter) or ord(letter) <= 57):
                num_counter += 1

        # If there are no numbers, returns an error message
        if (num_counter == 0):
            return apology("Please use numbers in your password")

        # If password is less than 8 characters, return an error message
        if (len(password) < 8):
            return apology("Please choose a password with at least 8 characters")

        # Checks if password and confirmation match
        if (password != confirmation):
            return apology("Passwords do not match")

        # Hashes the user's password
        hash = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)

        # Inserts the username and the hash into user and returns and error message if the user name has already been taken
        try:
            pk = db.execute("INSERT INTO users (username, hash) VALUES (?, ? )", username, hash)
        except ValueError:
            return apology("username already taken")

        # Saves user's session
        session["user_id"] = pk
        
        # Redirects to homepage
        flash("Registered!")
        return redirect("/search")

    # If page is accessed through the GET method, renders register.html
    else:
        return render_template("register.html")

# Allows the user to log out of the site
@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

# Code to access the song page when the user clicks for the full list of songs
@app.route("/songs")
def songs():
    # Renders songs.html with values stored for songs and popularity_list
    return render_template("songs.html", songs=song, popularity_list = popularity)

# Code to access the albums page when the user clicks for the full list of albums
@app.route("/albums")
def albums():
    # Renders albums.html with values stored for albums and release_dates
    return render_template("albums.html", albums = album, release_dates = release)

# Code to access the search page when the user clicks the search link
@app.route("/search", methods=["GET", "POST"])
@login_required
def search():
    # Checks for a GET vs POST method; The first part runs for a POST method
    if request.method == "POST":
        # Lets the code know that global variables are being updated and then each time the user submits a new request, sets song, album, release, and popularity to empty lists
        # When these variable are accessed at any point in the code, their values depend on how their value updates based on this function
        global song
        song = []

        global album
        album = []

        global release
        release = []

        global popularity
        popularity = []

        # Gets user input from the form on the search page
        user_input = request.form.get("artists")

        # Uses search feature from spotify API through sotipy to search for songs related to the user's request; stored in song_results; limited at 50 by nature of the Spotify API
        song_results = sp.search(q=user_input, limit=50, type = 'track')

        # Returns an error message if user's query returns no results for songs
        if song_results['tracks']['items'] == []:
            return apology("Please enter a valid artist/artists")

        # For loop that iterates over each item in song_results['tracks]['items']
        for i in range(len(song_results['tracks']['items'])):
            # Appends the name of each song to the list "song"; results in a full list of the names of the songs returned in song_results
            song.append(song_results['tracks']['items'][i]['name'])

            # Appends the popularity value of each song to the list "popularity"; reults in a full list of the popularity values of the songs returned in song_results
            popularity.append(song_results['tracks']['items'][i]['popularity'])

        # Uses search feature from spotify API through sotipy to search for albums related to the user's request; stored in album_results; limited at 50 by nature of the Spotify API
        album_results = sp.search(q=user_input, limit=50, type = 'album')

        # Returns an error message if user's query returns no results for albums
        if album_results['albums']['items'] == []:
            return apology("Please enter a valid artist/artists")

        # For loop that iterates over each item in album_results['tracks]['items']
        for i in range(len(album_results['albums']['items'])):
            # Appends the name of each album to the list "album"; Results in a full list of the names of the albums returned in album_results
            album.append(album_results['albums']['items'][i]['name'])

            # Appends the release date of each album to the list "release"; Results in a full list of the release dates of the ablums returned in album_results
            release.append(album_results['albums']['items'][i]['release_date'] + '\n\n')

        # Renders index.html with new values stored for songs, albums, release_dates, and popularity_list
        return render_template("index.html", songs = song[:5], albums = album[:5], release_dates=release[:5], popularity_list = popularity[:5])

    # If page is accessed through the GET method, renders search.html so the user can search
    else:
        return render_template("search.html")

# Handles errors in the code
def errorhandler(e):
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
