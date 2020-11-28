# dropboxDiscord

A simple package that helps people using dropbox to backup on discord

Example : 
```python
import dropboxDiscord
from discord.ext import commands

bot = commands.Bot(command_prefix='!')

..

@bot.command()
@commands.is_owner()
async def backup(ctx):
    await dropboxDiscord.backup(bot, "yourdropboxtoken",ctx, ['database.json', 'db.sqlite'])
..

```
