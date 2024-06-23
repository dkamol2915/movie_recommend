# -*- coding: utf-8 -*-
"""movie recommend.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1BbAZldwtSDWfQmwAN1QWGwNWGIGJDns2
"""

import numpy as np
import pandas as pd

movies = pd.read_csv('/content/tmdb_5000_movies.csv')
credits = pd.read_csv('/content/tmdb_5000_credits.csv')

movies.head()

credits.head(2)

movies = movies.merge(credits,on = 'title')

movies.head(1)

movies = movies[['movie_id','title','overview','genres','keywords','cast','crew']]

movies.head(1)

movies.isnull().sum()

movies.dropna(inplace=True)

movies.isnull().sum()

movies.duplicated().sum()

import ast
ast.literal_eval('[{"id": 28, "name": "Action"}, {"id": 12, "name": "Adventure"}, {"id": 14, "name": "Fantasy"}, {"id": 878, "name": "Science Fiction"}]')

def convert(obj):
  L =[]
  for i in ast.literal_eval(obj):
      L.append(i['name'])
  return L

movies['genres'] = movies['genres'].apply(convert)

movies.head()

movies['keywords'] = movies['keywords'].apply(convert)

movies.head()

movies['cast'][0]

def convert2(obj):
  L =[]
  counter = 0
  for i in ast.literal_eval(obj):
      if counter != 3:
         L.append(i['name'])
         counter+=1
      else:
          break
  return L

movies['cast'] = movies['cast'].apply(convert2)

movies.head()

def fetch_director(obj):
    L =[]
    for i in ast.literal_eval(obj):
        if i['job'] == 'Director':
            L.append(i['name'])
            break
    return L

movies['crew'] = movies['crew'].apply(fetch_director)

movies.head()

movies['overview'][0]

movies['overview'] = movies['overview'].apply(lambda x:x.split())

movies.head()

movies['genres'] = movies['genres'].apply(lambda x:[i.replace(" ", "") for i in x])
movies['keywords'] = movies['keywords'].apply(lambda x:[i.replace(" ", "") for i in x])
movies['cast'] = movies['cast'].apply(lambda x:[i.replace(" ", "") for i in x])
movies['crew'] = movies['crew'].apply(lambda x:[i.replace(" ", "") for i in x])

movies.head()

movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']

movies.head()

new_df = movies[['movie_id','title', 'tags']]

new_df

new_df['tags'] = new_df['tags'].apply(lambda x:" ".join(x))

new_df.head()

!pip install nltk

import nltk

from nltk.stem.porter import PorterStemmer
ps = PorterStemmer()

def stem(text):
    y = []

    for i in text.split():
         y.append(ps.stem(i))
    return " ".join(y)

new_df['tags'] = new_df['tags'].apply(stem)

from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(max_features=5000,stop_words='english')

vector = cv.fit_transform(new_df['tags']).toarray()

vector

vector[0]

cv.get_feature_names_out()

from sklearn.metrics.pairwise import cosine_similarity

similarity = cosine_similarity(vector)

similarity

sorted(list(enumerate(similarity[0])),reverse=True,key = lambda x: x[1])[1:6]

def recommend(movie):
   movie_index = new_df[new_df['title'] == movie].index[0]
   distances = similarity[movie_index]
   movies_list = sorted(list(enumerate(similarity[0])),reverse=True,key = lambda x: x[1])[1:6]
   for i in movies_list:
        print(new_df.iloc[i[0]].title)

recommend('Avatar')

