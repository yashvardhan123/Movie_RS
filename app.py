from flask import Flask, redirect, url_for, render_template, request, redirect
import requests
import json
# import sqlite3 as sql

app = Flask(__name__, static_folder='static')

apiKEY = '054c1318c6bf2ac45d4cd737d88111eb'
data = {}

@app.route("/")
def index():
    params = {
        'api_key': '054c1318c6bf2ac45d4cd737d88111eb',
    }
    trendingMovies = requests.get(
        f'https://api.themoviedb.org/3/trending/all/day?api_key={apiKEY}', params=params)
    return render_template("index.html", userName='Login', movieName=json.loads(trendingMovies.text)['results'])


@app.route("/home")
def home():
    userName = "Hi, " + request.args['userName']
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
                return render_template("login.html", error = error)
        else:
            error = "No User Found"
            return render_template("login.html", error = error)
    else:
        return render_template("login.html")


@app.route("/signup", methods=["POST", "GET"])
def signup():
    global data
    if request.method == "POST":
        userName = request.form.get('username')
        password = request.form.get('password')
        data[userName] = password
        return redirect(url_for('home',userName=userName, **request.args))
    else:
        return render_template("signup.html")


if __name__ == "__main__":
    app.run(debug=True)
