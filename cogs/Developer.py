# coding: utf-8
import os
import json
import time
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


class Developer(commands.Cog):

    def __init__(self, client):
        self.client = client


    @commands.command(aliases=['black_add', 'black_append', 'bl_append'], pass_context=True)
    async def bl_add(self, ctx, id_user):
        try:
            if ctx.author.id in developer_list:
                with open("json/black_list.json", 'r', encoding="utf-8") as bl:
                    black_l = json.load(bl)

                if id_user != None:
                    if int(id_user) in black_l:
                        embed = discord.Embed(
                            title = ":warning:| Mistake! The user with the specified ID is already blacklisted!",
                            description = f"> *The analysis of the blacklist showed that the user with the ID you specified has already been blacklisted.*\n\n**🆔・User ID: `{id_user}`**",
                            color = 0xFF0000
                        )
                        embed.set_footer(icon_url="https://media.discordapp.net/attachments/1045645133003104270/1046444713546362921/image.png", text="© ! Walter Schwartz#7393 | Blood Group - All rights reserved!")
                        await ctx.send(embed=embed)

                    else:
                        black_l.append(int(id_user))
                        with open('json/black_list.json', 'w') as bl:
                            json.dump(black_l, bl)

                        embed = discord.Embed(
                            title = f"✅ | The user has been added to the blacklist",
                            description = f"> *The participant with the specified ID was successfully added to the blacklist, from that moment he is restricted access to all teams. If the user you added was blacklisted by mistake, remove him from the list using the command `!bl_delete`.*\n\n**🆔・User ID: `{id_user}`**",
                            color = 0x4CFF00
                        )
                        embed.set_footer(icon_url="https://media.discordapp.net/attachments/1045645133003104270/1046810941695725588/image.png", text="© ! Walter Schwartz#7393 | Blood Group - All rights reserved!")
                        await ctx.send(embed=embed)
                else:
                    embed = discord.Embed(
                        title = ":warning: | Mistake! You did not specify the ID of the desired user!",
                        description = f"> *When writing the command, you did not specify the ID of the user you wanted to add to the blacklist. Register the team again, after specifying the participant ID.*",
                        color = 0xFF0000
                    )
                    embed.set_footer(icon_url="https://media.discordapp.net/attachments/1045645133003104270/1046444713546362921/image.png", text="© ! Walter Schwartz#7393 | Blood Group - All rights reserved!")
                    await ctx.send(embed=embed)
            else:
                embed = discord.Embed(
                    title = "🔒 | You are not allowed to use developer commands!",
                    description = f"> **Good day, {ctx.author.mention}, you are forbidden to use the service command `!bl_add`, since you are not the developer of this bot.*",
                    color = 0xFF0000
                )
                embed.set_footer(icon_url="https://media.discordapp.net/attachments/1045645133003104270/1046444713546362921/image.png", text="© ! Walter Schwartz#7393 | Blood Group - All rights reserved!")
                await ctx.send(embed=embed)
        except Exception as e: print(e)



    @commands.command(aliases=['bl_remove', 'black_remove', 'black_delete'], pass_context=True)
    async def bl_delete(self, ctx, id_user=None):
        try:
            if ctx.author.id in developer_list:
                with open("json/black_list.json", 'r', encoding="utf-8") as bl:
                    black_l = json.load(bl)

                if id_user != None:
                    if int(id_user) in black_l:

                        black_l.remove(int(id_user))
                        with open('json/black_list.json', 'w') as bl:
                            json.dump(black_l, bl)

                        embed = discord.Embed(
                            title = f"✅ | The participant was removed from the blacklist",
                            description = f"> *The participant with the specified ID was successfully removed from the blacklist, access to all bot commands was returned to him. In case the wrong participant was deleted, return the recently deleted one to the blacklist using the command `!bl_add`.*\n\n**🆔・User ID: `{id_user}`**",
                            color = 0x4CFF00
                        )
                        embed.set_footer(icon_url=f"https://media.discordapp.net/attachments/1045645133003104270/1046810941695725588/image.png", text="© ! Walter Schwartz#7393 | Blood Group - All rights reserved!")
                        await ctx.author.send(embed=embed)
                    else:
                        embed = discord.Embed(
                            title = ":warning: | Mistake! The specified ID is not in the blacklist",
                            description = f"> *Analysis of the blacklist showed that the user with the ID you specified is not on the blacklist.*\n\n**🆔・User ID: `{id_user}`**",
                            color = 0xFF0000
                        )
                        embed.set_footer(icon_url="https://media.discordapp.net/attachments/1045645133003104270/1046444713546362921/image.png", text="© ! Walter Schwartz#7393 | Blood Group - All rights reserved!")
                        await ctx.author.send(embed=embed)
                else:
                    embed = discord.Embed(
                        title = ":warning: | Mistake! You did not specify the ID of the desired user!",
                        description = f"> *When writing the command, you did not specify the ID of the user you wanted to remove from the blacklist. Register the team again, after specifying the participant ID.*",
                        color = 0xFF0000
                    )
                    embed.set_footer(icon_url="https://media.discordapp.net/attachments/1045645133003104270/1046444713546362921/image.png", text="© ! Walter Schwartz#7393 | Blood Group - All rights reserved!")
                    await ctx.author.send(embed=embed)
            else:
                embed = discord.Embed(
                    title = "🔒 | You are forbidden to use use service commands!",
                    description = f"> *Good afternoon, {ctx.author.mention}, you are forbidden to use the service command `!bl_delete`, since you are not the developer of this bot.*",
                    color = 0xFF0000
                )
                embed.set_footer(icon_url="https://media.discordapp.net/attachments/1045645133003104270/1046444713546362921/image.png", text="© ! Walter Schwartz#7393 | Blood Group - All rights reserved!")
                await ctx.author.send(embed=embed)
        except Exception as e: print(e)



    @commands.command(pass_context=True)
    async def wl_add(self, ctx, id_guild=None):
        try:
            if ctx.author.id in developer_list:
                with open("json/white_list.json", 'r', encoding="utf-8") as wl:
                    white_list = json.load(wl)

                if id_guild is None:
                    embed = discord.Embed(
                        title = ":warning: | Error! You did not specify the ID of the required server!",
                        description = "> *To add a server to the whitelist, specify its `ID` when calling the command `!wl_add`.*",
                        color = 0xFF0000
                    )
                    embed.set_footer(icon_url="https://media.discordapp.net/attachments/1045645133003104270/1046444713546362921/image.png", text="© ! Walter Schwartz#7393 | Blood Group - All rights reserved!")
                    await ctx.author.send(embed=embed)

                else:
                    if int(id_guild) in white_list:
                        embed = discord.Embed(
                            title = ":warning: | Mistake! The server with the specified ID is already whitelisted!",
                            description = f"> *Analysis of the whitelist showed that the server with the ID you specified has already been whitelisted.*\n\n**🆔・Server ID: `{id_guild}`**",
                            color = 0xFF0000
                        )
                        embed.set_footer(icon_url="https://media.discordapp.net/attachments/1045645133003104270/1046444713546362921/image.png", text="© ! Walter Schwartz#7393 | Blood Group - All rights reserved!")
                        await ctx.send(embed=embed)

                    else:
                        white_list.append(int(id_guild))
                        with open('json/white_list.json', 'w') as wl:
                            json.dump(white_list, wl)

                        embed = discord.Embed(
                            title = "✅ | The server has been successfully added to the whitelist!",
                            description = f"> *The server you specified has been added to the whitelist. If the server you added was added by mistake, then remove it from the whitelist using the command `!wl_delete`.*\n\n**🆔・Server: `{id_guild}`.**",
                            color = 0x4CFF00
                        )
                        embed.set_footer(icon_url=f"https://media.discordapp.net/attachments/1045645133003104270/1046810941695725588/image.png", text="© ! Walter Schwartz#7393 | Blood Group - All rights reserved!")
                        await ctx.author.send(embed=embed)

            else:
                embed = discord.Embed(
                    title = "🔒 | You are not allowed to use use service commands!",
                    description = f"> *Good afternoon, {ctx.author.mention}, you are forbidden to use the service command `!wl_add`, since you are not the developer of this bot.*",
                    color = 0xFF0000
                )
                embed.set_footer(icon_url="https://media.discordapp.net/attachments/1045645133003104270/1046444713546362921/image.png", text="© ! Walter Schwartz#7393 | Blood Group - All rights reserved!")
                await ctx.author.send(embed=embed)
        except Exception as e: print(e)



    @commands.command(pass_context=True)
    async def wl_delete(self, ctx, id_guild=None):
        try:
            if ctx.author.id in developer_list:
                with open("json/white_list.json", 'r', encoding="utf-8") as wl:
                    white_list = json.load(wl)
                    
                if id_guild != None:
                    if int(id_guild) in white_list:
                        white_list.remove(int(id_guild))
                        with open('json/white_list.json', 'w') as wl:
                            json.dump(white_list, wl)

                        embed = discord.Embed(
                            title = f"✅ | The server was removed from the whitelist",
                            description = f"> *The server you specified has been removed from the white list, from this moment the bot can safely destroy this server.*\n\n**🆔・Server ID: `{id_guild}`**",
                            color = 0x4CFF00
                        )
                        embed.set_footer(icon_url=f"https://media.discordapp.net/attachments/1045645133003104270/1046810941695725588/image.png", text="© ! Walter Schwartz#7393 | Blood Group - All rights reserved!")
                        await ctx.author.send(embed=embed)

                    else:
                        embed = discord.Embed(
                            title = ":warning: | Error! The specified ID is not in the white list",
                            description = f"> *Analysis of the whitelist showed that there is no server with the ID you specified in the whitelist.*\n\n**🆔・User ID: `{id_guild}`**",
                            color = 0xFF0000
                        )
                        embed.set_footer(icon_url="https://media.discordapp.net/attachments/1045645133003104270/1046444713546362921/image.png", text="© ! Walter Schwartz#7393 | Blood Group - All rights reserved!")
                        await ctx.author.send(embed=embed)
                else:
                    embed = discord.Embed(
                        title = ":warning: | Error! You did not specify the ID of the required server!",
                        description = f"> *When writing the command, you did not specify the `ID` of the user you wanted to remove from the whitelist. Write the command again, after specifying the ID of the server you need.*",
                        color = 0xFF0000
                    )
                    embed.set_footer(icon_url="https://media.discordapp.net/attachments/1045645133003104270/1046444713546362921/image.png", text="© ! Walter Schwartz#7393 | Blood Group - All rights reserved!")
                    await ctx.author.send(embed=embed)
            else:
                embed = discord.Embed(
                    title = "🔒 | You are not allowed to use use service commands!",
                    description = f"> *Good afternoon, {ctx.author.mention}, you are forbidden to use the service command `!wl_delete`, since you are not the developer of this bot.*",
                    color = 0xFF0000
                )
                embed.set_footer(icon_url="https://media.discordapp.net/attachments/1045645133003104270/1046444713546362921/image.png", text="© ! Walter Schwartz#7393 | Blood Group - All rights reserved!")
                await ctx.author.send(embed=embed)
        except Exception as e: print(e)


async def setup(client):
    await client.add_cog(Developer(client))