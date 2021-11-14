#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 13 19:02:43 2021

@author: yiannimercer
"""

import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
import numpy as np    
from SECRETS import CLIENT_ID, CLIENT_SECRET
from spotipy.oauth2 import SpotifyClientCredentials






# Spotify Liked Songs Playlist to Dataset

def dataframe_tracks(results):
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               redirect_uri="https://example.com/callback",
                                               scope="user-library-read playlist-modify-public playlist-modify-private"))
    artists = []
    track_list = []
    ids = []
    liked_dates = []
    
    results = sp.current_user_saved_tracks()
    tracks = results['items']
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])

    for item in tracks:
        track_name = item['track']['name']
        track_list.append(track_name)
        
        artist_name = item['track']['artists'][0]['name']
        artists.append(artist_name)
        
        spotify_uri = item['track']['uri']
        ids.append(spotify_uri)
        
        date_liked = item['added_at']
        liked_dates.append(date_liked)
      
    data_dict = {"artist_name":artists,"track_name":track_list,"track_id":ids,"date_liked":liked_dates}
    df = pd.DataFrame(data = data_dict)
    return df

# Dataframe Function Creation
results = sp.current_user_saved_tracks()
df = dataframe_tracks(results)

# Cleaning the URI id column

df['track_id'] = df.apply(lambda x: x['track_id'].split(":")[-1],axis = 1)

df.drop_duplicates(subset = ['artist_name','track_name'],inplace = True)


# SpotifyFeatures Dataset

features = pd.read_csv("data_files/SpotifyFeatures.csv")

# Marking songs that I have favortied in Spotify Dataset

liked_df = features.copy()

features['same_artist'] = features.artist_name.isin(df.artist_name)
features['same_track'] = features.track_name.isin(df.track_name)
features['liked'] = np.where((features["same_artist"] == True) & (features["same_track"] == True), 1,0)
classified_df = features.drop(["same_artist", "same_track"], axis=1)
classified_df = classified_df.drop_duplicates(['artist_name','track_name'])
classified_df = pd.merge(classified_df,df[['track_name','artist_name','date_liked']],how = 'left',on=['track_name','artist_name'])
                   
# Cleaning Data Frame

classified_df.columns

## Casting as proper dtype 

num_cols = ['popularity','acousticness', 'danceability', 'duration_ms', 
            'energy', 'instrumentalness','liveness', 'loudness',
            'speechiness', 'tempo','valence', 'liked']

for col in num_cols:
    classified_df[col] = classified_df[col].astype(float)
    
classified_df['liked_date'] = pd.to_datetime(classified_df['date_liked'])
        
# Write to CSV

classified_df.to_csv("data_files/spotify_liked_final_df.csv")

