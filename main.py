import pandas as pd
import streamlit as st
import pickle
import requests

movies_list = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))
movies = pd.DataFrame(movies_list)
movies_title_list = movies['title'].values

def fetch_posters(movie_id):
     response = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US")
     data = response.json()
     return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

def recommend(movie):
     movie_index = movies[movies['title'] == movie].index[0]
     distances = similarity[movie_index]
     recommended_movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
     recommended_movies = []
     recommended_movies_posters = []
     for i in recommended_movies_list:
          recommended_movies.append(movies.iloc[i[0]].title)
          recommended_movies_posters.append(fetch_posters(movies.iloc[i[0]].id))
     return recommended_movies,recommended_movies_posters


st.title('Movie Recommender System')
option = st.selectbox(
     'How would you like to be contacted?',
     movies_title_list)
if st.button('Recommend'):
     names,posters = recommend(option)
     col1, col2, col3, col4, col5 = st.columns(5)
     with col1:
          st.text(names[0])
          st.image(posters[0])
     with col2:
          st.text(names[1])
          st.image(posters[1])
     with col3:
          st.text(names[2])
          st.image(posters[2])
     with col4:
          st.text(names[3])
          st.image(posters[3])
     with col5:
          st.text(names[4])
          st.image(posters[4])

