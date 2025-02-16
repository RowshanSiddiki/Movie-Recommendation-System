import streamlit as st
import random
import pandas as pd

df_movies = pd.read_csv('clustered_movies.csv')

def recommend_movie(movie_name: str):
    movie_name = movie_name.strip().lower()
    
    # Ensure 'name' column is of string type before applying .str
    df_movies['name'] = df_movies['name'].astype(str).str.lower().str.strip()

    # Find the movie by name
    movie = df_movies[df_movies['name'].str.contains(movie_name, na=False)]

    if not movie.empty:
        cluster = movie['dbscan_clusters'].values[0]
        cluster_movies = df_movies[df_movies['dbscan_clusters'] == cluster]

        # Recommend movies based on the cluster
        if len(cluster_movies) >= 5:
            recommended_movies = random.sample(list(cluster_movies['name']), 5)
        else:
            recommended_movies = list(cluster_movies['name'])

        return recommended_movies
    else:
        return ["Movie not found"]

# --------------------- Streamlit app here -----------------------

st.title('Movies Recommendation System')
st.write("-"*20)

st.subheader('Supported Datasets')
st.write("Netflix TV Shows and Movies")
st.write("HBO Max TV Shows and Movies")
st.write("Amazon Prime TV Shows and Movies")

st.write("-"*20)

# Movie selection from the DataFrame
movie_name = df_movies['name'].values
movie_name = st.selectbox("Find your movie", options=movie_name, index=0, placeholder="Search for a movie")

# Recommend movies when button is pressed
if st.button("Recommend Movies"):
    st.write("Recommended Movies:")
    recommendation = recommend_movie(movie_name)
    st.write(recommendation)  # Display the recommendations as a list
