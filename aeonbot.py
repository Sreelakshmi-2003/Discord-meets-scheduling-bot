import discord
from discord.ext import commands

from apikeys import *

intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix = '!' , intends = intents)

@client.event
async def on_ready():
    print("The bot is now ready to use!")
    print("............................")
    
    
@client.command()
async def hello(ctx):
    await ctx.send("HEllo i am a youtube bot")
    
    
@client.event
async def on_member_join(member):
    channel = client.get_channel('')
    await channel.send("HEllo")

    
    
client.run('MTA0NTY0MDcwODkyMjU0ODMyNA.GJ1O7k.pX6NOh4Yyrh4MYWMK8HUdiOh3bA3s8HO71O4wc')