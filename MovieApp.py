import streamlit as st
import pandas as pd

df = pd.read_csv('df_test2_list.csv')
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
    search_query = st.selectbox("Rechercher un film:", df['Movie_Title'])
    if st.button("Rechercher"):
        # Logique de recherche et affichage des résultats
        st.write(f"Résultats de la recherche pour: {search_query}")
        
    df

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

