import pandas as pd
import matplotlib.pyplot as plt
import wordcloud
from collections import Counter
from textblob import TextBlob
from tabulate import tabulate

import helper_function



def top_senders_and_recipients(messages_df):
    """
    Analyze the top senders and recipients of messages in the given year.
    
    Args:
        messages_df (pandas.DataFrame): The DataFrame containing the messages.
    
    Returns:
        None
    """
    # Top 10 senders
    top_senders = messages_df['sender_name'].value_counts().head(10).reset_index()
    top_senders.columns = ['Sender', 'Number of Messages']

    # Print top senders in a table format
    print(f"\nTop 10 senders in {messages_df['year'].unique()[0]}:")
    print(tabulate(top_senders, headers=['Sender', 'Number of Messages'], tablefmt='fancy_grid'))
    

def messaging_trends(messages_df):
    """
    Analyze the messaging trends, including messages per month and messages per day of the week.
    
    Args:
        messages_df (pandas.DataFrame): The DataFrame containing the messages.
    
    Returns:
        None
    """
    messages_df['date'] = pd.to_datetime(messages_df['timestamp_ms'], unit='ms')
    messages_df['month'] = messages_df['date'].dt.strftime('%b')
    messages_df['day_of_week'] = messages_df['date'].dt.day_name()

    # Messages per month
    monthly_messages = messages_df.groupby('month')['content'].count().reset_index().sort_values('month')
    
    # Print messages per month in table format
    print("\nMessaging Trends by Month:")
    print(tabulate(monthly_messages, headers=['Month', 'Number of Messages'], tablefmt='fancy_grid'))

    # Messages per day of the week
    daily_messages = messages_df.groupby('day_of_week')['content'].count().reset_index().sort_values('day_of_week')
    
    # Print messages per day of the week in table format
    print("\nMessaging Trends by Day of the Week:")
    print(tabulate(daily_messages, headers=['Day of Week', 'Number of Messages'], tablefmt='fancy_grid'))


def analyze_messages(messages_df):
    """
    Perform a comprehensive analysis of the messages in the given DataFrame.
    
    Args:
        messages_df (pandas.DataFrame): The DataFrame containing the messages.
    
    Returns:
        None
    """
    top_senders_and_recipients(messages_df)
    messaging_trends(messages_df)
