import pandas as pd
import streamlit as st
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image
import os
from streamlit.components.v1 import html
from streamlit_extras.switch_page_button import switch_page

def rh_page():
    st.title("Datavisualisation du Département RH")
    
    script_directory = os.path.dirname(os.path.abspath(__file__))
    # Combine le chemin du script avec le chemin relatif du fichier Excel
    excel_file_path = os.path.join(script_directory, 'data', 'Akigora_data.xlsx')
    DFexp0 = pd.read_excel(excel_file_path, sheet_name='Collection Experts')
    DFexp1= pd.DataFrame()
    DFexp1=DFexp0.copy()
    DFexp2= pd.DataFrame()
    DFexp3= pd.DataFrame()
    DFexp4= pd.DataFrame()
    DFexp5= pd.DataFrame()
    
    DFexp1['linkedInImport'] = DFexp0['linkedInImport'].fillna(0).astype(bool) #NaN = 0, changement de float a Booleen

    seuil_non_nullite = int(0.85 * len(DFexp0))
    DFexp2 = DFexp0
    DFexp2 = DFexp2.dropna(axis=1, thresh=seuil_non_nullite)


    DFexp0['visible'].astype(bool)
    DFexp3 = DFexp2
    DFexp3 = DFexp3.dropna(subset=['Created'])
    DFexp3 = DFexp3.sort_values(by='Created', ascending=True)
    Expert_grouped = DFexp3.groupby('Created').size()
    DFgrouped = pd.DataFrame(Expert_grouped)
    st.write(DFgrouped)
    counts_by_interval = DFgrouped.groupby(pd.Grouper(freq='6M')).size()
    cumulative_counts_by_interval = counts_by_interval.cumsum()

    start_date = DFexp3['Created'].min()
    end_date = DFexp3['Created'].max()

    Nb_experts = DFexp0.shape[0]

    # Nombre d'experts visibles
    nb_visible = sum(DFexp0['visible']==1.0)
    nb_tempo_invisible = sum(DFexp0['temporarilyInvisible']==1.0)

    # Profils d'expert remplis à 100%
    profil_remplis = sum(DFexp0['percentage']==100) / 2455
    prct_profil_remplis = round(profil_remplis * 100, 2)
    profil_incomplet = sum(DFexp0['percentage'] !=100)
    
    #Les domaines
    Domains = DFexp0['domains'].unique()
    Domains_grouped = DFexp0.groupby('domains').size()
    Domains_grouped_sorted = Domains_grouped.sort_values(ascending=False)
    Domains_prct = round((DFexp0['domains'].dropna().value_counts(normalize=True)*100), 2)

    # Définir les couleurs
    couleur_info_box = "#87CEEB"  # Ciel léger
    couleur_card = "#F0FFFF"  # Azur clair

    # Afficher les informations avec des éléments visuels
    st.info("### Statistiques des experts sur la plateforme")
    # Sélection de la visualisation
    selected_visualization = st.selectbox("Sélectionnez la visualisation :", ["Visualisation 1", "Visualisation 2", "Visualisation 3"])
    # Affichage du nombre d'experts inscrits
    if selected_visualization == "Visualisation 1":
        st.info(f"Nombre d'experts inscrits : {DFexp1.shape[0]}")
        # Affichage du nombre d'experts visibles
        st.success(f"Nombre d'experts visibles : {sum(DFexp0['visible']==1.0)}")
    
        # Diagramme circulaire pour illustrer le pourcentage de profils remplis
        fig, ax = plt.subplots(figsize=(2, 2))  # Taille réduite
        colors = ['#02A865', '#A4d1AE']  # couleur akigora
        ax.pie([prct_profil_remplis, 100 - prct_profil_remplis], labels=['Remplis à 100%', 'Non remplis à 100%'], autopct='%1.1f%%', startangle=90, colors=colors)
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        st.pyplot(fig)

    if selected_visualization == "Visualisation 2":
        fig, axs = plt.subplots(1, 2, figsize=(15, 6))

        # Tracer le premier graphique (cumulatif)
        axs[0].plot(cumulative_counts_by_interval.index, cumulative_counts_by_interval.values, linestyle='-', color='b', marker='o')
        axs[0].set_title('Évolution cumulatif du nombre d\'experts')
        axs[0].set_xlabel('Tranche de 6 mois')
        axs[0].set_ylabel('Nombre d\'experts')
        axs[0].tick_params(axis='x', rotation=45)  # Rotation des dates pour une meilleure lisibilité

        # Tracer le deuxième graphique (non cumulatif)
        axs[1].plot(counts_by_interval.index, counts_by_interval.values, linestyle='-', color='r', marker='o')
        axs[1].set_title('Évolution non cumulatif du nombre d\'experts')
        axs[1].set_xlabel('Tranche de 6 mois')
        axs[1].set_ylabel('Nombre d\'experts')
        axs[1].tick_params(axis='x', rotation=45)
           
        selected_date_range = st.slider('**Sélectionner la plage de dates**',
                                            min_value=start_date.timestamp(),
                                            max_value=end_date.timestamp(),
                                            value=(start_date, end_date),
                                            format="YYYY/MM/DD")
           #filters_date = start_date >= selected_date_range[0]&end_date <= selected_date_range[1]    
        fig, axs = plt.subplots(1, 2, figsize=(15, 6))
         # Tracer le premier graphique (cumulatif)
        axs[0].plot(cumulative_counts_by_interval.index, cumulative_counts_by_interval.values, linestyle='-', color='b', marker='o')
        axs[0].set_title('Évolution cumulatif du nombre d\'experts')
        axs[0].set_xlabel('Tranche de 6 mois')
        axs[0].set_ylabel('Nombre d\'experts')
        axs[0].tick_params(axis='x', rotation=45)  # Rotation des dates pour une meilleure lisibilité
        # Tracer le deuxième graphique (non cumulatif)
        axs[1].plot(counts_by_interval.index, counts_by_interval.values, linestyle='-', color='r', marker='o')
        axs[1].set_title('Évolution non cumulatif du nombre d\'experts')
        axs[1].set_xlabel('Tranche de 6 mois')
        axs[1].set_ylabel('Nombre d\'experts')
        axs[1].tick_params(axis='x', rotation=45)  # Rotation des dates pour une meilleure lisibilité
        st.pyplot(fig)



def marketing_page():
    st.title("Département Marketing")
    # Votre contenu pour le département Marketing ici

def technique_page():
    st.title("Département Technique")
    # Votre contenu pour le département Technique ici

def direction_page():
    st.title("Département Direction")
    # Votre contenu pour le département Direction ici

def commerce_page():
    st.title("Département Commerce")
    # Votre contenu pour le département Commerce ici


def home_page():
    st.title("Bienvenue sur votre Dashboard AKIGORA")
    # Définir les icônes pour chaque département
    icons = {
        "Ressources Humaines": "👥",
        "Marketing": "📈",
        "Technique": "⚙️",
        "Direction": "📊",
        "Commerce": "💼"
    }
    def logo():
        image_path = "C:\\Users\\simplon\\Desktop\\Projet_Akigora\\Akigora_code\\Logo_Akigora.png"
        original_image = Image.open(image_path)
        st.image(original_image, width=500, caption="")
    
    logo()
    st.write("Vos département :")
    
    # Utiliser une disposition de colonnes pour aligner horizontalement les boutons
    col1, col2, col3, col4, col5 = st.columns(5)

    # Boutons pour chaque département avec des icônes


    # Cases pour chaque département avec des icônes et couleur de fond
    for departement, icon in icons.items():
        if departement == "Ressources Humaines":
            col1.markdown(
                f"""<div style='text-align: center; background-color: #02a865; padding: 10px; border-radius: 10px;'>
                    <strong>{departement}</strong>  <br> {icon}
                </div>""",
                unsafe_allow_html=True
            )
        elif departement == "Marketing":
            col2.markdown(
                f"""<div style='text-align: center; background-color: #02a865; padding: 10px; border-radius: 10px;'>
                    <strong>{departement}</strong>  <br> {icon}
                </div>""",
                unsafe_allow_html=True
            )
        elif departement == "Technique":
            col3.markdown(
                f"""<div style='text-align: center; background-color: #02a865; padding: 10px; border-radius: 10px;'>
                    <strong>{departement}</strong>  <br> {icon}
                </div>""",
                unsafe_allow_html=True
            )
        elif departement == "Direction":
            col4.markdown(
                f"""<div style='text-align: center; background-color: #02a865; padding: 10px; border-radius: 10px;'>
                    <strong>{departement}</strong>  <br> {icon}
                </div>""",
                unsafe_allow_html=True
            )
        elif departement == "Commerce":
            col5.markdown(
                f"""<div style='text-align: center; background-color: #02a865; padding: 10px; border-radius: 10px;'>
                    <strong>{departement}</strong>  <br> {icon}
                </div>""",
                unsafe_allow_html=True
            )


# Fonction principale pour gérer la navigation entre les pages
def main():
    st.sidebar.title("Menu")
    pages = ["Accueil", "RH", "Marketing", "Technique", "Direction", "Commerce"]
    selected_page = st.sidebar.selectbox("Sélectionnez une page", pages)

    if selected_page == "Accueil":
        home_page()
    elif selected_page == "RH":
        rh_page()
    elif selected_page == "Marketing":
        marketing_page()
    elif selected_page == "Technique":
        technique_page()
    elif selected_page == "Direction":
        direction_page()
    elif selected_page == "Commerce":
        commerce_page()

if __name__ == "__main__":
    main()
