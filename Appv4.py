import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from io import BytesIO

# Configuration de la page
st.set_page_config(page_title="Easyviz", layout="wide")

# CSS pour ajouter un fond personnalisé
st.markdown(
    """
    <style>
    body {
        background-color: #f5f7fa; /* Couleur de fond */
        color: #333333; /* Couleur du texte */
    }
    .stApp {
        background-image: url('https://www.transparenttextures.com/patterns/white-paper.png');
        background-size: cover;
    }
    h1, h2, h3, h4 {
        color: #004080; /* Couleur des titres */
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Fonction pour télécharger des graphiques
def download_plot(fig, filename="graphique.png"):
    buf = BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    return buf

# Titre de l'application
st.title("📊 Easyviz")
st.markdown("""
<div style="display: flex; align-items: center;">
    <img src="https://www.canva.com/design/DAGdGuEF8eI/OMJfwjPF_obiNe7dAEnCvg/edit?utm_content=DAGdGuEF8eI&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton" >
    <h1 style="display: inline-block;">📊 EasyViz</h1>
</div>
""", unsafe_allow_html=True)
st.markdown("""
Bienvenue sur cette application de visualisation des données ! 
Téléversez un fichier CSV pour explorer et visualiser vos données.
""")

# Téléverser un fichier CSV
uploaded_file = st.file_uploader("📂 Téléversez un fichier CSV", type=["csv"])

if uploaded_file is not None:
    try:
        # Charger les données
        data = pd.read_csv(uploaded_file)
        st.success("Fichier téléversé avec succès !")
        
        # Aperçu des données
        st.subheader("Aperçu des données")
        st.dataframe(data.head(), use_container_width=True)
        
        # Colonnes disponibles
        all_columns = data.columns.tolist()
        numeric_columns = data.select_dtypes(include=["float64", "int64"]).columns.tolist()

        # Interface de sélection des axes
        with st.sidebar:
            st.header("Paramètres de visualisation")
            x_column = st.selectbox("Sélectionnez les données pour l'axe X :", all_columns, index=0)
            y_column = st.selectbox("Sélectionnez les données pour l'axe Y :", numeric_columns, index=0 if numeric_columns else -1)

        # Ajouter des onglets pour différents graphiques
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📈 Graphique de distribution",
            "📊 Scatterplot animé",
            "📉 Graphique en ligne animé",
            "📚 Pairplot",
            "🌀 Heatmap des corrélations"
        ])

        # 1. Graphique de distribution
        with tab1:
            st.subheader("📈 Graphique de distribution")
            if y_column:
                bins = st.slider("Nombre de classes (bins) :", min_value=5, max_value=50, value=10)
                fig, ax = plt.subplots()
                sns.histplot(data[y_column], kde=True, bins=bins, ax=ax)
                ax.set_title(f"Distribution de {y_column}")
                st.pyplot(fig)

                # Ajouter un bouton de téléchargement
                st.download_button(
                    label="Télécharger le graphique",
                    data=download_plot(fig),
                    file_name="distribution.png",
                    mime="image/png"
                )

        # 2. Scatterplot animé
        with tab2:
            st.subheader("📊 Scatterplot animé")
            if x_column and y_column:
                fig = px.scatter(
                    data, x=x_column, y=y_column,
                    animation_frame=x_column if x_column in numeric_columns else None,
                    title=f"Scatterplot : {y_column} vs {x_column}",
                    color=y_column if y_column in numeric_columns else None,
                    template="plotly_white"
                )
                st.plotly_chart(fig)

        # 3. Graphique en ligne animé
        with tab3:
            st.subheader("📉 Graphique en ligne animé")
            if x_column and y_column:
                fig = px.line(
                    data, x=x_column, y=y_column,
                    title=f"Graphique en ligne : {y_column} vs {x_column}",
                    markers=True,
                    template="plotly_white"
                )
                st.plotly_chart(fig)

        # 4. Pairplot
        with tab4:
            st.subheader("📚 Pairplot")
            pairplot_columns = st.multiselect(
                "Sélectionnez des colonnes pour le Pairplot (2 minimum) :", numeric_columns, default=numeric_columns[:2]
            )
            if len(pairplot_columns) >= 2:
                fig = sns.pairplot(data[pairplot_columns])
                st.pyplot(fig)

                # Ajouter un bouton de téléchargement
                st.download_button(
                    label="Télécharger le graphique",
                    data=download_plot(fig.fig),
                    file_name="pairplot.png",
                    mime="image/png"
                )

        # 5. Heatmap des corrélations
        with tab5:
            st.subheader("🌀 Heatmap des corrélations")
            if len(numeric_columns) > 1:
                fig, ax = plt.subplots(figsize=(10, 6))
                corr = data[numeric_columns].corr()
                sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)
                ax.set_title("Matrice de corrélation")
                st.pyplot(fig)

                # Ajouter un bouton de téléchargement
                st.download_button(
                    label="Télécharger le graphique",
                    data=download_plot(fig),
                    file_name="heatmap.png",
                    mime="image/png"
                )
    except Exception as e:
        st.error(f"Erreur lors de la lecture du fichier : {e}")
else:
    st.info("Veuillez téléverser un fichier CSV pour commencer.")            

# Pied de page
st.markdown("---")
st.markdown("Créé avec ❤️ par Jinshan LI,Karim OURDEDINE,Ines BEN MOUSSA,Moyi ZHANG")