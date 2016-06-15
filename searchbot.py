import discord
import sys
from discord.ext import commands
from derpibooru import Search, sort

bot = commands.Bot(command_prefix='>>', description="search bot")

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command()
async def search(*tags: str):
    """seraches derpibooru"""
    try:
        imgs = [img for img in Search().query(*tags).sort_by(sort.RANDOM)]
        url = imgs[0].full
        await bot.say(url)
    except:
        await bot.say("Invalid search term")

if len(sys.argv) < 2:
    print("usage " + str(sys.argv[0]) + " token")
    exit(0)

bot.run(sys.argv[1])
