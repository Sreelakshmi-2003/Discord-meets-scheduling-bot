AEON
# Discord Meeting Bot

## Description

This Discord bot manages meetings on your server. It allows users to schedule meetings, track participants, and send reminders. It also provides functionality for admins to manage meetings and users.

## Features

- *Meeting Management*: Schedule, edit, and delete meetings.
- *User Management*: Add or remove users from meetings, set reminders.
- *Admin Management*: Assign and remove administrators for meetings.
- *Meeting Notifications*: Send notifications to users who are missing from meetings.
- *Help Command*: List available commands and their usage.

## Requirements

- Python 3.8 or higher
- discord.py library
- python-dotenv for environment variable management
- schedule library for scheduling tasks

## Installation

1. *Clone the repository:*

   bash
   git clone <https://github.com/Sreelakshmi-2003/Discord-meets-scheduling-bot/tree/main>
   cd <Discord-meets-scheduling-bot>
   

2. *Install the required libraries:*

   bash
   pip install -r requirements.txt
   

3. **Create a .env file in the root directory and add your Discord bot token:**

   dotenv
   DISCORD_TOKEN=<your-discord-bot-token>
   


## Usage

1. *Run the bot:*

   bash
   python bot.py
   

2. *Commands:*

   - **$hello**: The bot responds with "Hello!".
   - **$goodbye**: The bot responds with a farewell message.
   - **$meeting <name> [start_time] [duration] [date] [participants] [description] [auto_remind]**: Schedules a new meeting.
   - **$show_meetings**: Shows all scheduled meetings.
   - **$my_meetings**: Sends a DM with the user's scheduled meetings.
   - **$edit <meeting_name> [parameters]**: Edits the details of an existing meeting.
   - **$delete_meeting <meeting_name>**: Deletes a meeting.
   - **$missing**: Checks the user's voice channel for missing meeting participants and sends notifications.
   - **$add_admin <meeting_name> <user>**: Adds an admin to the meeting.
   - **$remove_admin <meeting_name> <user>**: Removes an admin from the meeting.
   - **$leave_meeting <meeting_name>**: Allows a user to leave a meeting.
   - **$help**: Lists all available commands.

## Development

- **on_ready**: Initializes the bot and sets its username and avatar.
- **on_member_join**: Sends a welcome message when a new member joins the server.
- **on_member_remove**: Sends a farewell message when a member leaves the server.
- **on_reaction_add**: Handles user reactions to join meetings.
- **on_guild_join**: Sends a greeting message when the bot joins a new guild.


---
