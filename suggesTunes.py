from knn_recommender import Recommender
from flask import Flask, render_template, request
from ast import literal_eval
import string
import json

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
        songs_arr = dict()
        index = int(request.form.get("index"))
        duration = int(request.form.get("duration"))
        songs = reco.find_neighbors(index, duration)
        vals = songs.values.tolist()
        for i in range(len(songs.values)):
            print(songs['name'])
            break
            songs_arr[i] = vals[i]
        return render_template("results.html", songs_arr=songs_arr)

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
    # Use reco.search_name(<title of song>) to return DataFrame with index, title of song and artists.
    # Use reco.find_neighbors(<index>, <duration>) to return DataFrame of song recommendations with all columns.
    reco = Recommender()
    app.run(debug=True)