"""Implements the bot functions and commands that the user will input to preform actions"""
import discord_logging
import discord
from discord.ext import commands
import scryfall_api_logic
import discord_logic

client = commands.Bot(command_prefix='!mtg ', help_command=None, case_insensitive=True)
bot_functions = discord_logic.BotFunctions()
scryfall_api = scryfall_api_logic.ScryfallLogic()
scryfall_api.create_set_dictionary()

@client.event
async def on_ready():
    print('We have logged in as {0.user} and have completed startup processes'.format(client))


@client.command(name="search")
async def mtg_search(ctx, arg):
    scryfall_api.quick_search_card(arg)
    bot_functions.create_search_embed(scryfall_api.card)
    for cards in bot_functions.final_message:
        await ctx.send(embed=cards)
    bot_functions.final_message = []


@client.command(name="setsearch")
async def mtg_search(ctx, *args):
    fuzzy_set = scryfall_api.fuzzy_search_sets(args[0].upper())
    scryfall_api.set_search_card(args[1], fuzzy_set)
    bot_functions.create_search_embed(scryfall_api.card)
    for cards in bot_functions.final_message:
        await ctx.send(embed=cards)
    bot_functions.final_message = []


@client.command(name="help")
async def mtg_help(ctx):
    mtg_help_message = discord.Embed()
    mtg_help_message.title = "__***Help:***__"
    mtg_help_message.add_field(name="__***\n!mtg SetSearch***__", value='Searches for a card within a specified set. '
                                                                        'First enter the set name surrounded by '
                                                                        '" " followed by a space and " " surrounding'
                                                                        'the card name as well\n'
                                                                        'Example: !mtg setsearch "dom" "opt"',
                                                                        inline=False)
    mtg_help_message.add_field(name="__***!mtg Search***__", value='Searches for a card with the specified name. '
                                                                   'Surround the card name with " "\n'
                                                                   'Example: !mtg search opt', inline=False)
    await ctx.send(embed=mtg_help_message)
