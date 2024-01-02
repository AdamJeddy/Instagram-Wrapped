import os
import json
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pprint import pprint
import emoji
from colorama import Fore, Style

import helper_function


plt.style.use('Solarize_Light2')


if __name__ == '__main__':
    # Root directory where all user folders are located
    # Columns to drop and users to drop
    # User's Instagram name
    root_directory = os.path.join(os.getcwd(), 'messages/Instagram-Wrapped/inbox')
    columns_to_drop = ['call_duration', 'sticker', 'is_geoblocked_for_viewer']
    users_to_drop = []
    your_instagram_name = 'Adam'


    messages_df = helper_function.load_messages(root_directory, columns_to_drop, users_to_drop)


    ### ~~~~~~~~~~~ 2023 Review ~~~~~~~~ ###
    # New DataFrame for the year 2023
    messages_2023_df = messages_df[messages_df['year'] == 2023]

    ## Number of messages sent by each user
    message_count_by_user = messages_2023_df['sender_name'].value_counts()
    print(message_count_by_user[0:10])