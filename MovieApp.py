import streamlit as st
import pandas as pd
import requests

url = "https://api.themoviedb.org/3/authentication"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI1ZWMyMGJhM2JhMDY3Y2MwMWI3ZjQ2ZGVkZTViYTQ0OCIsInN1YiI6IjY1NjIyMmJmN2RmZGE2NTkzMDRiMzU0ZSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.ZhSey6voKWvmjdL3NlLcSeCBdPFgEH2ur2xUNBuiXlU"
}

response = requests.get(url, headers=headers)

print(response.text)

# Charger les DataFrames
df_actors = pd.read_csv("actorsIdAndNames.csv", index_col=0)
df_actmov = pd.read_csv("actorsInFilmsTable.csv")
df_all = pd.read_csv("df_frenchComedies2000_all.csv", index_col=0)
df_directors = pd.read_csv("directorsTable.csv", index_col=0)
df_genres = pd.read_csv("tableGenresDesFilms.csv", index_col=0)

# Fusionner les tables en fonction des identifiants tconst, nconst, etc.
merged_df = pd.merge(df_all, df_actmov, on='tconst', how='inner')  # Fusionner avec les acteurs et films
merged_df = pd.merge(merged_df, df_actors, left_on='actor_id', right_on='nconst', how='inner')  # Fusionner avec les informations sur les acteurs
merged_df = pd.merge(merged_df, df_directors, on='tconst', how='inner')  # Fusionner avec les informations sur les réalisateurs
merged_df = pd.merge(merged_df, df_genres, on='tconst', how='inner')  # Fusionner avec les genres des films

merged_df

# Barre latérale pour la sélection
option = st.sidebar.radio('Sélectionner le critère de tri', ['Acteurs', 'Producteurs'])

if option == 'Acteurs':
    st.sidebar.header('Tri par Acteur')
    selected_actor = st.sidebar.selectbox('Sélectionner un acteur', merged_df['primaryName_y'].unique())
    # Filtrer les données en fonction de l'acteur sélectionné
    filtered_data = merged_df[merged_df['primaryName_y'] == selected_actor]
    st.dataframe(filtered_data)

elif option == 'Producteurs':
    st.sidebar.header('Tri par Producteur')
    selected_producer = st.sidebar.selectbox('Sélectionner un producteur', merged_df['primaryName_x'].unique())
    # Filtrer les données en fonction du producteur sélectionné
    filtered_data = merged_df[merged_df['primaryName_x'].apply(lambda x: selected_producer in x)]
    st.dataframe(filtered_data)

st.image('MovieApp.svg')

# Using object notation
add_selectbox = st.sidebar.selectbox(
    "How would you like to be contacted?",
    ("Email", "Home phone", "Mobile phone")
)

# Using "with" notation
with st.sidebar:
    add_radio = st.radio(
        "Choose a shipping method",
        ("Standard (5-15 days)", "Express (2-5 days)")
    )

# Onglet de recherche de films
def search_tab():
    st.title("Recherche de Films")
    
    # Ajoutez ici vos composants de recherche, résultats, etc.
    search_query = st.selectbox("Rechercher un film:", df_all['originalTitle'])
    if st.button("Rechercher"):
        # Logique de recherche et affichage des résultats
        st.write(f"Résultats de la recherche pour: {search_query}")

    df_all

# Onglet de gestion des profils utilisateur
def profile_tab():
    st.title("Gestion des Profils Utilisateur")
    
    # Ajoutez ici vos composants de gestion des profils, recommandations, etc.
    user_profile = st.text_input("Nom du Profil:")
    st.write(f"Profil sélectionné: {user_profile}")

# Définition des onglets
tabs = {"Recherche de Films": search_tab, "Profils Utilisateur": profile_tab}

# Barre de navigation pour sélectionner les onglets
selected_tab = st.sidebar.radio("Navigation", list(tabs.keys()))

# Afficher l'onglet sélectionné
tabs[selected_tab]()

