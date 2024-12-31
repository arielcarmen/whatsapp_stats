import streamlit as st

from collections import defaultdict
import re
import pandas as pd


# def analyze_messages(file_path):
#     # Dictionnaire pour stocker les comptes des utilisateurs et leurs premiers messages
#     user_message_data = defaultdict(lambda: {"count": 0, "first_message": None})
#     timestamps = []

#     # Expression régulière pour extraire les informations
#     pattern = r'^(\d{2}/\d{2}/\d{4}, \d{2}:\d{2}) - ([^:]+):'

#     try:
#         # Lecture du fichier
#         with open(file_path, 'r', encoding='utf-8') as file:
#             for line in file:
#                 match = re.match(pattern, line)
#                 if match:
#                     timestamp, user = match.groups()
#                     timestamps.append(timestamp)
                    
#                     # Mettre à jour le compte des messages
#                     user_data = user_message_data[user.strip()]
#                     user_data["count"] += 1

#                     # Enregistrer le premier message si ce n'est pas encore défini
#                     if user_data["first_message"] is None:
#                         user_data["first_message"] = timestamp
#     except FileNotFoundError:
#         print(f"Le fichier '{file_path}' n'a pas été trouvé.")
#         return {}, []
#     except Exception as e:
#         print(f"Une erreur s'est produite : {e}")
#         return {}, []

#     return user_message_data, timestamps

def analyze_messages(uploaded_file):
    """
    Analyse les messages d'un fichier téléchargé via Streamlit.
    
    Args:
        uploaded_file (UploadedFile): Fichier téléchargé via Streamlit.
        
    Returns:
        tuple: Dictionnaire des utilisateurs et leurs données, et une liste des horodatages.
    """
    # Dictionnaire pour stocker les comptes des utilisateurs et leurs premiers messages
    user_message_data = defaultdict(lambda: {"count": 0, "first_message": None})
    timestamps = []

    # Expression régulière pour extraire les informations
    pattern = r'^(\d{2}/\d{2}/\d{4}, \d{2}:\d{2}) - ([^:]+):'

    try:
        # Lecture du contenu du fichier depuis l'objet UploadedFile
        for line in uploaded_file.getvalue().decode("utf-8").splitlines():
            match = re.match(pattern, line)
            if match:
                timestamp, user = match.groups()
                timestamps.append(timestamp)

                # Mettre à jour le compte des messages
                user_data = user_message_data[user.strip()]
                user_data["count"] += 1

                # Enregistrer le premier message si ce n'est pas encore défini
                if user_data["first_message"] is None:
                    user_data["first_message"] = timestamp
    except Exception as e:
        print(f"Une erreur s'est produite : {e}")
        return {}, []

    return user_message_data, timestamps


def write_to_file(output_path, content):
    try:
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f"Les résultats ont été écrits dans le fichier : {output_path}")
    except Exception as e:
        print(f"Une erreur s'est produite lors de l'écriture du fichier : {e}")

def analyse_datas(results):
    # Déterminer les premières et dernières dates globales
    first_message = min(timestamps) if timestamps else "Inconnu"
    last_message = max(timestamps) if timestamps else "Inconnu"
    
    # Calculer le total des messages
    total_messages = sum(user_data["count"] for user_data in results.values())
    
    # Construire le contenu à écrire
    output_content = []
    output_content.append(f"Total des messages entre : {first_message} et {last_message}\n")
    output_content.append("Liste des utilisateurs et nombre total de messages :\n")
    
    for idx, (user, data) in enumerate(sorted(results.items(), key=lambda x: x[1]["count"], reverse=True), start=1):
        output_content.append(f"{idx}. {user} (Premier message : {data['first_message']}) : {data['count']}\n")
    
    output_content.append(f"\nCompte total des messages : {total_messages}\n")
    
    # Convertir le contenu en chaîne de caractères
    output_string = "".join(output_content)
    
    # Afficher dans la console
    st.write(output_string)


# EXECUTION
st.title(':green[Whastats]')
file = st.file_uploader("Importer vos données de discussion", type=["txt"])

# Vérification si un fichier a été téléchargé
if file is not None:
    results, timestamps = analyze_messages(file)
    if results:
        if st.button("Stats"):
            analyse_datas(results)
    else:
        st.write("Aucune donnée trouvée")
