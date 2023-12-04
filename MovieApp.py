import streamlit as st
import pandas as pd
import requests
from sklearn.neighbors import NearestNeighbors
from translate import Translator


# Set Streamlit to wide mode
st.set_page_config(layout="wide")

# Link the CSS file
st.markdown(
    f'<style>{open("styles.css").read()}</style>',
    unsafe_allow_html=True
)

df_test = pd.read_csv("df_test2_list.csv")

# Image de fond
st.image('MovieApp2.svg')

# Api tmdb - clef
url = "https://api.themoviedb.org/3/authentication"
headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI1ZWMyMGJhM2JhMDY3Y2MwMWI3ZjQ2ZGVkZTViYTQ0OCIsInN1YiI6IjY1NjIyMmJmN2RmZGE2NTkzMDRiMzU0ZSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.ZhSey6voKWvmjdL3NlLcSeCBdPFgEH2ur2xUNBuiXlU"
}
response = requests.get(url, headers=headers)
print(response.text)


# Dictionnaire des genres
genre_mapping = {
    '28': 'Action',
    '12': 'Adventure',
    '16': 'Animation',
    '35': 'Comedy',
    '80': 'Crime',
    '99': 'Documentary',
    '18': 'Drama',
    '10751': 'Family',
    '14': 'Fantasy',
    '36': 'History',
    '27': 'Horror',
    '10402': 'Music',
    '9648': 'Mystery',
    '10749': 'Romance',
    '878': 'Science Fiction',
    '10770': 'TV Movie',
    '53': 'Thriller',
    '10752': 'War',
    '37': 'Western'
}

st.markdown("<h1 style='color:#FF5757;'>Recherche de Films</h1>", unsafe_allow_html=True)
    
    # Ajoutez ici vos composants de recherche, résultats, etc.
liste_films = df_test['Movie_Title']
search_query = st.selectbox("J'aimerais voir un film similaire à:", liste_films, index=None, placeholder="Saisissez le titre d'un film que vous avez aimé")
weight_option = st.selectbox("J'aimerais essentiellement retrouver:", ['Les réalisateurs', 'Les acteurs', 'Le genre', 'Un peu tout !'])
  
# Initialiser le traducteur une seule fois en dehors de la boucle
translator_similar = Translator(to_lang='fr')

if st.button("Rechercher"):
    # Utiliser le film choisi comme variable
    film = search_query

        # Get the IMDb ID of the selected movie
    selected_movie_index = df_test.index[df_test['Movie_Title'] == film].tolist()

    if selected_movie_index:
        selected_movie_index = selected_movie_index[0]
        selected_movie = df_test.iloc[selected_movie_index]
        imdb_id_selected = selected_movie['ID']

        # Call the TMDB API to get information about the selected movie
        tmdb_url_selected = f"https://api.themoviedb.org/3/find/{imdb_id_selected}?external_source=imdb_id"
        tmdb_response_selected = requests.get(tmdb_url_selected, headers=headers)

        col1_selected, col2_selected, col3_selected= st.columns([2, 1, 4])


        if tmdb_response_selected.status_code == 200:
            tmdb_data_selected = tmdb_response_selected.json()
            selected_movie_data = tmdb_data_selected['movie_results'][0]

            # Translate the overview from English to French
            english_summary_selected = selected_movie_data['overview']
            chunk_size_selected = 400
            chunks_selected = [english_summary_selected[i:i + chunk_size_selected] for i in range(0, len(english_summary_selected), chunk_size_selected)]
            french_summary_selected = " ".join(translator_similar.translate(chunk) for chunk in chunks_selected)

            with col1_selected:
            # Display details of the selected movie
                st.image(f"https://image.tmdb.org/t/p/w500/{selected_movie_data['poster_path']}", use_column_width=True)
                st.title(f"{selected_movie['Movie_Title']}")
                st.markdown(f"<span style='color:#FF5757'>Date de sortie:</span> {selected_movie_data['release_date']}", unsafe_allow_html=True)
                genre_ids_selected = selected_movie_data['genre_ids']
                genre_names_selected = [genre_mapping.get(str(genre_id), '') for genre_id in genre_ids_selected]
                st.markdown(f"<span style='color:#FF5757'>Genres:</span> {', '.join(genre_names_selected)}", unsafe_allow_html=True)
                st.markdown(f"<span style='color:#FF5757'>Note moyenne:</span> {selected_movie_data['vote_average']}", unsafe_allow_html=True)
                st.markdown(f"<span style='color:#FF5757'>Popularité:</span> {selected_movie_data['popularity']}", unsafe_allow_html=True)
                st.write(f"{french_summary_selected}")

        else:
            st.warning(f"Impossible de récupérer les informations du film sélectionné à partir de l'API TMDB.")
    
    from sklearn.preprocessing import MultiLabelBinarizer
    import numpy as np

    # factorisation des listes en une seule variable (de liste)
    if weight_option == 'Un peu tout !':
        mlb = MultiLabelBinarizer()
        genres_binarized= mlb.fit_transform(df_test['Movie_Genres'])*1.5
        actors_binarized= mlb.fit_transform(df_test['Actors_Name'])*1.1
        directors_binarized= mlb.fit_transform(df_test['Directors_Name'])*1.3
        year_np= np.array(df_test['Movie_Year']).reshape(-1, 1)

    if weight_option == 'Les réalisateurs':
        mlb = MultiLabelBinarizer()
        genres_binarized= mlb.fit_transform(df_test['Movie_Genres'])*1.3
        actors_binarized= mlb.fit_transform(df_test['Actors_Name'])*1.1
        directors_binarized= mlb.fit_transform(df_test['Directors_Name'])*1.5
        year_np= np.array(df_test['Movie_Year']).reshape(-1, 1)

    if weight_option == 'Les acteurs':
        mlb = MultiLabelBinarizer()
        genres_binarized= mlb.fit_transform(df_test['Movie_Genres'])*1.3
        actors_binarized= mlb.fit_transform(df_test['Actors_Name'])*1.5
        directors_binarized= mlb.fit_transform(df_test['Directors_Name'])*1.1
        year_np= np.array(df_test['Movie_Year']).reshape(-1, 1)

    if weight_option == 'Le genre':
        mlb = MultiLabelBinarizer()
        genres_binarized= mlb.fit_transform(df_test['Movie_Genres'])*1.7
        actors_binarized= mlb.fit_transform(df_test['Actors_Name'])*1.2
        directors_binarized= mlb.fit_transform(df_test['Directors_Name'])*1.2
        year_np= np.array(df_test['Movie_Year']).reshape(-1, 1)

    numerics_variable = np.hstack((genres_binarized, actors_binarized, directors_binarized, year_np))

    # initialiser et entrainer modèle de nearest neighbors
    from sklearn.neighbors import NearestNeighbors
    from sklearn.metrics.pairwise import cosine_similarity
    X = numerics_variable
    modelNN = NearestNeighbors(n_neighbors = 4, metric='cosine', algorithm='brute')
    modelNN.fit(X)

    index_film = df_test.index[df_test['Movie_Title'].str.contains(film)]

    distances, indices = modelNN.kneighbors(numerics_variable[index_film])
    # Boucle pour afficher les films similaires
    for i in range(3):
        similar_movie_index = indices[0][i+1]
        similar_movie = df_test.iloc[similar_movie_index]
        
        # Obtenir l'ID IMDb du film similaire
        imdb_id_similar = similar_movie['ID']

        # Appeler l'API TMDB pour obtenir les informations du film similaire
        tmdb_url_similar = f"https://api.themoviedb.org/3/find/{imdb_id_similar}?external_source=imdb_id"
        tmdb_response_similar = requests.get(tmdb_url_similar, headers=headers)

        if tmdb_response_similar.status_code == 200:
            tmdb_data_similar = tmdb_response_similar.json()

            # Traduire le résumé de l'anglais au français pour le film similaire
            english_summary_similar = tmdb_data_similar['movie_results'][0]['overview']

            # Split the text into chunks to avoid exceeding the character limit
            chunk_size_similar = 400  # Adjust the chunk size as needed
            chunks_similar = [english_summary_similar[i:i + chunk_size_similar] for i in range(0, len(english_summary_similar), chunk_size_similar)]

            # Translate each chunk and concatenate the results
            french_summary_similar = " ".join(translator_similar.translate(chunk) for chunk in chunks_similar)

            # Display title, image, and details in a single column

            with col3_selected:
                col_1, col_2 = st.columns([1, 1])
                with col_1:
                    st.image(f"https://image.tmdb.org/t/p/w500/{tmdb_data_similar['movie_results'][0]['poster_path']}", use_column_width=True)

                with col_2:
                    st.title(f"{similar_movie['Movie_Title']}")
                    st.markdown(f"<span style='color:#FF5757'>Date de sortie:</span> {tmdb_data_similar['movie_results'][0]['release_date']}", unsafe_allow_html=True)
                    genre_ids_similar = tmdb_data_similar['movie_results'][0]['genre_ids']
                    genre_names_similar = [genre_mapping.get(str(genre_id), '') for genre_id in genre_ids_similar]
                    st.markdown(f"<span style='color:#FF5757'>Genres:</span> {', '.join(genre_names_similar)}", unsafe_allow_html=True)
                    st.markdown(f"<span style='color:#FF5757'>Note moyenne:</span> {tmdb_data_similar['movie_results'][0]['vote_average']}", unsafe_allow_html=True)
                    st.markdown(f"<span style='color:#FF5757'>Popularité:</span> {tmdb_data_similar['movie_results'][0]['popularity']}", unsafe_allow_html=True)
                    st.write(f"{french_summary_similar}")

        else:
            st.warning(f"Impossible de récupérer les informations du film similaire {similar_movie['Movie_Title']} à partir de l'API TMDB.")
