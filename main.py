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
import review

plt.style.use('Solarize_Light2')

messages_df = None

def loading_animation():
    animation = ['⣾', '⣷', '⣯', '⣟', '⡿', '⢿', '⣻', '⣽']
    while not loading_complete:
        for frame in animation:
            print(Fore.CYAN + f"\r{frame}" + Style.RESET_ALL + "  Loading the messages... " + Style.RESET_ALL, end="", flush=True)
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
    print("")

    loading_thread = threading.Thread(target=loading_animation)
    loading_thread.start()
    
    error_flag = False, None
    try:
        messages_df, user_count = helper_function.load_messages(root_directory, columns_to_drop, users_to_drop)
    except Exception as e:
        error_flag = True, e

    loading_complete = True
    loading_thread.join()
    
    if error_flag[0]:
        print(Fore.RED + "\nError loading the messages DataFrame: " + Style.RESET_ALL + str(error_flag[1]))
        return
    print(Fore.GREEN + "Done in " + f"{(time.time() - start_time):.2f}" + " secs!" + Style.RESET_ALL)
    print(Fore.GREEN + "\nNumber of users: " + Style.RESET_ALL + str(user_count))

    messages_df = messages_df
    
    # Give statistics about the data loaded such as how many rows (messages were loaded, etc)

    ### ~~~~~~~~~~~ 2023 Review ~~~~~~~~ ###
    # New DataFrame for the year 2023
    # messages_2023_df = messages_df[messages_df['year'] == 2023]

    ## Number of messages sent by each user
    # message_count_by_user = messages_2023_df['sender_name'].value_counts()
    
    # print(Fore.GREEN + "\nNumber of messages sent by each user in 2023: " + Style.RESET_ALL)
    # print(message_count_by_user[0:10])
    
    """
    """
    review_menu(messages_df)

def review_menu(messages_df):
    # Ask if this is the user
    # users_name = messages_df['sender_name'].value_counts()[0:1].index[0]
    # print(Fore.GREEN + "\nIs this you? " + Style.RESET_ALL + users_name)
    
    # user_input = input(Fore.GREEN + "\nAre you " + Style.RESET_ALL + users_name + Fore.GREEN + "? "+ Style.RESET_ALL )

    # if user_input == "yes":
    #     print("Thank you!")
    # else:
    #     print("Well this is awkward...")

    
    while (True):
        print(Fore.GREEN + "\nReview Menu" + Style.RESET_ALL)
        print(Fore.CYAN + "\t1. Review this year" + Style.RESET_ALL)
        print(Fore.BLUE + "\t2. Review previous year" + Style.RESET_ALL)
        print(Fore.YELLOW + "\t3. Total Review" + Style.RESET_ALL)
        print(Fore.RED + "\t4. Quit" + Style.RESET_ALL)
        print("\n")

        user_input = input(Fore.GREEN + "Enter your choice: " + Style.RESET_ALL)

        match user_input:
            case "1":
                # review_this_year()
                pass
            case "2":
                # review_previous_year()
                pass
            case "3":
                # total_review()
                review.analyze_messages(messages_df)
                pass
            case "4":
                break
            case _:
                print(Fore.RED + "Invalid input!" + Style.RESET_ALL)
                continue
    
    
    print(Fore.GREEN + "Thank you!" + Style.RESET_ALL)

    

if __name__ == '__main__':
    main()