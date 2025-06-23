# from urllib import response
import streamlit as st
import pickle 
import pandas as pd
import requests




# def fetch_poster(movie_id):
#     url=f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=c5b1b8dd30c31f758048679c88d1c382&language=en-US"
#     # requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=c5b1b8dd30c31f758048679c88d1c382&language=en-US".format(movie_id))
#     response=requests.get(url)
#     data=response.json()

#     return "http://image.tmdb.org/t/p/w500/" + data['poster_path']

# import requests

# def fetch_poster(movie_id):
#     try:
#         url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=c5b1b8dd30c31f758048679c88d1c382&language=en-US"
#         response = requests.get(url)
#         data = response.json()
#         return "https://image.tmdb.org/t/p/w500" + data['poster_path']
#     except Exception as e:
#         print("Error fetching poster:", e)
#         return "https://via.placeholder.com/500x750?text=No+Image"

import requests

def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=599222c8d24e7e34890c3124c8fba881&language=en-US"
        response = requests.get(url)
        data = response.json()

        poster_path = data.get('poster_path')
        print(f"[DEBUG] movie_id: {movie_id}, poster_path: {poster_path}")

        if poster_path and poster_path != "null":
            return "https://image.tmdb.org/t/p/w500/" + poster_path
        else:
            return "https://via.placeholder.com/500x750?text=No+Image"
    except Exception as e:
        print(f"[ERROR] movie_id: {movie_id}, error: {e}")
        return "https://via.placeholder.com/500x750?text=Error"


def recommend(movie):
    movie_index = movies[movies['title']==movie].index[0]
    distances = similarity[movie_index]
    movies_list =sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]

    recommend_movies=[]
    recommend_movies_poster=[]

    for i in movies_list:
        try:
            movie_id=movies.iloc[i[0]].movie_id
            # fetch poster 
            print(f"[DEBUG] Trying movie ID: {movie_id}")
            recommend_movies.append(movies.iloc[i[0]].title)
            recommend_movies_poster.append(fetch_poster(movie_id))
        except Exception as e:
            print(f"[ERROR] Skipping movie due to bad Id : {e}")

    return recommend_movies,recommend_movies_poster
    


movies_dict = pickle.load(open('movie_dict.pkl','rb'))
movies=pd.DataFrame(movies_dict)

similarity=pickle.load(open('similarity.pkl','rb'))

st.title('Movie Recommendation System')

selected_movie_name =st.selectbox(
    'Select a movie to get recommendation: ',
   movies['title'].values
)

if st.button('Recommend'):
    names,poster = recommend(selected_movie_name)
    
    col1,col2,col3,col4,col5=st.columns(5)
    with col1:
        st.text(names[0])
        st.image(poster[0])
    with col2:
        st.text(names[1])
        st.image(poster[1])
    with col3:
        st.text(names[2])
        st.image(poster[2])
    with col4:
        st.text(names[3])
        st.image(poster[3])
    with col5:
        st.text(names[4])
        st.image(poster[4])


