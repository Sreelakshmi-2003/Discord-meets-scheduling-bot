import discord
from discord.ext import commands
from asyncio import sleep as s
import json
import requests


intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix = '!' , intents = intents)

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
    channel = client.get_channel(1045640085963546669)
    await channel.send("Hello")


@client.event
async def on_member_remove(member):
    channel = client.get_channel(1045640085963546669)
    await channel.send("Goodbye")



@client.command()
async def reminder(ctx,time: int,,msg):
    while True:
        await s(10time)
        await ctx.send(f'{msg},{ctx.author.mention}')
        if(ctx.author.message.content=='stop'):
            await ctx.send('stopped')
            break;