import streamlit as st

from collections import defaultdict
import re
import datetime

def extract_group_details(uploaded_file):
    """
    Analyse les messages d'un fichier téléchargé via Streamlit.
    
    Args:
        uploaded_file (UploadedFile): Fichier téléchargé via Streamlit.
        
    Returns:
        tuple: Dictionnaire des utilisateurs et leurs données, et une liste des horodatages.
    """
    group_info = ""
    group_name = ""
    group_creation_pattern = r'^(\d{2}/\d{2}/\d{4}, \d{2}:\d{2}) - ([^:]+) a créé le groupe \"(.*?)\"'
    try:

        for line in uploaded_file.getvalue().decode("utf-8").splitlines():
            group_match = re.match(group_creation_pattern, line)
            if group_match:
                creation_date, creator, group_name = group_match.groups()
                group_info = f"{group_name}, créé par {creator} le {creation_date}"

    except Exception as e:
        print(f"Une erreur s'est produite : {e}")
        return {}, []

    return group_info, group_name

def get_date_range(uploaded_file):
    """
    Extrait les dates min et max des messages du fichier.
    
    Args:
        uploaded_file (UploadedFile): Fichier téléchargé via Streamlit.
        
    Returns:
        tuple: (date_min, date_max) en tant qu'objets datetime
    """
    dates = []
    try:
        for line in uploaded_file.getvalue().decode("utf-8").splitlines():
            match = re.match(r"^(\d{2}/\d{2}/\d{4}), \d{2}:\d{2}", line)
            if match:
                date_str = match.group(1)
                try:
                    date_obj = datetime.datetime.strptime(date_str, '%d/%m/%Y')
                    dates.append(date_obj)
                except ValueError:
                    continue
    except Exception as e:
        print(f"Une erreur s'est produite : {e}")
        return None, None
    
    if dates:
        return min(dates).date(), max(dates).date()
    return None, None

def analyze_messages(uploaded_file, keyword, date_start=None, date_end=None):
    """
    Analyse les messages d'un fichier téléchargé via Streamlit.
    
    Args:
        uploaded_file (UploadedFile): Fichier téléchargé via Streamlit.
        keyword (str): Mot-clé à rechercher
        date_start (date): Date de début du filtrage
        date_end (date): Date de fin du filtrage
        
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
            # match = re.match(pattern, line)
            match = re.match(r"^(\d{2}/\d{2}/\d{4}, \d{2}:\d{2}) - ([^:]+): (.+)", line)
            if match:
                timestamp, user, content = match.groups()
                
                # Vérifier le filtre de dates si spécifié
                if date_start or date_end:
                    try:
                        msg_date = datetime.datetime.strptime(timestamp, '%d/%m/%Y, %H:%M').date()
                        if date_start and msg_date < date_start:
                            continue
                        if date_end and msg_date > date_end:
                            continue
                    except ValueError:
                        continue
                
                pattern = r'\b' + re.escape(keyword.lower()) + r'\b'

                # if keyword.lower() in content.lower():
                if re.search(pattern, content.lower()) is not None:

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

def analyse_datas(results, group_name, keyword):
    # Déterminer les premières et dernières dates globales
    dates = []
    for timestamp in timestamps:
        try:
            date_obj = datetime.datetime.strptime(timestamp, '%d/%m/%Y, %H:%M')
            dates.append(date_obj)
        except ValueError:
            continue

    # Déterminer les premières et dernières dates globales
    if dates:
        first_message = min(dates).strftime('%d/%m/%Y, %H:%M')
        last_message = max(dates).strftime('%d/%m/%Y, %H:%M')
    else:
        first_message = "Inconnu"
        last_message = "Inconnu"
    
    # Calculer le total des messages
    total_messages = sum(user_data["count"] for user_data in results.values())
    
    # Construire le contenu à écrire
    output_content = []
    output_content.append(f"Total des messages entre : {first_message} et {last_message}\n\n")

    if keyword != "":
        output_content.append("Liste des utilisateurs ayant envoyé : '"+ keyword +"'\n")
    else:
        output_content.append("Liste des utilisateurs et nombre total de messages :\n")
    
    for idx, (user, data) in enumerate(sorted(results.items(), key=lambda x: x[1]["count"], reverse=True), start=1):
        output_content.append(f"{idx}. {user} (Premier message : {data['first_message']}) : {data['count']}\n")
    
    output_content.append(f"\nCompte total des messages : {total_messages}\n")
    
    # Convertir le contenu en chaîne de caractères
    output_string = "".join(output_content)
    
    # Afficher dans la console
    st.write(output_string)

    st.download_button(
        label="Télécharger en txt",
        data=output_string,
        file_name= group_name+"_export.txt",
        mime="text/plain"
    )


# EXECUTION
st.title(':blue[Whastats]')
file = st.file_uploader("Importer vos données de discussion:", type=["txt"])

# Vérification si un fichier a été téléchargé
if file is not None:
    group_name = "Aucun groupe trouvé"
    group_infos, group_name = extract_group_details(file)
    
    st.write(group_infos)
    
    if group_infos or True:
        # Obtenir la plage de dates disponibles
        date_min, date_max = get_date_range(file)
        
        col1, col2 = st.columns(2)
        with col1:
            date_start = st.date_input("Date de début", value=date_min, min_value=date_min, max_value=date_max)
        with col2:
            date_end = st.date_input("Date de fin", value=date_max, min_value=date_min, max_value=date_max)
        
        keyword = st.text_input("Mot-clé (laissez vide pour les stats globales)", "")
        if st.button("Stats"):
            results, timestamps = analyze_messages(file, keyword, date_start, date_end)
            analyse_datas(results, group_name, keyword)
    else:
        st.write("Aucune donnée trouvée")
