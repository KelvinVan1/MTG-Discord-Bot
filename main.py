import discord_bot_action

TOKEN_KEY = open("Token/token.txt", "r")


if __name__ == '__main__':
    discord_bot_action.client.run(TOKEN_KEY.read())
    TOKEN_KEY.close()

