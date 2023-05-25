# coding: utf-8
#
#
#!!!ВНИМАНИЕ!!!
#Я не разработчик бота, я пофиксил некоторые баги и всё, разраб бота - ! ARMAGEDDON#7393
#
#

import os
import json
import aiohttp
import asyncio
import discord
import subprocess
import datetime
from utils import *
from os import system, name
from discord.ext.commands.core import cooldown
from discord import Permissions

from discord.ext import (
    commands,
    tasks
)

#https://discord.com/api/oauth2/authorize?client_id=1106322966490386542&permissions=8&scope=bot



intents = discord.Intents.all()
client = commands.Bot(command_prefix=prefix, intents=intents)
client.remove_command('help')

@client.command()
async def spam_send(ctx, count):
    try:
        with open(spam_text_file, 'r') as spam_text_n:
            spam_text = spam_text_n.read()
        await ctx.send(spam_text.strip('\"'))
    except Exception as e: print(e)

@client.command()
async def loadcog(ctx, extension):
    if ctx.author.id == 695690814491328642:
        await client.load_extension(f"cogs.{extension[:-3]}")
        await ctx.send("Cogs loaded!")
    else:
        await ctx.send("You are not a bot developer.")


@client.command()
async def unload(ctx, extension):
    if ctx.author.id == 695690814491328642:
        await client.unload_extension(f"cogs {extension}")
        await ctx.send("Cogs unloaded!")
    else:
        await ctx.send("You are not a bot developer.")


@client.command()
async def reload(ctx, extension):
    if ctx.author.id == 695690814491328642:
        await client.unload_extension(f"cogs {extension}")
        await client.load_extension(f"cogs {extension}")
        await ctx.send("Cogs reloaded!")
    else:
        await ctx.send("You are not a bot developer.")


@client.event
async def on_ready():
    print(f''' [] Nick: {client.user}
        [] Link: https://discord.com/api/oauth2/authorize?client_id={client.user.id}&permissions=8&scope=bot''')
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await client.load_extension(f"cogs.{filename[:-3]}")


client.run(token)
