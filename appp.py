import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configuration de la page
st.set_page_config(page_title="Visualisation des données", layout="wide")

# Titre de l'application
st.title("📊 Visualisation des données interactives")
st.markdown("""
Bienvenue sur cette application de visualisation des données ! 
Téléversez un fichier CSV pour explorer et visualiser vos données à l'aide de différents graphiques interactifs.
""")

# Téléverser un fichier CSV
uploaded_file = st.file_uploader("📂 Téléversez un fichier CSV", type=["csv"])

if uploaded_file is not None:
    # Charger les données
    data = pd.read_csv(uploaded_file)
    
    # Aperçu des données
    st.subheader("Aperçu des données")
    st.dataframe(data.head(), use_container_width=True)
    
    # Choisir une colonne pour les graphiques
    numeric_columns = data.select_dtypes(include=["float64", "int64"]).columns
    if len(numeric_columns) == 0:
        st.warning("Aucune colonne numérique trouvée pour la visualisation.")
    else:
        with st.sidebar:
            st.header("Paramètres de visualisation")
            selected_column = st.selectbox("Sélectionnez une colonne numérique :", numeric_columns)
        
        # Ajouter des onglets pour différents graphiques
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📈 Graphique de distribution",
            "📊 Boxplot",
            "📉 Graphique en ligne",
            "📚 Pairplot",
            "🌀 Heatmap des corrélations"
        ])

        # 1. Graphique de distribution
        with tab1:
            st.subheader("📈 Graphique de distribution")
            bins = st.slider("Nombre de classes (bins) :", min_value=5, max_value=50, value=10)
            fig, ax = plt.subplots()
            sns.histplot(data[selected_column], kde=True, bins=bins, ax=ax)
            ax.set_title(f"Distribution de {selected_column}")
            st.pyplot(fig)

        # 2. Boxplot
        with tab2:
            st.subheader("📊 Boxplot")
            fig, ax = plt.subplots()
            sns.boxplot(x=data[selected_column], ax=ax, color="skyblue")
            ax.set_title(f"Boxplot de {selected_column}")
            st.pyplot(fig)

        # 3. Graphique en ligne
        with tab3:
            st.subheader("📉 Graphique en ligne")
            fig, ax = plt.subplots()
            data[selected_column].plot(kind="line", ax=ax, color="purple")
            ax.set_title(f"Graphique en ligne pour {selected_column}")
            st.pyplot(fig)

        # 4. Pairplot
        with tab4:
            st.subheader("📚 Pairplot")
            pairplot_columns = st.multiselect(
                "Sélectionnez des colonnes pour le Pairplot (2 minimum) :", numeric_columns, default=numeric_columns[:2]
            )
            if len(pairplot_columns) < 2:
                st.warning("Veuillez sélectionner au moins deux colonnes.")
            else:
                fig = sns.pairplot(data[pairplot_columns])
                st.pyplot(fig)

        # 5. Heatmap des corrélations
        with tab5:
            st.subheader("🌀 Heatmap des corrélations")
            fig, ax = plt.subplots(figsize=(10, 6))
            corr = data.corr()
            sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)
            ax.set_title("Matrice de corrélation")
            st.pyplot(fig)