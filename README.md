
# Aeon : the discord meet scheduler

Aeon is a discord meet scheduler bot which makes meet scheduling easy and fast 




## commands

```$help``` : prints all the inbuilt commands set up inside the bot  

```$meeting ```- allows you to schedule a new meeting

```$show_meetings``` - will show all currently scheduled my_meetings

```$my_meetings``` - sends you a direct message of all of your scheduled meetings

```$edit``` - lets meeting organizer/administrator(s) edit meeting details

```$delete_meeting``` - allows the meeting organizer/adminstrator(s) to delete a meeting given its name

```$add_admin``` - adds an administrator to the meeting given the meeting name and the @ of the new administrator (e.g. $add_admin test @john)

```$remove_admin``` - removes an administrator to the meeting given the meeting name and the @ of the old administrator (e.g. $remove_admin test @john)

```$missing``` - checks the sender's voice channel to see if all meeting attendees are present and sends a direct message to those who are missing
## Installation

1.Create a discord bot through https://discord.com/developers

2.Obtain the bot token and store it as ```.env```file


3.Download the github project file 

4.run ```pip install -U python-dotenv``` and ```pip install -U discord.py```

5.run ```aeonbot.py``` on your cmd locally
    
## Stack used
``python`` `discord.py`
## Limitation

our discord bot can schedule your meetings via personal messaging only...
The bot don't work while adding on to a server.We are working on the limitations and trying to change the bot application settings