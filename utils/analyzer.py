"""
WhatsApp Message Analysis Utilities
This module contains utility functions for analyzing WhatsApp chat exports.
"""

import re
import datetime
from collections import defaultdict


def extract_group_details(uploaded_file):
    """
    Extract group name and creation details from a WhatsApp chat export.
    
    Args:
        uploaded_file (UploadedFile): Uploaded file via Streamlit.
        
    Returns:
        tuple: (group_info_string, group_name)
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
    Extract the minimum and maximum dates from the messages.
    
    Args:
        uploaded_file (UploadedFile): Uploaded file via Streamlit.
        
    Returns:
        tuple: (date_min, date_max) as datetime objects
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
    Analyze messages from a WhatsApp chat export file.
    
    Args:
        uploaded_file (UploadedFile): Uploaded file via Streamlit.
        keyword (str): Keyword to search for.
        date_start (date): Start date for filtering (optional).
        date_end (date): End date for filtering (optional).
        
    Returns:
        tuple: (user_message_data dict, timestamps list)
    """
    # Dictionary to store user data and their message counts
    user_message_data = defaultdict(lambda: {"count": 0, "first_message": None})
    timestamps = []

    try:
        # Read content from the uploaded file
        for line in uploaded_file.getvalue().decode("utf-8").splitlines():
            match = re.match(r"^(\d{2}/\d{2}/\d{4}, \d{2}:\d{2}) - ([^:]+): (.+)", line)
            if match:
                timestamp, user, content = match.groups()
                
                # Check date filter if specified
                if date_start or date_end:
                    try:
                        msg_date = datetime.datetime.strptime(timestamp, '%d/%m/%Y, %H:%M').date()
                        if date_start and msg_date < date_start:
                            continue
                        if date_end and msg_date > date_end:
                            continue
                    except ValueError:
                        continue
                
                # Search for keyword (case-insensitive, whole word)
                pattern = r'\b' + re.escape(keyword.lower()) + r'\b'

                if re.search(pattern, content.lower()) is not None:
                    timestamps.append(timestamp)
                    # Update user message count
                    user_data = user_message_data[user.strip()]
                    user_data["count"] += 1

                    # Record first message timestamp
                    if user_data["first_message"] is None:
                        user_data["first_message"] = timestamp

    except Exception as e:
        print(f"Une erreur s'est produite : {e}")
        return {}, []

    return user_message_data, timestamps


def generate_analysis_report(results, group_name, keyword, timestamps):
    """
    Generate a formatted analysis report from the results.
    
    Args:
        results (dict): User message data dictionary.
        group_name (str): Name of the WhatsApp group.
        keyword (str): The keyword that was searched.
        timestamps (list): List of message timestamps.
        
    Returns:
        str: Formatted analysis report.
    """
    # Determine the first and last message dates
    dates = []
    for timestamp in timestamps:
        try:
            date_obj = datetime.datetime.strptime(timestamp, '%d/%m/%Y, %H:%M')
            dates.append(date_obj)
        except ValueError:
            continue

    # Determine the first and last message dates
    if dates:
        first_message = min(dates).strftime('%d/%m/%Y, %H:%M')
        last_message = max(dates).strftime('%d/%m/%Y, %H:%M')
    else:
        first_message = "Unknown"
        last_message = "Unknown"
    
    # Calculate total messages
    total_messages = sum(user_data["count"] for user_data in results.values())
    
    # Build the output content
    output_content = []
    output_content.append(f"Total messages between: {first_message} and {last_message}\n\n")

    if keyword != "":
        output_content.append(f"List of users who sent '{keyword}':\n")
    else:
        output_content.append("List of users and total number of messages:\n")
    
    for idx, (user, data) in enumerate(sorted(results.items(), key=lambda x: x[1]["count"], reverse=True), start=1):
        output_content.append(f"{idx}. {user} (First message: {data['first_message']}) : {data['count']}\n")
    
    output_content.append(f"\nTotal message count: {total_messages}\n")
    
    # Convert to string
    output_string = "".join(output_content)
    
    return output_string
