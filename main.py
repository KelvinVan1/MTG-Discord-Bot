import asyncio
import discord.errors
import discord_bot_action
from os.path import exists
from os import makedirs


def create_token() -> None:
    """Ask the user if they wish to create a new token and if so obtain the token from the user"""
    while True:
        user_input = input("No token was found! Do you wish to create the token file? (Y/N): ")
        if user_input.upper() == 'Y':
            if not _check_path():
                makedirs("Token/")
            token_file = open("Token/token.txt", "x")
            token_file.write(input("Please enter the Token of your discord bot: "))
            token_file.close()
            return 0
        elif user_input.upper() == 'N':
            return 0
        else:
            print("Invalid input, please try again")


def start_bot() -> None:
    if check_token():
        try:
            token_file = open("Token/token.txt", "r")
            discord_bot_action.client.run(token_file.read())
            token_file.close()
        except discord.errors.LoginFailure or discord.errors.HTTPException:
            print("Invalid token. Please restart the program and change the token or correct the token.txt file.")
            input("Press enter to close the program.")


def change_token() -> None:
    token_file = open("Token/token.txt", "w")
    token_file.write(input("Please enter the Token of your discord bot: "))
    token_file.close()


def check_token() -> bool:
    """Checks to see if the token.txt file is found in the path Token"""
    return exists("Token/token.txt")


def _check_path() -> bool:
    """Checks to see if the Token folder exists"""
    return exists("Token/")


if __name__ == '__main__':
    if not check_token():
        create_token()

    print("Welcome to the MTG Discord Bot \n"
          "Please choose one of the options below to continue\n\n"
          "1 : Start Program\n"
          "2 : Change Token Key")
    user_choice = input("Enter either 1 or 2: ")

    if user_choice == "1":
        start_bot()
    elif user_choice == "2":
        change_token()
        start_bot()






