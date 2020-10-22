from knn_recommender import Recommender
from youtube import Youtube
from flask import Flask, render_template, request
from ast import literal_eval
from os import environ
from dotenv import load_dotenv
import string
import json
import re

app = Flask(__name__)

def standardize(s):
    s = "".join([i.lower() for i in s if i not in frozenset(string.punctuation)])
    return s

@app.route("/")
def index():
    return render_template("home.html")

@app.route("/results", methods=["POST"])
def search():
    if request.method == "POST":
        index = int(request.form.get("index"))
        duration = int(request.form.get("duration"))
        songs = reco.find_neighbors(index, duration)

        songs_arr = dict()
        youtube_arr = dict()

        vals = songs[['name', 'artists', 'duration_ms']].values.tolist()

        for i in range(len(songs.values)):
            songs_arr[i] = {}
            name = vals[i][0]
            name = re.sub('\"', '\\\"', name)
            songs_arr[i]['name'] = name
            songs_arr[i]['duration'] = vals[i][2]
            
            artists = vals[i][1]
            artists = literal_eval(artists)
            artists_str = ""
            for artist in artists:
                artists_str = artists_str + artist + ", "
            artists_str = artists_str[:-2]
            artists_str = re.sub('\"', '\\\"', artists_str)
            songs_arr[i]['artists'] = artists_str

            if i < 1:
                try:
                    ytsearch = youtube.search(name + " - " + artists[0])
                    youtube_arr[i] = ytsearch
                except:
                    print("Out of youtube quota.")
                    youtube_arr[i] = ""
            else:
                youtube_arr[i] = ""
        return render_template("results.html", songs_arr=songs_arr, youtube_arr=youtube_arr)

@app.route('/api', methods=['POST'])
def find_test():
    name = request.values.get('input')
    name = standardize(name)
    
    found = reco.search_name(name)

    indices = found.index.values.tolist()
    vals = found.values.tolist()
    arr = dict()
    for i in range(len(found.values)):
        name = vals[i][0]
        artists = vals[i][1]
        index = indices[i]

        artists = literal_eval(artists)
        artists_str = ""
        for artist in artists:
            artists_str = artists_str + artist + ", "
        artists_str = artists_str[:-2]
        arr[i] = [name, artists_str, index]
    return arr
    
@app.route("/test")
def test():
    return render_template("test.html")


if __name__ == "__main__":
    load_dotenv()
    # Use reco.search_name(<title of song>) to return DataFrame with index, title of song and artists.
    # Use reco.find_neighbors(<index>, <duration>) to return DataFrame of song recommendations with all columns.
    reco = Recommender()
    youtube = Youtube()
    if 'DYNO' in environ:
        app.run(debug=False, host='0.0.0.0', port=environ.get("PORT", 5000))
    else:
        app.run(debug=True, port=environ.get("PORT", 5000))
