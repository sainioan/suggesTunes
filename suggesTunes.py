from knn_recommender import Recommender
from flask import Flask, render_template, request
import string

app = Flask(__name__)

def standardize(s):
    s = "".join([i.lower() for i in s if i not in frozenset(string.punctuation)])
    return s

@app.route("/search", methods=["POST"])
def search():
    if request.method == "POST":
        name= str(request.form.get("name"))
        name = standardize(name)
        found = reco.search_name(name)
        # TODO return list of song titles and artists based on similarity of searched name
        # TODO user clicks song in list to return index of the track -> find id of the track 
        duration = str(request.form.get("duration"))
        # TODO return neighbors (recommendations) in new page
    return duration


@app.route("/")
def index():
    return render_template("home.html")


if __name__ == "__main__":
    # Use reco.search_name(<title of song>) to return DataFrame with index, title of song and artists.
    # Use reco.find_id(<index>) to return id of searched song.
    # Use reco.find_neighbors(<id>, <duration>) to return DataFrame of song recommendations with all columns.
    reco = Recommender()
    app.run(debug=True)