"""Script instagram"""

import getpass
import time
import os
from instagrapi import Client
from instagrapi.exceptions import (
    TwoFactorRequired,
    UnknownError,
    LoginRequired,
)


def clear_screen():
    """
    Clears the console screen.
    """
    time.sleep(1)
    os.system("cls")


clear_screen()
cl = Client()

username = getpass.getpass("Username: ")
password = getpass.getpass("Password: ")
def login():
    """
    A function that handles the login process by prompting the user for a username and password. 
    If a TwoFactorRequired exception is raised, the user is prompted for a 2FA code. 
    If an UnknownError exception is raised during 2FA verification, it informs the user and retries. 
    Upon successful login, it sets the delay range for the client. 
    """
    while True:

        try:
            cl.login(username, password)
            break
        except TwoFactorRequired:
            print("2FA required")
            code = getpass.getpass("2FA code: ")
            try:
                cl.login(username, password, verification_code=code)
                break
            except UnknownError:
                print("Invalid 2FA code, trying again...")
                clear_screen()
                continue
    print("Login successful!")
    cl.delay_range = (1, 3)

login()


while True:
    clear_screen()
    option = input(
        """
    Select an Option:
    1. Like photos based on hashtag 
    0. Exit
"""
    )

    if option == "1":
        hashtag = input("Enter hashtag: ")
        amount = int(input("Enter quantity: "))
        medias = cl.hashtag_medias_recent(hashtag, amount)
        medias_to_like = [media.id for media in medias]
        i = 0
        for media in medias_to_like:
            try:
                cl.media_like(media)
                os.system("cls")
                i += 1
                print(f"Liked {i} photos out of {len(medias_to_like)}")
            except LoginRequired:
                print('Failed, trying to relogin...')
                cl.relogin()
        print("Done!")
        input("Press Enter to continue...")

    elif option == "0":
        print("Bye!")
        break

    else:
        print("Invalid option!")
