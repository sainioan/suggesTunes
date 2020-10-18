import pandas as pd
from flask import Flask, render_template, request
import numpy as np
from sklearn.neighbors import NearestNeighbors
from ast import literal_eval

class Recommender: 
    def __init__(self):
        self.neighbors = 25000
        self.max_duration = 360  # minutes
        self.max_duration *= 60000  # to milliseconds
        self.df = pd.read_csv("songs_w_genres_v4.csv")

        # Drop unused columns and make "id" the index
        self.df_data = self.df.drop(['artists', 'duration_ms', 'explicit', 'mode', 'name', 
            'popularity', 'release_date', 'year', 'genres', 'standardized_name'], axis=1)
        self.df_data.index = self.df_data['id']
        self.df_data = self.df_data.drop(['id'], axis=1)

        # Normalize values
        self.df_data['key'] = self.df_data['key'] / 12
        max_loudness = self.df_data['loudness'].max()
        self.df_data['loudness'] = abs(self.df_data['loudness'] / max_loudness)
        max_tempo = self.df_data['tempo'].max()
        self.df_data['tempo'] = self.df_data['tempo'] / max_tempo

        self.knn = NearestNeighbors(n_neighbors=50, algorithm='ball_tree')
        self.knn.fit(self.df_data.values)

    # def index_input():
        # good_input = 0
        # ind = input('Enter the index value of the required song: ')
        # while not good_input:
            # if not ind.isdigit():
                # ind = input('Index has to be a number, please try again: ')
                # continue
            # ind = int(ind)
            # if not ind <= df['id'].count():
                # ind = input('Index has to be smaller than 169910. Please try again: ')
                # continue
            # good_input = 1
        # return ind


    # def duration_input():
        # duration = input('Enter duration of playlist in minutes: ')
        # while not duration.isdigit():
            # duration = input('Duration has to be a number (Leave out the word minutes). Please try again: ')
        # return duration

    def matching_genres(genres1, genres2):
        genres1 = literal_eval(genres1)
        matches = list(set(genres1) & set(genres2))
        return len(matches) > 0

    def recommend(id, model, duration):
        query = self.df_data.loc[id].to_numpy().reshape(1, -1)
        distances, indices = model.kneighbors(query, n_neighbors=neighbors)

        songs = self.df.loc[indices[0]].where(self.df['id'] != id).dropna()

        songs = songs.drop_duplicates(subset=['name', 'artists'])

        searched = self.df.where(self.df['id'] == id).dropna().head()
        genres = literal_eval(searched['genres'].values[0])

        if len(genres) > 0:
            songs = songs[songs['genres'].apply(matching_genres, args=([genres]))]

        duration *= 60000  # convert to milliseconds
        duration = duration if duration < max_duration else max_duration

        count = songs[songs['duration_ms'].cumsum() < duration]['id'].count()
        songs = songs.head(count + 1)

        print(songs[['name', 'artists']])

        return songs

    def search_name(self, name):
        found = self.df[['name', 'artists', 'popularity']].where(self.df['standardized_name']
            .str.contains(name)).dropna().sort_values(ascending=False, by="popularity")
        # while found.empty:
            # name = input('No songs found with that title. Enter a new song title.')
            # name = standardize(name)
        if not found.empty:
            found = self.df[['name', 'artists', 'popularity']].where(self.df['standardized_name'].
                str.contains(name)).dropna().sort_values(ascending=False, by="popularity")
            found = found[['name', 'artists']]

        return found

    def find_id(self, index):
        id = self.df['id'].loc[index]
        return id


    def find_neighbors(self, id, duration):
        songs = recommend(id, self.knn, duration)
        return songs

    

