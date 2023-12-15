import pandas as pd
import streamlit as st
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image
import os


# Ajoutez la classe "wide" pour élargir la page
st.markdown('<style>.wide { max-width: 1200px; margin: 0 auto; }</style>', unsafe_allow_html=True)

# Définir les couleurs
couleur_fond_page = "#00CED1"  # Bleu turquoise
couleur_texte = "#2F4F4F"  # Gris foncé
couleur_case_cliquable = "#AFEEEE"  # Turquoise pâle

# Appliquer le style à un conteneur global
st.markdown(
    f"""
    <style>
        .app-container {{
            background-color: {couleur_fond_page};
            color: {couleur_texte};
            padding: 1rem;
            border-radius: 5px;
        }}
        .case-cliquable {{
            background-color: {couleur_case_cliquable};  /* Modifiez ici la couleur de fond */
            padding: 10px;
            border-radius: 10px;
            text-align: center;
            margin-bottom: 10px;
        }}
    </style>
    """,
    unsafe_allow_html=True
)

# Appliquer le style au texte des cases cliquables
style_texte_case_cliquable = "font-weight: bold; text-decoration: none; color: black;"

# Titre du tableau de bord
st.title("Bienvenue")

# Logo de l'entreprise
def logo() : 
    image_path = "C:\\Users\\simplon\\Desktop\\Projet_Akigora\\Akigora_code\\Logo_Akigora.png"
    original_image = Image.open(image_path)
    st.image(original_image, use_column_width=True, caption="")
logo()
# Espacement
st.write("\n\n")

# Cadres cliquables pour les départements
col1, col2, col3, col4, col5 = st.columns(5)

# Options de département
departement_options = ["Département RH", "Département Marketing", "Département Technique", "Département Direction", "Département Commerce"]

start_date = None
end_date = None

# Redirection vers la page "Indicateurs du Département" correspondante
if col1.button("Département RH", key="departement_rh", on_click=None, help=None):
    # Masquer le titre "Bienvenue" en utilisant du CSS
    st.markdown("<style>h1 { display : none; }</style>", unsafe_allow_html=True)
    # Afficher les indicateurs du Département RH
    st.markdown("## Indicateurs du Département RH")
    # Obtient le répertoire du script actuel
    script_directory = os.path.dirname(os.path.abspath(__file__))
    # Combine le chemin du script avec le chemin relatif du fichier Excel
    excel_file_path = os.path.join(script_directory, 'data', 'Indicateurs_a_envoyer_aux_etudiants_Simplon.xlsx')
    DFexp0 = pd.read_excel(excel_file_path, sheet_name='Collection Experts')
    DFexp1= pd.DataFrame()
    DFexp1=DFexp0.copy()
    DFexp2= pd.DataFrame()
    DFexp3= pd.DataFrame()
    DFexp4= pd.DataFrame()
    DFexp5= pd.DataFrame()    
   
    DFexp1['updatedAt'] = pd.to_datetime(DFexp0['updatedAt'], unit='ms') #changement de type int a date
    DFexp1['createdAt'] = pd.to_datetime(DFexp0['createdAt'], format='%d/%m/%Y', errors='coerce') # changement du format
    DFexp1['linkedInImport'] = DFexp0['linkedInImport'].fillna(0).astype(bool) #NaN = 0, changement de float a Booleen

    seuil_non_nullite = int(0.85 * len(DFexp0))
    DFexp2 = DFexp1
    DFexp2 = DFexp1.dropna(axis=1, thresh=seuil_non_nullite)

    start_date = DFexp2['createdAt'].min()
    end_date = DFexp2['createdAt'].max()

    DFexp3 = DFexp2.copy()
    DFexp3 = DFexp3.dropna(subset=['createdAt'])
    DFexp3 = DFexp3.sort_values(by='createdAt', ascending=True)

    DFexp4 = DFexp3.copy()
    DFexp4 = DFexp4.reset_index(drop=True)
    DFexp4.set_index('createdAt', inplace=True)
    counts_by_interval = DFexp4.groupby(pd.Grouper(freq='6M')).size()
    cumulative_counts_by_interval = counts_by_interval.cumsum()

    DFexp5 = DFexp3.copy()
    DFexp5 = DFexp5.reset_index(drop=True)
    DFexp5['createdAt'] = pd.to_datetime(DFexp5['createdAt'])
    counts_by_interval = DFexp5.groupby(pd.Grouper(key='createdAt', freq='6M')).size()

    Nb_experts = DFexp1.shape[0]

    # Nombre d'experts visibles
    nb_visible = sum(DFexp0['visible'] == 1.0)

    # Profils d'expert remplis à 100%
    profil_remplis = sum(DFexp1['percentage'] == 100) / len(DFexp1)
    prct_profil_remplis = round(profil_remplis * 100, 2)

    # Définir les couleurs
    couleur_info_box = "#87CEEB"  # Ciel léger
    couleur_card = "#F0FFFF"  # Azur clair

    # Afficher les informations avec des éléments visuels
    st.info("### Statistiques des experts sur la plateforme")

    # Affichage du nombre d'experts inscrits
    st.info(f"Nombre d'experts inscrits : {DFexp1.shape[0]}")
    # Affichage du nombre d'experts visibles
    st.success(f"Nombre d'experts visibles : {sum(DFexp0['visible']==1.0)}")
    
    # Diagramme circulaire pour illustrer le pourcentage de profils remplis
    fig, ax = plt.subplots(figsize=(2, 2))  # Taille réduite
    colors = ['#02A865', '#A4d1AE']  # couleur akigora
    ax.pie([prct_profil_remplis, 100 - prct_profil_remplis], labels=['Remplis à 100%', 'Non remplis à 100%'], autopct='%1.1f%%', startangle=90, colors=colors)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    st.pyplot(fig)

    

if col2.button("Département Marketing", key="departement_marketing", on_click=None, help=None):
    # Afficher les indicateurs du Département Marketing
    st.markdown("## Indicateurs du Département Marketing")
    st.write("Ajoutez ici les indicateurs spécifiques au Département Marketing.")

  

if col3.button("Département Technique", key="departement_technique", on_click=None, help=None):
    # Afficher les indicateurs du Département Technique
    st.markdown("## Indicateurs du Département Technique")
    st.write("Ajoutez ici les indicateurs spécifiques au Département Technique.")



if col4.button("Département Direction", key="departement_direction", on_click=None, help=None):
    # Afficher les indicateurs du Département Direction
    st.markdown("## Indicateurs du Département Direction")
    st.write("Ajoutez ici les indicateurs spécifiques au Département Direction.")


if col5.button("Département Commerce", key="departement_commerce", on_click=None, help=None):
    # Afficher les indicateurs du Département Commerce
    st.markdown("## Indicateurs du Département Commerce")
    st.write("Ajoutez ici les indicateurs spécifiques au Département Commerce.")


