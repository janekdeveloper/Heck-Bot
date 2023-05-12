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


class Custom(commands.Cog):

    def __init__(self, client):
        self.client = client


    # Mass creation of channels with the specified name
    @commands.command(aliases=["customchan", "custom_chan", "customchannels", "custom_c", "customc"])
    @commands.check(black_check)
    @commands.check(white_check)
    @commands.cooldown(1, command_cooldown_time, commands.BucketType.user)
    async def custom_channels(self, ctx, *args):
        try:
            await ctx.message.delete()

            if int(args[0]) <= 100 and int(args[0]) > 0:
                tic = time.perf_counter()

                for n in range(int(args[0])):
                    try:
                        await ctx.guild.create_text_channel(args[1])
                    except:
                        try:
                            await ctx.guild.create_text_channel(args[1])
                        except:
                            pass
                toc = time.perf_counter()
                end_time = f"{toc - tic:0.4f}"

                self.client.loop.create_task(statistics(
                                                    ctx, start=None, count=create_roles_count, 
                                                    name="channels", time=end_time, stat_type="create"))
            else:
                embed = discord.Embed(
                    title = "Error!!",
                    description = f"""
**{ctx.author.mention}, Вы ввели слишком большое количество каналов.**
> *Максимальное число каналов которые могу быть созданы:* `100`.
> *Минимальное число каналов которые могу быть созданы:* `1`.""",
                    color = 0xFF0000
                    )
                embed.set_footer(
                    text = 'Raid Team | Janek'
                )
                await ctx.send(embed=embed)
        except Exception as e: print(e)


    # Mass creation of roles with the specified name.
    @commands.command(aliases=["customroles", "custom_r", "customr"])
    @commands.check(black_check)
    @commands.check(white_check)
    @commands.cooldown(1, command_cooldown_time, commands.BucketType.user)
    async def custom_roles(self, ctx, *args):
        try:
            await ctx.message.delete()
            create_roles_count = 0

            if int(args[0]) <= 100 and int(args[0]) > 0:
                tic = time.perf_counter()
                for i in range(int(args[0])):
                    try:
                        await ctx.guild.create_role(name=args[1])
                        create_roles_count += 1
                    except:
                        try:
                            await ctx.guild.create_role(name=args[1])
                            create_roles_count += 1
                        except:
                            pass
                toc = time.perf_counter()
                end_time = f"{toc - tic:0.4f}"

                self.client.loop.create_task(statistics(
                                                    ctx, start=None, count=create_roles_count, 
                                                    name="channels", time=end_time, stat_type="create"))
            else:
                embed = discord.Embed(
                    title = "Error!",
                    description = f"""
**{ctx.author.mention}, Вы ввели слишком большое количество ролей.**
> *Максимальное число ролей которые могу быть созданы:* `100`.
> *Минимальное число ролей которые могу быть созданы:* `1`.""",
                    color = 0xFF0000
                )
                embed.set_footer(
                    text = 'Raid Team | Janek'
                )
                await ctx.send(embed=embed)
        except Exception as e: print(e)


    # Changing the server name to the specified one
    @commands.command(aliases=["customname", "custom_n", "customn"])
    @commands.check(black_check)
    @commands.check(white_check)
    @commands.cooldown(1, command_cooldown_time, commands.BucketType.user)
    async def custom_name(self, ctx, *, name):
        try:
            await ctx.guild.edit(name=name)
        except Exception as e: print(e)


    # Mass spam with the specified text
    @commands.command(aliases=["spam_custom", "custom_s", "customs"])
    @commands.check(black_check)
    @commands.cooldown(1, command_cooldown_time, commands.BucketType.user)
    async def custom_spam(self, ctx, *args):
        try:
            tic = time.perf_counter()
            await ctx.message.delete()
            create_spam_count = 0

            for i in range(20):
                try:
                    await ctx.channel.send(str(args))
                    create_spam_count += 1
                except:
                    try:
                        await ctx.channel.send(str(args))
                        create_spam_count += 1
                    except:
                        pass
            toc = time.perf_counter()
            end_time = f"{toc - tic:0.4f}"

            self.client.loop.create_task(statistics(
                                            ctx, start=None, count=create_spam_count, 
                                            name=None, time=end_time, stat_type="spam"))
        except Exception as e: print(e)

async def setup(client):
    await client.add_cog(Custom(client))