from flask import Flask, redirect, url_for, render_template, request, redirect
import requests
import json
import random
import sqlite3 as sql

app = Flask(__name__, static_folder='static')

apiKEY = '054c1318c6bf2ac45d4cd737d88111eb'
data = {}


@app.route("/")
def index():
    params = {
        'api_key': '054c1318c6bf2ac45d4cd737d88111eb',
    }
    urlStart = 'https://api.themoviedb.org/3/trending/all/day'
    trendingMovies = requests.get(
        f'{urlStart}?api_key={apiKEY}', params=params)
    return render_template("index.html", userName='Login', movieName=json.loads(trendingMovies.text)['results'])


@app.route("/moviePlot")
def moviePlot():
    movieName = request.args['movieName']
    params = {
        'api_key': '054c1318c6bf2ac45d4cd737d88111eb',
    }
    searchQuery = apiKEY + '&language=en-US&query=' + \
        movieName + '&page=1&include_adult=false'
    searchResults = requests.get(
        f'https://api.themoviedb.org/3/search/movie?api_key={searchQuery}', params=params)
    return render_template("movieDetails.html", movieName=json.loads(searchResults.text)['results'])


@app.route("/home")
def home():
    userName = request.args['userName']
    params = {
        'api_key': '054c1318c6bf2ac45d4cd737d88111eb',
    }
    trendingMovies = requests.get(
        f'https://api.themoviedb.org/3/trending/all/day?api_key={apiKEY}', params=params)
    return render_template("index.html", userName=userName, movieName=json.loads(trendingMovies.text)['results'])


@app.route("/search", methods=["GET"])
def search():
    userName = request.args['userName']
    params = {
        'api_key': '054c1318c6bf2ac45d4cd737d88111eb',
    }
    searchText = request.args['query']
    # searchText = 'iron%20man'
    searchQuery = apiKEY + '&language=en-US&query=' + \
        searchText + '&page=1&include_adult=false'
    searchResults = requests.get(
        f'https://api.themoviedb.org/3/search/movie?api_key={searchQuery}', params=params)
    return render_template("index.html", userName=userName, movieName=json.loads(searchResults.text)['results'])

# moods route


moodList = {'happy': ['la+la+land', 'happy', 'cars', 'toy', 'up'],
            'sad': ['moonlight', 'sad', 'depression', 'suicide', 'joker'],
            'excited': ['iron+man', 'dunkirk', 'wonder', 'mission'],
            'angry': ['get+out', 'black', 'djnago', 'kill+bill'],
            'loving': ['vow', 'love', 'the+theory+of+everything', 'twilight']}


@app.route("/moods", methods=["POST", "GET"])
def moods():
    if request.method == "POST":
        global moodList
        userName = request.form.get('userName')
        moodValue = request.form.get('mood')
        params = {
            'api_key': '054c1318c6bf2ac45d4cd737d88111eb',
        }
        # searchText = request.args['query']
        searchNumber = random.randint(0, 3)
        searchText = moodList[moodValue][searchNumber]
        searchQuery = apiKEY + '&language=en-US&query=' + \
            searchText + '&page=1&include_adult=false'
        urlStart = 'https://api.themoviedb.org/3/search/movie'
        searchResults = requests.get(
            f'{urlStart}?api_key={searchQuery}', params=params)
        return render_template("index.html", userName=userName, movieName=json.loads(searchResults.text)['results'])
    else:
        userName = request.args['userName']
        return render_template("moods.html", userName=userName)


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        userName = request.form.get('username')
        password = request.form.get('password')

        if(userName in data):
            if(password in data[userName]):
                return redirect(url_for('home', userName=userName, **request.args))
            else:
                error = "Wrong Password"
                return render_template("login.html", error=error)
        else:
            error = "No User Found"
            return render_template("login.html", error=error)
    else:
        return render_template("login.html")


@app.route("/signup", methods=["POST", "GET"])
def signup():
    global data
    if request.method == "POST":
        userName = request.form.get('username')
        password = request.form.get('password')
        data[userName] = password
        return redirect(url_for('home', userName=userName, **request.args))
    else:
        return render_template("signup.html")


if __name__ == "__main__":
    app.run(debug=True)
