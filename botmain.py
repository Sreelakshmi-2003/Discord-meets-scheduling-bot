import discord
from discord.ext import commands
from discord import DMChannel
import os
import schedule
import datetime
import threading
from dotenv import load_dotenv

project_folder = os.path.expanduser("C:")  # adjust as appropriate
load_dotenv(os.path.join(project_folder, 'distoken.env'))

intents = discord.Intents.default()
intents.members = True
intents.message_content = True  # Added to handle message content in on_message
client = commands.Bot(command_prefix='$', intents=intents)

meetings = []
users = {}

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    if client.user.name != "aeon":
        await client.user.edit(username="aeon")
    with open('icon.png', 'rb') as image:
        await client.user.edit(avatar=image.read())
    # Start periodic check
    threading.Thread(target=checkTime, daemon=True).start()

@client.event
async def on_member_join(member):
    channel = client.get_channel(channel_id)
    await channel.send("Hello")

@client.event
async def on_member_remove(member):
    channel = client.get_channel(channel_id)
    await channel.send("Goodbye")

def checkTime():
    # This function runs periodically every 60 seconds
    threading.Timer(60, checkTime).start()

    time_now = datetime.datetime.now().strftime("%H:%M")
    date_now = datetime.datetime.today().strftime('%Y-%m-%d')
    now = date_now + " " + time_now

    for meeting in meetings:
        meeting_time = meeting.getDateTime().strftime("%Y-%m-%d %H:%M")

        if str(meeting_time) == str(now):
            # Trigger dm_missing
            # Process command `missing`
            channel = client.get_channel(channel_id)  
            if channel:
                message = await channel.fetch_message(meeting.getMessageId())  # Fetch the message for the meeting
                await dm_missing(message)

def addUser(user):
    if user.id not in users:
        users[user.id] = []

def addUserMeeting(user, meeting):
    addUser(user)
    if meeting.getName() not in users[user.id]:
        users[user.id].append(meeting.getName())

def removeUserMeeting(user, meeting):
    if meeting.getName() in users.get(user.id, []):
        users[user.id].remove(meeting.getName())
    print(users)

async def dm_missing(message):
    author = message.author
    if author.voice is None:
        await message.channel.send('Sorry, you are not currently in a voice channel.')
    else:
        channel = author.voice.channel
        now = datetime.datetime.now()
        current_time = now.strftime('%H:%M')
        current_date = now.strftime('%B %d, %Y')

        for meeting in meetings:
            if meeting.getDateTime() <= now <= meeting.getEndDateTime():
                if not admin_authentication(author, meeting):
                    await message.channel.send(f"{author} could not ping everyone missing for the meeting {meeting.getName()}")
                    return
                missing = meeting
                await message.channel.send(f'{meeting.getName()} is taking place right now')
                for person in missing.getParticipants():
                    if person.voice is None or person.voice.channel != channel:
                        await person.send(f'{meeting.getName()} is taking place right now! Come to {channel} to join!')
                await message.channel.send(f"{author} pinged everyone missing for the meeting {meeting.getName()}")
                return

async def helpCommands(message):
    embed_help = discord.Embed(title="Help Center:", color=0x685BC7)
    msg = """Welcome to the aeon bot! \nHere are some of the commands you can use:
    \n ```$meeting - allows you to schedule a new meeting 
    \n you can mix and match these parameters but make sure you have the title!
    \n parameters: 
    \n title: **all meetings must have this** (e.g. $meeting party)
    \n start time: 24h-time, defaults to current time (e.g. $meeting party 13:35)
    \n duration: defaults to 1 hour (e.g. $meeting party 13:35 1:45)
    \n date: defaults to current date (e.g. $meeting party 24/01/2021)
    \n participants: @ any users you want to schedule for the meeting (e.g. $meeting party @joe)
    \n description: put your meeting description in between ' ' (e.g. $meeting party 'susan's birthday!')
    \n auto remind: use TRUE or FALSE to turn auto remind on or off, defaults to FALSE (e.g. $meeting party TRUE)```
    ```$show_meetings - will show all currently scheduled meetings```
    ```$my_meetings - sends you a direct message of all of your scheduled meetings```
    ```$edit - lets meeting organizer/administrator(s) edit meeting details```
    ```$delete_meeting - allows the meeting organizer/adminstrator(s) to delete a meeting given its name```
    ```$add_admin - adds an administrator to the meeting given the meeting name and the @ of the new administrator (e.g. $add_admin party @bob)```
    ```$remove_admin - removes an administrator to the meeting given the meeting name and the @ of the old administrator (e.g. $remove_admin party @bob)```
    ```$missing - checks the sender's voice channel to see if all meeting attendees are present and sends a direct message to those who are missing```
    """
    embed_help.description = msg
    await message.channel.send(embed=embed_help)

async def parse_meeting_info(parameters):
    meeting_time = None
    meeting_date = None
    meeting_duration = None
    start_recorded = False
    participants = []
    desc = ''
    auto_remind = None
    copy_desc = False

    for param in parameters:
        # Time parameter HH:MM (24HR)
        if ':' in param and len(param) >= 3:
            if not start_recorded:
                try:
                    minutes = int(param[3:])
                except ValueError:
                    minutes = 0
                meeting_time = datetime.time(int(param[:2]), minutes)
                start_recorded = True
            else:
                try:
                    minutes = int(param[3:])
                except ValueError:
                    minutes = 0
                meeting_duration = datetime.timedelta(hours=int(param[:2]), minutes=minutes)

        # Time parameter alternate format H:MM (24HR)
        elif ':' in param and len(param) >= 2:
            if not start_recorded:
                try:
                    minutes = int(param[2:])
                except ValueError:
                    minutes = 0
                meeting_time = datetime.time(int(param[:1]), minutes)
                start_recorded = True
            else:
                try:
                    minutes = int(param[2:])
                except ValueError:
                    minutes = 0
                meeting_duration = datetime.timedelta(hours=int(param[:1]), minutes=minutes)

        # Date parameter DD/MM/YYYY
        if len(param) == 5 and param[2] == '/':
            meeting_date = datetime.date(datetime.datetime.now().year, int(param[3:]), int(param[:2]))
        elif len(param) == 10 and param[2] == '/' and param[5] == '/':
            meeting_date = datetime.date(int(param[6:]), int(param[3:5]), int(param[:2]))

        # Participants parameter - all the @ users
        if param.startswith('<@!'):
            participants.append(await client.guilds[0].fetch_member(int(param[3:-1])))

        # Description parameter start - string (in quotes)
        if param.startswith("'"):
            copy_desc = True
            param = param[1:]
            desc = ""

        # End of description
        if param.endswith("'"):
            copy_desc = False
            desc += param[:-1]

        # Add part of the description
        if copy_desc:
            desc += param + ' '

        # Auto-remind parameter - TRUE or FALSE
        if param.lower() == "true":
            auto_remind = True
        elif param.lower() == 'false':
            auto_remind = False

    return meeting_time, meeting_duration, meeting_date, participants, desc, auto_remind

async def make_meeting(parameters):
    name = "Undefined"
    if len(parameters) >= 1:
        for meet in meetings:
            if meet.getName() == parameters[0]:
                return "A meeting already uses that name!"
        name = parameters[0]
    else:
        return "No parameters given!"

    meeting_time, meeting_duration, meeting_date, participants, desc, auto_remind = await parse_meeting_info(parameters[1:])

    if meeting_time is None:
        meeting_time = datetime.datetime.now().time()
    if meeting_duration is None:
        meeting_duration = datetime.timedelta(hours=1)
    if meeting_date is None:
        meeting_date = datetime.date.today()
    if auto_remind is None:
        auto_remind = False

    meeting = schedule.Meeting(name, meeting_time, meeting_duration, meeting_date, participants, desc, auto_remind)
    meetings.append(meeting)

    for user in participants:
        addUserMeeting(user, meeting)

    return None

async def update_meeting(message, parameters):
    meeting_name = parameters[0]
    meeting = next((meet for meet in meetings if meet.getName() == meeting_name), None)

    if meeting is None:
        return "Meeting not found!"

    if len(parameters) < 2:
        return "No parameters given to update!"

    # Update meeting details
    param_updates = parameters[1:]
    meeting_time, meeting_duration, meeting_date, participants, desc, auto_remind = await parse_meeting_info(param_updates)

    if meeting_time:
        meeting.setTime(meeting_time)
    if meeting_duration:
        meeting.setDuration(meeting_duration)
    if meeting_date:
        meeting.setDate(meeting_date)
    if desc:
        meeting.setDesc(desc)
    if participants:
        meeting.setParticipants(participants)
    if auto_remind is not None:
        meeting.setAutoRemind(auto_remind)

    return "Meeting updated!"

async def delete_meeting(parameters):
    if len(parameters) == 0:
        return "No meeting name provided!"
    meeting_name = parameters[0]
    meeting = next((meet for meet in meetings if meet.getName() == meeting_name), None)
    if meeting:
        meetings.remove(meeting)
        return "Meeting deleted!"
    else:
        return "Meeting not found!"

@client.command()
async def meeting(ctx, *params):
    result = await make_meeting(params)
    if result:
        await ctx.send(result)
    else:
        await ctx.send("Meeting created!")

@client.command()
async def show_meetings(ctx):
    if not meetings:
        await ctx.send("No meetings scheduled.")
        return
    embed = discord.Embed(title="Scheduled Meetings", color=0x685BC7)
    for meeting in meetings:
        embed.add_field(name=meeting.getName(), value=f"Date: {meeting.getDateTime().strftime('%Y-%m-%d')}\nTime: {meeting.getDateTime().strftime('%H:%M')}\nDescription: {meeting.getDesc()}", inline=False)
    await ctx.send(embed=embed)

@client.command()
async def my_meetings(ctx):
    user = ctx.author
    if user.id not in users or not users[user.id]:
        await ctx.send("You have no meetings scheduled.")
        return
    embed = discord.Embed(title="Your Scheduled Meetings", color=0x685BC7)
    for meeting_name in users[user.id]:
        meeting = next((meet for meet in meetings if meet.getName() == meeting_name), None)
        if meeting:
            embed.add_field(name=meeting.getName(), value=f"Date: {meeting.getDateTime().strftime('%Y-%m-%d')}\nTime: {meeting.getDateTime().strftime('%H:%M')}\nDescription: {meeting.getDesc()}", inline=False)
    await ctx.send(embed=embed)

@client.command()
async def edit(ctx, *params):
    result = await update_meeting(ctx.message, params)
    if result:
        await ctx.send(result)
    else:
        await ctx.send("Meeting updated!")

@client.command()
async def delete_meeting(ctx, *params):
    result = await delete_meeting(params)
    if result:
        await ctx.send(result)
    else:
        await ctx.send("Meeting deletion failed!")

@client.command()
async def add_admin(ctx, meeting_name, user: discord.User):
    meeting = next((meet for meet in meetings if meet.getName() == meeting_name), None)
    if meeting:
        meeting.addAdmin(user)
        await ctx.send(f"Added {user} as an admin to the meeting {meeting_name}")
    else:
        await ctx.send("Meeting not found!")

@client.command()
async def remove_admin(ctx, meeting_name, user: discord.User):
    meeting = next((meet for meet in meetings if meet.getName() == meeting_name), None)
    if meeting:
        meeting.removeAdmin(user)
        await ctx.send(f"Removed {user} as an admin from the meeting {meeting_name}")
    else:
        await ctx.send("Meeting not found!")

@client.command()
async def missing(ctx):
    message = await ctx.send("Checking for missing participants...")
    await dm_missing(message)

@client.command()
async def help(ctx):
    await helpCommands(ctx.message)

client.run(os.getenv('DISCORD_TOKEN'))
