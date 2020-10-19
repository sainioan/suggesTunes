from knn_recommender import Recommender
from flask import Flask, render_template, request
import string
import json

app = Flask(__name__)

def standardize(s):
    s = "".join([i.lower() for i in s if i not in frozenset(string.punctuation)])
    return s

@app.route("/")
def index():
    return render_template("home.html")

@app.route("/search", methods=["POST"])
def search():
    if request.method == "POST":
        # TODO user clicks song in list to return index of the track 
        duration = str(request.form.get("duration"))
        # TODO return neighbors (recommendations) in new page
    return duration

@app.route('/api', methods=['POST'])
def find_test():
    name = request.values.get('input')
    found = reco.search_name(name)
    # TODO format results in a better way
    result = found.to_json(orient="index")
    return result
    
@app.route("/test")
def test():
    return render_template("test.html")


if __name__ == "__main__":
    # Use reco.search_name(<title of song>) to return DataFrame with index, title of song and artists.
    # Use reco.find_neighbors(<index>, <duration>) to return DataFrame of song recommendations with all columns.
    reco = Recommender()
    app.run(debug=True)