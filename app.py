import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configuration de la page
st.set_page_config(page_title="EasyViz", layout="wide")

# Titre de l'application
st.title("📊 EasyViz : Visualisation de données simplifiée")
st.write("Téléversez un fichier CSV pour explorer et visualiser vos données rapidement.")

# Section pour téléverser le fichier CSV
uploaded_file = st.file_uploader("Téléversez un fichier CSV", type=["csv"])

if uploaded_file is not None:
    # Chargement des données
    try:
        data = pd.read_csv(uploaded_file)
        st.success("Fichier téléversé avec succès !")
        
        # Afficher les données
        st.subheader("Aperçu des données :")
        st.dataframe(data.head())
        
        # Afficher les statistiques descriptives
        st.subheader("Statistiques descriptives :")
        st.write(data.describe())

        # Sélectionner les colonnes pour la visualisation
        st.subheader("Créer une visualisation :")
        numeric_columns = data.select_dtypes(include=['number']).columns
        
        if len(numeric_columns) < 2:
            st.warning("Le fichier CSV doit contenir au moins deux colonnes numériques pour générer une visualisation.")
        else:
            x_axis = st.selectbox("Sélectionnez la colonne pour l'axe X", options=numeric_columns)
            y_axis = st.selectbox("Sélectionnez la colonne pour l'axe Y", options=numeric_columns)
            chart_type = st.radio("Type de graphique :", options=["Scatter Plot", "Line Plot", "Bar Plot"])

            # Créer un graphique en fonction des sélections
            if st.button("Générer le graphique"):
                fig, ax = plt.subplots(figsize=(10, 6))
                if chart_type == "Scatter Plot":
                    sns.scatterplot(data=data, x=x_axis, y=y_axis, ax=ax)
                elif chart_type == "Line Plot":
                    sns.lineplot(data=data, x=x_axis, y=y_axis, ax=ax)
                elif chart_type == "Bar Plot":
                    sns.barplot(data=data, x=x_axis, y=y_axis, ax=ax)

                st.pyplot(fig)
    except Exception as e:
        st.error(f"Erreur lors de la lecture du fichier : {e}")

else:
    st.info("Veuillez téléverser un fichier CSV pour commencer.")

# Pied de page
st.markdown("---")
st.markdown("Créé avec ❤️ par [Votre Nom ou Organisation]")