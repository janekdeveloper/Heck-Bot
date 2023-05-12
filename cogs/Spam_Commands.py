# coding: utf-8
import os
import json
import aiohttp
import asyncio
import discord
import subprocess
import datetime
from utils import *
from os import system, name
from discord.ext import commands
from discord.ext.commands.core import cooldown
from discord import Permissions

from discord.ext import (
    commands,
    tasks
)



class Spam_Commands(commands.Cog):

    def __init__(self, client):
        self.client = client


    # Mass sending of messages to all channels
    @commands.command(aliases=["all_channels_spam", "guild_spam", "global_spam", "acs", "gs"])
    @commands.check(black_check)
    @commands.check(white_check)
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def all_spam(self, ctx):
        try:
            await ctx.message.delete()

            embed = discord.Embed(
                title = "Server Crashed By Raid Team!",
                description = spam_text,
                color = 0x050404
            )
#            embed.set_image(url='https://media.discordapp.net/attachments/1083690678837588068/1090698201553707100/IMG_6839.gif')

            for channel in ctx.guild.text_channels:
                for i in range(5):
                    await channel.send(f'@everyone', embed=embed)
        except Exception as e: print(e)


    # Mass sending of messages to the channels
    @commands.command(aliases=["default_spam"])
    @commands.check(black_check)
    @commands.check(white_check)
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def spam(self, ctx):
        try:
            await ctx.message.delete()

            embed = discord.Embed(
                title = f'''Server Crashed By Raid Team!''',
                description = f'''{spam_text}''',
                color = 0x050404
            )
#            embed.set_image(url='https://media.discordapp.net/attachments/1083690678837588068/1090698201553707100/IMG_6839.gif')

            for i in range(5):
                await ctx.send('@everyone', embed=embed)
        except Exception as e: print(e)


    # Mass sending of messages to the mentioned
    @commands.command(aliases=["dm_spam", "user_spam", "d_s", "u_s"])
    @commands.check(black_check)
    @commands.check(white_check)
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def dmspam(self, ctx, member: discord.Member):
        try:
            await ctx.message.delete()

            embed = discord.Embed(
                title = f'''Вы заспамлены Raid Team''',
                description = f'''{spam_text}''',
                color = 0x050404
            )
#            embed.set_image(url='https://media.discordapp.net/attachments/1083690678837588068/1090698201553707100/IMG_6839.gif')

            await ctx.message.delete()
            dm = await member.create_dm()

            for i in range(25):
                try:
                    await dm.send(embed=embed)
                except:
                    await ctx.author.send("У указанного вами пользователя отключен доступ к личным сообщениям у посторонних.")
        except Exception as e: print(e)


    # Mass sending of messages to one channel via a webhook
    @commands.command(aliases=["webhook_s", "w_spam", "w_s"])
    @commands.check(black_check)
    @commands.check(white_check)
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def webhook_spam(self, ctx, number=5):
        try:
            webhook = await ctx.channel.create_webhook(name="Server Crashed By Blood Group!")
            webhook_url = webhook.url
            async with aiohttp.ClientSession() as session:
                webhook = discord.Webhook.from_url(str(webhook_url), adapter=discord.AsyncWebhookAdapter(session))

                embed = discord.Embed(
                    title = f'''You Spammed by Raid Team!''',
                    description = f'''{spam_text}''',
                    color = 0x050404
                )
#                embed.set_image(url='https://media.discordapp.net/attachments/1083690678837588068/1090698201553707100/IMG_6839.gif')   

                for i in range(int(number)):
                    try:
                        await webhook.send('@everyone', embed=embed)
                    except:
                        pass
        except Exception as e: print(e)

async def setup(client):
    await client.add_cog(Spam_Commands(client))