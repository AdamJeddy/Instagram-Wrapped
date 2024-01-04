import os
import json
import re
import threading
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pprint import pprint
import emoji
from colorama import Fore, Style
from pyfiglet import Figlet

import helper_function

plt.style.use('Solarize_Light2')

def loading_animation():
    animation = ['⣾', '⣷', '⣯', '⣟', '⡿', '⢿', '⣻', '⣽']
    while not loading_complete:
        for frame in animation:
            print(Fore.CYAN + f"\r{frame}" + Style.RESET_ALL + "  Loading the messages DataFrame...  ", end="", flush=True)
            time.sleep(0.1)


def main():
    # Printing the title
    print( "\n" )
    print("☆.。.:*・°☆.。.:*・°☆.。.:*・°☆.。.:*・°☆.。.:*・°☆." + Style.RESET_ALL)
    print(Figlet().renderText('Instagram Wrapped'))
    print("☆.。.:*・°☆.。.:*・°☆.。.:*・°☆.。.:*・°☆.。.:*・°☆." + Style.RESET_ALL)
    print("\n")
    
    # Root directory where all user folders are located
    # Columns to drop and users to drop
    # User's Instagram name
    root_directory = os.path.join(os.getcwd(), './inbox')
    columns_to_drop = ['call_duration', 'sticker', 'is_geoblocked_for_viewer']
    users_to_drop = []
    your_instagram_name = 'Adam'

    # Loading the messages DataFrame and time it
    global loading_complete
    loading_complete = False

    start_time = time.time()
    print(Fore.GREEN + "Loading the messages DataFrame... " + Style.RESET_ALL, end="", flush=True)

    loading_thread = threading.Thread(target=loading_animation)
    loading_thread.start()
    
    try:
        messages_df = helper_function.load_messages(root_directory, columns_to_drop, users_to_drop)
    except Exception as e:
        error_flag = True, e

    loading_complete = True
    loading_thread.join()
    
    if error_flag[0]:
        print(Fore.RED + "\nError loading the messages DataFrame: " + Style.RESET_ALL + str(error_flag[1]))
        return
    print(Fore.GREEN + "Done in " + f"{(time.time() - start_time):.2f}" + " secs!" + Style.RESET_ALL)

    """
    ### ~~~~~~~~~~~ 2023 Review ~~~~~~~~ ###
    # New DataFrame for the year 2023
    messages_2023_df = messages_df[messages_df['year'] == 2023]

    ## Number of messages sent by each user
    message_count_by_user = messages_2023_df['sender_name'].value_counts()
    print(message_count_by_user[0:10])
    """
    

    

if __name__ == '__main__':
    main()