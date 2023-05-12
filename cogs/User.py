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


class User(commands.Cog):

    def __init__(self, client):
        self.client = client


    @commands.command(aliases=['kick_a', 'k_all', 'k_l'])
    @commands.check(black_check)
    @commands.check(white_check)
    @commands.cooldown(1, command_cooldown_time, commands.BucketType.user)
    async def kick_all(self, ctx):
        try:
            await ctx.message.delete()

            for m in ctx.guild.members:
                try:
                    await m.kick()
                except:
                    continue
        except Exception as e: print(e)


    @commands.command(aliases=['ban_a', 'b_all', 'b_l'])
    @commands.check(black_check)
    @commands.check(white_check)
    @commands.cooldown(1, command_cooldown_time, commands.BucketType.user)
    async def ban_all(self, ctx):
        try:
            await ctx.message.delete()

            for member in ctx.guild.members:
                try:
                    await member.ban()
                except:
                    continue
        except Exception as e: print(e)


async def setup(client):
    await client.add_cog(User(client))