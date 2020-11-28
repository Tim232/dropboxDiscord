# -*-coding: utf-8-*-

import dropbox
import discord
import asyncio
from discord.ext import commands

async def backup(bot:commands.Bot, token:str, ctx:commands.context.Context, available:list):
    dbx = dropbox.Dropbox(token)
    backups = '\n'.join(available).strip()
    embed = discord.Embed(title=":outbox_tray: **INFO**", description=(f"**Files** - \n{backups}"))
    backup_message = await ctx.send(embed=embed)
    await backup_message.add_reaction("✅")
    await backup_message.add_reaction("❎")
    def check_backup(reaction, user):
        return user == ctx.author and str(reaction.emoji) in ["✅","❎"]
    try:
        reaction, user = await bot.wait_for('reaction_add', timeout=5.0, check=check_backup)
    except asyncio.TimeoutError:
        embed = discord.Embed(title=":warning: **WARN**", description="Timeout")
        await backup_message.edit(embed=embed)
    else:
        if str(reaction.emoji) == "✅":
            embed = discord.Embed(title=":outbox_tray: **INFO**", description=(f"**Loading...** - \n{backups}"))
            await backup_message.edit(embed=embed)
            for z in available:
                with open(z, 'rb') as f:
                    dbx.files_upload(f.read(), z)
                backups = backups.replace(z, f"{z} :white_check_mark:")
                embed = discord.Embed(title=":outbox_tray: **INFO**", description=(f"**Loading...** - \n{backups}"))
                await backup_message.edit(embed=embed)
            embed = discord.Embed(title=":outbox_tray: **INFO**", description=(f"**Done** - \n{backups}"))
            await backup_message.edit(embed=embed)
        else: #elif str(reaction.emoji) == "❎":
            embed = discord.Embed(title=":outbox_tray: **INFO**", description="**Canceled**")
            await backup_message.edit(embed=embed)
