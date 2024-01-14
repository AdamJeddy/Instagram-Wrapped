import os
import json
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pprint import pprint
import emoji
import unicodedata
from unidecode import unidecode
from colorama import Fore, Style
from collections import Counter
import nltk
from nltk.tokenize import word_tokenize

### ~~~~~~~~~~~ Functions ~~~~~~~~ ###

# Function to load JSON data from a file
def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

# Function to extract messages from the JSON data
def extract_messages(data):
    messages = data.get('messages', [])
    return messages

# Function to convert the JSON data into a Pandas DataFrame
def text_to_emoji(text):
    return text.encode('latin1').decode('utf-8')

# Function to fix encoding issues
def fix_encoding(text):
    if isinstance(text, str):
        try:
            # Try UTF-8 decoding first
            return text.encode('latin1').decode('utf-8')
        except UnicodeEncodeError:
            try:
                # If it fails, try the next encoding
                return text.encode('iso-8859-1').decode('utf-8')
            except UnicodeEncodeError:
                # If both fail, return the original text
                return text
    else:
        return text

# Function to correct encoding
def correct_encoding(text):
    try:
        return text.encode('latin1').decode('utf-8')
    except Exception as e:
        # Return the original text if there's an error
        return text

# Function to check if text contains non-Latin characters
def contains_non_latin(text):
    return re.search(r'[^\p{Latin}\p{Common}]', text) is not None

# Function to normalize text
def normalize_text(text):
    try:
        if not contains_non_latin(text):
            return unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('ASCII')
        else:
            return text
    except Exception as e:
        # Return the original text if there's an error
        return text

# Function to check if 'share' contains a link with 'reel'
def contains_reel_link(share_data):
    if isinstance(share_data, dict) and 'link' in share_data:
        return 1 if 'reel' in share_data['link'] else 0
    return 0

# Function to load all the messages
def load_messages(root_directory, columns_to_drop, users_to_drop):
    # Initialize an empty DataFrame to store all messages
    all_messages_df = pd.DataFrame()

    # Counter for tracking the number of users
    user_count = 0

    # Iterate through user folders
    for user_folder in os.listdir(root_directory):
        user_folder_path = os.path.join(root_directory, user_folder)
        
        # Check if the item in the directory is a folder
        if os.path.isdir(user_folder_path):
            
            user_count += 1
            
            # Iterate through JSON files in the user's folder
            for json_file in os.listdir(user_folder_path):
                if json_file.endswith('.json'):
                    json_file_path = os.path.join(user_folder_path, json_file)
                    
                    # Load JSON data
                    data = load_json(json_file_path)
                    
                    # Extract messages
                    messages = extract_messages(data)
                    
                    # Create a Pandas DataFrame from the messages
                    df = pd.DataFrame(messages)
                    
                    # Add a column for the user's name
                    df['user'] = user_folder.rsplit('_', 1)[0]
                    
                    # Concatenate the DataFrame to the overall DataFrame
                    all_messages_df = pd.concat([all_messages_df, df])

    # Drop the specified columns
    all_messages_df = all_messages_df.drop(columns=columns_to_drop, errors='ignore')

    # Drop rows where 'sender_name' is in the list of users to drop or where 'sender_name' is "Instagram User" or 'user' is "instagramuser"
    all_messages_df = all_messages_df[
        ~(all_messages_df['user'].isin(users_to_drop) | 
        (all_messages_df['sender_name'] == "Instagram User") |
        (all_messages_df['user'] == "instagramuser")
        )
    ]


    # Extract only the 'reaction' from the 'reactions' column and use text_to_emoji() to convert it to emoji
    all_messages_df['reactions'] = all_messages_df['reactions'].apply(lambda x: x[0]['reaction'].encode('latin1').decode('utf-8') if isinstance(x, list) and len(x) > 0 else None)


    # Convert the 'timestamp_ms' column to datetime format
    all_messages_df['timestamp'] = pd.to_datetime(all_messages_df['timestamp_ms'], unit='ms')

    # Create new columns for year, month, day, and time
    all_messages_df['year'] = all_messages_df['timestamp'].dt.year
    all_messages_df['month'] = all_messages_df['timestamp'].dt.month
    all_messages_df['day'] = all_messages_df['timestamp'].dt.day
    all_messages_df['time'] = all_messages_df['timestamp'].dt.strftime('%H:%M')
    all_messages_df['hour'] = all_messages_df['timestamp'].dt.hour
    all_messages_df['minute'] = all_messages_df['timestamp'].dt.minute


    # Regex pattern to match werid characters into readbale text
    all_messages_df['sender_name'] = all_messages_df['sender_name'].apply(correct_encoding)

    # Apply the function to the 'sender_name' column
    all_messages_df['sender_name'] = all_messages_df['sender_name'].apply(normalize_text)

    # Apply the fix_encoding function to the 'content' column
    all_messages_df['content'] = all_messages_df['content'].apply(fix_encoding)


    # Drop rows where 'content' column contains the specified text
    all_messages_df = all_messages_df[~all_messages_df['content'].str.contains("تم التفاعل باستخدام", na=False)]
    all_messages_df = all_messages_df[~all_messages_df['content'].str.contains("هامت رسالة على الإعجاب", na=False)]

    # Apply the function to create the 'Reel' column
    all_messages_df['reel'] = all_messages_df['share'].apply(contains_reel_link)

    # Create a new column for word count
    all_messages_df['word_count'] = all_messages_df['content'].astype(str).apply(lambda x: len(x.split()))

    return all_messages_df, user_count