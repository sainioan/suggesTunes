import matplotlib
import pandas as pd
from flask import Flask, render_template, request
import numpy as np
from jedi.api.refactoring import inline
from sklearn.neighbors import NearestNeighbors
from ast import literal_eval
import string

# from PIL import Image
# import PIL.ImageOps
# import matplotlib.pyplot as plt

# from wordcloud import WordCloud


# %%
app = Flask(__name__)


# %%


def standardize(s):
    s = "".join([i.lower() for i in s if i not in frozenset(string.punctuation)])
    return s


@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "GET":
        return render_template("search.html")
    if request.method == "POST":
        name= str(request.form.get("name"))
        name = standardize(name)
        duration = str(request.form.get("duration"))
    return duration


@app.route("/")
def index():
    return render_template("home.html")


if __name__ == "__main__":
    app.run(debug=True)
df = pd.read_csv("songs_w_genres_v4.csv")
df.head()

df_data = df.drop(['artists', 'duration_ms', 'explicit', 'mode', 'name', 'popularity', 'release_date', 'year', 'genres',
                   'standardized_name'], axis=1)
df_data.index = df_data['id']
df_data = df_data.drop(['id'], axis=1)
df_data.head()

# %%

df_data['key'] = df_data['key'] / 12
max_loudness = df_data['loudness'].max()
df_data['loudness'] = abs(df_data['loudness'] / max_loudness)
max_tempo = df_data['tempo'].max()
df_data['tempo'] = df_data['tempo'] / max_tempo
df_data.head()

# %%

knn = NearestNeighbors(n_neighbors=50, algorithm='ball_tree')
knn.fit(df_data.values)


# %%

def standardize(s):
    s = "".join([i.lower() for i in s if i not in frozenset(string.punctuation)])
    return s


# %%

def matching_genres(genres1, genres2):
    genres1 = literal_eval(genres1)
    matches = list(set(genres1) & set(genres2))
    return len(matches) > 0


# %%

neighbors = 25000

max_duration = 360  # minutes
max_duration *= 60000  # to milliseconds


# %%

def recommend(id, model, duration):
    query = df_data.loc[id].to_numpy().reshape(1, -1)
    distances, indices = model.kneighbors(query, n_neighbors=neighbors)

    songs = df.loc[indices[0]].where(df['id'] != id).dropna()

    songs = songs.drop_duplicates(subset=['name', 'artists'])

    searched = df.where(df['id'] == id).dropna().head()
    genres = literal_eval(searched['genres'].values[0])

    if len(genres) > 0:
        songs = songs[songs['genres'].apply(matching_genres, args=([genres]))]

    duration *= 60000  # convert to milliseconds
    duration = duration if duration < max_duration else max_duration

    count = songs[songs['duration_ms'].cumsum() < duration]['id'].count()
    songs = songs.head(count + 1)

    print(songs[['name', 'artists']])

    return songs


# %%

def index_input():
    good_input = 0
    ind = input('Enter the index value of the required song: ')
    while not good_input:
        if not ind.isdigit():
            ind = input('Index has to be a number, please try again: ')
            continue
        ind = int(ind)
        if not ind <= df['id'].count():
            ind = input('Index has to be smaller than 169910. Please try again: ')
            continue
        good_input = 1
    return ind


# %%

def duration_input():
    duration = input('Enter duration of playlist in minutes: ')
    while not duration.isdigit():
        duration = input('Duration has to be a number (Leave out the word minutes). Please try again: ')
    return duration


# %%

name = search()
name = standardize(name)

duration = int(duration_input())

found = df[['name', 'artists', 'popularity']].where(df['standardized_name'].str.contains(name)).dropna().sort_values(
    ascending=False, by="popularity")
while found.empty:
    name = input('No songs found with that title. Enter a new song title.')
    name = standardize(name)
    found = df[['name', 'artists', 'popularity']].where(
        df['standardized_name'].str.contains(name)).dropna().sort_values(ascending=False, by="popularity")
found = found[['name', 'artists']]
print('Search results: \n', found)

ind = index_input()
id = df['id'].loc[ind]

song = df['name'].loc[ind]
artists = df['artists'].loc[ind]

print('\nSearching for', song, 'by', artists)

songs = recommend(id, knn, duration)

# %%

searched = df.where(df['id'] == id).dropna().head()

pd.concat([searched, songs]).head()

# %%


# again empty space
