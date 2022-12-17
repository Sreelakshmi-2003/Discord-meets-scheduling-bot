import discord
from discord.ext import commands

from bottoken import *

intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix = '!' , intends = intents)

@client.event
async def on_ready():
    print("The bot is now ready to use!")
    print("............................")
    
    
@client.command()
async def hello(ctx):
    await ctx.send("HEllo i am a bot")
    
@client.command()
async def goodbye(ctx):
    await ctx.send("hope you have a good day")
    
    
@client.event
async def on_member_join(member):
    channel = client.get_channel('')
    await channel.send("HEllo")

    
client.run(TOKEN)