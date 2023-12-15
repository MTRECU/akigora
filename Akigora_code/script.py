import pandas as pd
import streamlit as st
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns

DFexp0 = pd.read_excel('data/Indicateurs_a_envoyer_aux_etudiants_Simplon.xlsx', sheet_name = 'Collection Experts')

# DFexp= pd.DataFrame() # type colonne updatedAt + Boolen de linkedin
# DFexp['updatedAt'] = pd.to_datetime(DFexp0['updatedAt'], unit='ms')
# DFexp['createdAt'] = pd.to_datetime(DFexp0['createdAt'], format='%d/%m/%Y', errors='coerce') # changement du format
# DFexp['linkedInImport'] = DFexp0['linkedInImport'].fillna(0).astype(bool) #NaN = 0, changement de float a Booleen

# seuil_non_nullite = int(0.85 * len(DFexp)) #drop les colonnes -15%
# DFexp_clean = pd.DataFrame
# DFexp_clean = DFexp0.dropna(axis=1, thresh=seuil_non_nullite)

# DFexp1 = pd.DataFrame
# DFexp1['createdAt'] = pd.to_datetime(DFexp0['createdAt'], errors='coerce')

# DFexp2 = pd.DataFrame
# DFexp2 = DFexp1.dropna(subset=['createdAt']).copy()
# DFexp2.set_index('createdAt', inplace=True) # Définir 'createdAt' comme index
# trimester_groups = DFexp2.resample('2Q')['_id'].agg(list) # Resample par trimestre et agréger les IDs

# #Nombres d'experts
# Nb_experts = DFexp0.shape[0]
# Nb_experts

# #le premier inscrit 
# Debut = min(DFexp0['createdAt'])
# Debut

# #Graph du nombre d'inscrit par tranche de 6 mois
# trimester_groups_df = pd.DataFrame({'Count': DFexp2.resample('2Q').size()})
# trimester_groups_df.plot(kind='line', marker='o', linestyle='-', color='b', figsize=(10, 6))

# plt.title('Number of Entries by semestre')
# plt.xlabel('Trimester')
# plt.ylabel('Number of Entries')
# plt.grid(True)

# #Nombre d'inscrit par 6 mois et inscrit totaux dans le temps
# total_entries = DFexp2.resample('2Q').size().cumsum()

# total_entries_df = pd.DataFrame({'Total Entries': total_entries})

# plt.figure(figsize=(10, 6))

# plt.plot(trimester_groups_df.index, trimester_groups_df['Count'], marker='o', linestyle='-', color='b', label='Last 6 Months')

# plt.plot(total_entries_df.index, total_entries_df['Total Entries'], marker='o', linestyle='-', color='r', label='Total Entries')

# plt.title('Number of Entries by semestre')
# plt.xlabel('Trimester')
# plt.ylabel('Number of Entries')
# plt.grid(True)
# plt.legend()

#de meme sur deux graphs


st.title('Akigora')
st.write(DFexp0)
# Exemple de widget pour filtrer par ville
selected_ville = st.sidebar.selectbox('Sélectionnez une ville', DFexp0['location'].unique())
filtered_data = DFexp0[DFexp0['location'] == selected_ville]
st.write(filtered_data)




