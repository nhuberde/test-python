#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import re

# import des données
drugs_df = pd.read_csv("drugs.csv")
pubmed_df = pd.read_csv("pubmed.csv")
pubmed_json = pd.read_json("pubmed.json", orient='records')
clinical_trials_df = pd.read_csv("clinical_trials.csv")

#
# Traitement des données
#

# on regroupe les données pubmed

pubmed_final_df = pubmed_df.append(pubmed_json).reset_index(drop=True)

# on replace les NaN par un str vide pour regrouper les titres en double
# on replace les string contenant des espaces pour enlever les lignes dont le titre est vide

clinical_trials_final_df = clinical_trials_df.fillna('')\
    .groupby('scientific_title', as_index=False)\
    .max().replace(r'^\s*$', np.nan, regex=True)\
    .dropna()

# on harmonise les dates 

clinical_trials_final_df['date'] = pd.to_datetime(clinical_trials_final_df['date'])
pubmed_final_df['date'] = pd.to_datetime(pubmed_final_df['date'])

# retour vers des dates en string pour une meilleure lisibilité

pubmed_final_df['date'] = pubmed_final_df['date'].dt.strftime('%Y-%m-%d')
clinical_trials_final_df['date'] = clinical_trials_final_df['date'].dt.strftime('%Y-%m-%d')

#
# Construction du graphe de liaison
#

list_ctrials = []

for index, value in drugs_df['drug'].items():
    temp_list = []
    for index2, value2 in clinical_trials_final_df['scientific_title'].items():
        if drugs_df['drug'][index].lower() in value2.lower():
            temp_list.append(pubmed_final_df.iloc[index2].to_dict())
    list_ctrials.append(temp_list)

list_ctrials

list_pubmed = []

for index, value in drugs_df['drug'].items():
    temp_list = []
    for index2, value2 in pubmed_final_df['title'].items():
        if drugs_df['drug'][index].lower() in value2.lower():
            temp_list.append(pubmed_final_df.iloc[index2].to_dict())
    list_pubmed.append(temp_list)

list_pubmed

drugs_df['clinical_trials'] = list_ctrials
drugs_df['pubmeds'] = list_pubmed

# export du graphe en json

drugs_df.to_json('final.json', orient='records')
