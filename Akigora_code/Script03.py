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
import json
import folium
from streamlit_folium import folium_static

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

    Localisation = DFexp0['location'].unique()
    DFexp1 = DFexp0
    DFexp1['location'] = DFexp1['location'].str.split().str.get(0)
    DFexp1['location'] = DFexp1['location'].str.replace(',','')
    
    Ville_grouped = DFexp1.groupby('location').size()
    Ville_grouped_sorted = Ville_grouped.sort_values(ascending=False)
    Top_10_villes = Ville_grouped_sorted.head(10)
    Pourcentage_ville = round((DFexp1['location'].dropna().value_counts(normalize=True)*100), 2)
    pourcent_Top_10_villes = Pourcentage_ville.head(10)

    # Définir les couleurs
    couleur_info_box = "#87CEEB"  # Ciel léger
    couleur_card = "#F0FFFF"  # Azur clair

    # Afficher les informations avec des éléments visuels
    st.info("### Statistiques des experts sur la plateforme")
    # Sélection de la visualisation
    selected_visualization = st.selectbox("Sélectionnez la visualisation :", ["Niveau de completion du formulaire", "Evolution des inscriptions", "Localisation de nos experts"])
    # Affichage du nombre d'experts inscrits
    if selected_visualization == "Niveau de completion du formulaire":
        st.info(f"Nombre d'experts inscrits : {DFexp1.shape[0]}")
        # Affichage du nombre d'experts visibles
        st.success(f"Nombre d'experts visibles : {sum(DFexp0['visible']==1.0)}")
    
        # Diagramme circulaire pour illustrer le pourcentage de profils remplis
        fig, ax = plt.subplots(figsize=(2, 2))  # Taille réduite
        colors = ['#02A865', '#A4d1AE']  # couleur akigora
        ax.pie([prct_profil_remplis, 100 - prct_profil_remplis], labels=['Formulaire remplis à 100%', 'Formulaire non remplis à 100%'], autopct='%1.1f%%', startangle=90, colors=colors)
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        st.pyplot(fig)


    if selected_visualization == "Evolution des inscriptions":

        # Ensure the 'Created' column is of datetime type
        DFexp3['Created'] = pd.to_datetime(DFexp3['Created'])

        # Convert datetime values to Unix timestamps

        start_date = DFexp3['Created'].min().date()
        end_date = DFexp3['Created'].max().date()

        selected_date_range = st.slider("Select a date range", min_value=start_date, max_value=end_date, value=(start_date, end_date))

        # Convert selected Unix timestamps back to datetime objects
        selected_start_date = pd.to_datetime(selected_date_range[0])
        selected_end_date = pd.to_datetime(selected_date_range[1])

        # Filter the DataFrame based on the selected date range
        filtered_df = DFexp3[(DFexp3['Created'] >= selected_start_date) & (DFexp3['Created'] <= selected_end_date)]

        # Perform grouping and counting operations on the filtered DataFrame
        Expert_grouped = filtered_df.groupby('Created').size()
        DFgrouped = pd.DataFrame(Expert_grouped)
        counts_by_interval = DFgrouped.groupby(pd.Grouper(freq='6M')).size()
        cumulative_counts_by_interval = counts_by_interval.cumsum()
           

        #filters_date = start_date >= selected_date_range[0]&end_date <= selected_date_range[1]    
        fig, axs = plt.subplots(1, 2, figsize=(15, 6))
         # Tracer le premier graphique (cumulatif)
        axs[0].plot(cumulative_counts_by_interval.index, cumulative_counts_by_interval.values, linestyle='-', color='b', marker='o')
        axs[0].set_title('Évolution cumulatif du nombre d\'experts', fontsize=20)
        axs[0].set_xlabel('Evolution semestrielle', fontsize=15)
        axs[0].set_ylabel('Nombre d\'experts', fontsize=15)
        axs[0].tick_params(axis='x', rotation=45)  # Rotation des dates pour une meilleure lisibilité
        # Tracer le deuxième graphique (non cumulatif)
        axs[1].plot(counts_by_interval.index, counts_by_interval.values, linestyle='-', color='r', marker='o')
        axs[1].set_title('Évolution non cumulatif du nombre d\'experts', fontsize=20)
        axs[1].set_xlabel('Evolution semestrielle', fontsize=15)
        axs[1].set_ylabel('Nombre d\'experts', fontsize=15)
        axs[1].tick_params(axis='x', rotation=45)  # Rotation des dates pour une meilleure lisibilité
        st.pyplot(fig)

    if selected_visualization == "Localisation de nos experts":
        
        # Sélection de la ville parmi le top 10, triées par ordre alphabétique
        selected_city = st.selectbox("Sélectionnez une ville :", Top_10_villes.sort_index().index)

        # Filtrer les données en fonction de la ville sélectionnée
        filtered_data = DFexp1[DFexp1['location'] == selected_city]

        # Calculer le pourcentage des domaines pour la ville sélectionnée
        domains_percent_city = (filtered_data['domains'].value_counts(normalize=True) * 100).round(2)

        # Créer et afficher l'histogramme
        st.bar_chart(domains_percent_city, color='#02A865')
        st.set_option('deprecation.showPyplotGlobalUse', False)
        st.pyplot().update_layout(xaxis_tickangle=-45)
        st.pyplot().update_xaxes(title_text='Domaines')
        st.pyplot().update_yaxes(title_text='Pourcentage')
        st.pyplot().update_layout(title_text=f'Répartition des domaines pour la ville : {selected_city}')



def marketing_page():
    st.title("Datavisualisation du Département Marketing")
    st.info("### Statistiques pour le département Marketing")
    # Sélection de la visualisation
    selected_visualization = st.selectbox("Sélectionnez la visualisation :", ["Les Newsletters", "How We Met", "3"])
    # Affichage du nombre d'experts inscrits
    if selected_visualization == "Les Newsletters":
        st.title("Qui sont nos abonnés")
        # Votre contenu pour le département Marketing ici
        # Charger les données de la newsletter
        script_directory = os.path.dirname(os.path.abspath(__file__))
        excel_file_path = os.path.join(script_directory, 'data', 'Akigora_data2.xlsx')
        DFnewsletter = pd.read_excel(excel_file_path, sheet_name='Collection newsletter')  # Remplacez 'newsletter' par le nom réel de votre feuille

        # Calculer la répartition des types d'inscrits
        type_counts = DFnewsletter['type'].value_counts()

        # Créer un diagramme en tarte
        fig, ax = plt.subplots(figsize=(1, 1)) 
        colors = ['#02A865', '#A4d1AE']
        ax.pie(type_counts, labels=type_counts.index, autopct='%1.1f%%', startangle=90, colors=colors, textprops={'fontsize': 4})
        ax.axis('equal')  
        st.pyplot(fig)
    if selected_visualization == "How We Met":
        st.title("How We Met")
        script_directory = os.path.dirname(os.path.abspath(__file__))
        excel_file_path = os.path.join(script_directory, 'data', 'Akigora_data2.xlsx')
        dfpro = pd.read_excel(excel_file_path, sheet_name='Collection profile (type compan')
        dfprofile = pd.DataFrame(dfpro)
        # Group by "howWeMet" and calculate the percentage
        dfprofile = dfprofile['howWeMet'].value_counts(normalize=True).reset_index()
        dfprofile.columns = ['howWeMet', 'Percentage']

        # Convert the percentage to percentage format
        dfprofile['Percentage'] = dfprofile['Percentage'] * 100

        # Create a pie chart
        fig, ax = plt.subplots()
        ax.pie(dfprofile['Percentage'], labels=dfprofile['howWeMet'], autopct='%1.1f%%', startangle=25, colors=plt.cm.Paired.colors, textprops={'fontsize': 6})
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        # Display the pie chart in Streamlit
 
        st.pyplot(fig)


    if selected_visualization == "3":
        st.write('Visualisations a venir')

def technique_page():
    st.title("Datavisualisation du Département Technique")
    st.info("### Statistiques pour le Département Technique")
    # Votre contenu pour le département Technique ici

def direction_page():
    
    st.title("Datavisualisation du Département Diréction")
    st.info("### Statistiques pour le Département Diréction")
    selected_visualization = st.selectbox("Sélectionnez la visualisation :", ["Les prix", "2", "3"])
    # Affichage du nombre d'experts inscrits
    if selected_visualization == "Les prix":
        st.title("Le prix de nos experts")
        
        # Charger les données et calculer les prix moyens
        script_directory = os.path.dirname(os.path.abspath(__file__))
        excel_file_path = os.path.join(script_directory, 'data', 'Akigora_data2.xlsx')
        DFprofil_expert = pd.read_excel(excel_file_path, sheet_name='Collection profile (type expert') 
        DFprofil_expert['daily_prices_avg'] = (DFprofil_expert['daily_hourly_prices.daily_price_min'] + DFprofil_expert['daily_hourly_prices.daily_price_max']) / 2
        DFprofil_expert['hourly_prices_avg'] = (DFprofil_expert['daily_hourly_prices.hourly_price_min'] + DFprofil_expert['daily_hourly_prices.hourly_price_max']) / 2
        DFprofil_expert['studyLevel'] = DFprofil_expert['studyLevel'].replace({'Bac +5': 'Bac + 5', 'Bac5': 'Bac + 5', 'Bac3': 'Bac + 3', 'Bac8': 'Bac + 8', 'Bac4': 'Bac + 4', 'Bac2': 'Bac + 2'})
        DFprofil_clean = DFprofil_expert.dropna(subset=['studyLevel', 'daily_prices_avg', 'hourly_prices_avg'])

        # Sélection et filtrage par niveau d'étude
        levels = sorted(DFprofil_clean['studyLevel'].unique())
        selected_level = st.selectbox("Sélectionnez le niveau d'étude :", levels)
        filtered_data = DFprofil_clean[DFprofil_clean['studyLevel'] == selected_level]

        # Calculer les prix moyens pour le niveau d'étude sélectionné
        avg_daily_price = filtered_data['daily_prices_avg'].mean()
        avg_hourly_price = filtered_data['hourly_prices_avg'].mean()

        # Affichage esthétique des prix moyens
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"<div style='background-color:#cdf4fa; padding:10px; border-radius:10px; text-align:center; color:white;'><h2>Prix moyen journalier</h2><h3>€{avg_daily_price:.2f}</h3></div>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"<div style='background-color:#cdf4fa; padding:10px; border-radius:10px; text-align:center; color:white;'><h2>Prix moyen par heure</h2><h3>€{avg_hourly_price:.2f}</h3></div>", unsafe_allow_html=True)

        # Préparer les données pour les visualisations
        daily_prices = filtered_data['daily_prices_avg']
        hourly_prices = filtered_data['hourly_prices_avg']

        # Créer les graphiques
        fig, axs = plt.subplots(1, 2, figsize=(10, 4))

        # Graphique pour les prix moyens journaliers
        sns.boxplot(y=daily_prices, ax=axs[0], color ='#9a02c6')
        axs[0].set_title('Prix moyens journaliers', fontsize=16)
        axs[0].set_ylabel('Prix (€)', fontsize=16)
        
        # Graphique pour les prix moyens horaires
        sns.boxplot(y=hourly_prices, ax=axs[1], color ='#9a02c6')
        axs[1].set_title('Prix moyens horaires', fontsize=16)
        axs[1].set_ylabel('Prix (€)', fontsize=16)

        # Afficher les graphiques
        st.pyplot(fig)

    

def commerce_page():
    st.title("Datavisualisation du Département Commerce")
    st.info("### Statistiques pour le Département Commerce")
    selected_visualization = st.selectbox("Sélectionnez la visualisation :", ["Nos missions", "Nos missions BIS", "3"])
    # Affichage du nombre d'experts inscrits
    if selected_visualization == "Nos missions":
        st.title("Localisation de nos missions")
        script_directory = os.path.dirname(os.path.abspath(__file__))
        excel_file_path = os.path.join(script_directory, 'data', 'Akigora_data2.xlsx')

        # Création du répertoire ville-coordonnées géographiques
        def create_city_coordinates_map(df_expert):
            city_coords_map = {}
            for _, row in df_expert.iterrows():
                if pd.notna(row['location']) and pd.notna(row['geo']):
                    city = str(row['location']).split(',')[0].strip()
                    try:
                        geo_data = json.loads(row['geo'])
                        lat = geo_data.get('latitude')
                        lon = geo_data.get('longitude')

                        if lat and lon:
                            city_coords_map[city] = (lat, lon)
                    except json.JSONDecodeError:
                        continue
            return city_coords_map

        # Charger les données des experts
        df_expert = pd.read_excel(excel_file_path, sheet_name='Collection profile (type expert')
        city_coords_map = create_city_coordinates_map(df_expert)

        # Enrichissement des données d'intervention
        def enrich_intervention_data(df_intervention, city_coords_map):
            df_intervention['geo'] = df_intervention['localisation'].apply(lambda x: city_coords_map.get(x, (None, None)))
            return df_intervention

        # Charger et enrichir les données d'intervention
        df_intervention = pd.read_excel(excel_file_path, sheet_name='Collection intervention')
        df_intervention = enrich_intervention_data(df_intervention, city_coords_map)

        # Création de la carte
        def create_map(data, city_coords_map, map_type='missions'):
            print("Type de 'data':", type(data))  # Pour comprendre la structure de 'data'
            print("Exemple de valeurs dans 'data':", list(data)[:5])  # Afficher quelques valeurs

            m = folium.Map(location=[46.2276, 2.2137], zoom_start=6)

            if isinstance(data, dict):
                data_values = list(data.values())
                max_value = max(data_values) if data_values else 1
            elif isinstance(data, pd.Series):
                max_value = data.max()
            else:
                raise TypeError("Type inattendu pour 'data'")

            for city, value in data.items():
                lat, lon = city_coords_map.get(city, (None, None))
                if lat and lon and value:
                    radius = min_radius + (max_radius - min_radius) * (value / max_value)
                    folium.CircleMarker(
                        location=[lat, lon],
                        radius=radius,
                        popup=f'{city}: {value}',
                        color='red',
                        fill=True,
                        fill_color='red'
                    ).add_to(m)

            return m


        # Affichage de la carte dans Streamlit
        def show_map_in_streamlit():
            selected_map_type = st.selectbox('Choisir le type de visualisation', ['missions', 'hours'])
            df_intervention['hours_planned'] = pd.to_numeric(df_intervention['hours_planned'], errors='coerce')
            total_hours_per_city = df_intervention.groupby('localisation')['hours_planned'].sum()

            if selected_map_type == 'missions':
                missions_count_per_city = df_intervention.groupby('localisation')['_id'].nunique()
                map_missions = create_map(missions_count_per_city, city_coords_map, map_type='missions')
                folium_static(map_missions)

            elif selected_map_type == 'hours':
                total_hours_per_city = df_intervention.groupby('localisation')['hours_planned'].sum()
                map_hours = create_map(total_hours_per_city, city_coords_map, map_type='hours')
                folium_static(map_hours)


        show_map_in_streamlit()
    if selected_visualization == "Nos missions BIS":

        script_directory = os.path.dirname(os.path.abspath(__file__))
        excel_file_path = os.path.join(script_directory, 'data', 'Akigora_data2.xlsx')

        # Charger les données d'intervention
        df_intervention = pd.read_excel(excel_file_path, sheet_name='Collection intervention')
        df_intervention['hours_planned'] = pd.to_numeric(df_intervention['hours_planned'], errors='coerce')

        # Calculer le nombre total de missions et d'heures par ville
        missions_count_per_city = df_intervention.groupby('localisation')['_id'].nunique()
        total_hours_per_city = df_intervention.groupby('localisation')['hours_planned'].sum()

        top_10_missions = missions_count_per_city.nlargest(10)
        top_10_hours = total_hours_per_city.nlargest(10)
        cadre_style = """
        <style>
            .dataframe-cadre {
                border: 2px solid #02A865;
                border-radius: 5px;
                padding: 10px;
                margin: 10px 0;
                color: #02A865;
            }
        </style>
        """
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### Top 10 villes par nombre de missions")
            for city, count in top_10_missions.items():
                st.markdown(f"<div style='color: #02A865;'><b>{city}</b>: {count} missions</div>", unsafe_allow_html=True)

        with col2:
            st.markdown("### Top 10 villes par heures totales")
            for city, hours in top_10_hours.items():
                st.markdown(f"<div style='color: #02A865;'><b>{city}</b>: {hours:.2f} heures</div>", unsafe_allow_html=True)


 

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
        script_directory = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(script_directory, 'Logo_Akigora.png')
        original_image = Image.open(image_path)
        st.image(original_image, width=500, caption="")
    
    logo()
    st.write("Vos département :")
    
    # Utiliser une disposition de colonnes pour aligner horizontalement les boutons
    col1, col2, col3, col4, col5 = st.columns(5)


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
    selected_page = st.sidebar.selectbox("Sélectionnez un département", pages)

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
