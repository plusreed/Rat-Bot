from os import getenv
from random import choice

import discord
from dotenv import load_dotenv

# Load from .env
load_dotenv()

from database import Database

# Initialize the database
db = Database(getenv("DB_NAME"))

client = discord.Client()

# Initialize the bot's activity status
activity_type = discord.ActivityType.listening
activity_name = "squeaks"
activity = discord.Activity(type=activity_type, name=activity_name)

admin_id = getenv("ADMIN_ID")  # User ID for admin user
bot_id = getenv("BOT_ID")  # User ID for the bot

ball_choices = (
    "It is certain.",
    "It is decidedly so.",
    "Without a doubt.",
    "Yes - definitely.",
    "You may rely on it.",
    "As I see it, yes.",
    "Most likely.",
    "Outlook good.",
    "Yes.",
    "Signs point to yes.",
    "Reply hazy, try again.",
    "Ask again later.",
    "Better not tell you now.",
    "Cannot predict now.",
    "Concentrate and ask again.",
    "Don't count on it.",
    "My reply is no.",
    "My sources say no.",
    "Outlook not so good.",
    "Very doubtful."
)


# Define events
@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")
    print(f"Setting presence to {activity_name}")
    await client.change_presence(activity=activity)


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # Rat emoji function
    lower_case_message = message.content.lower()
    lower_case_message = "".join(lower_case_message.split())

    if (("rat" in lower_case_message) or (client.user in message.mentions)):
        rat_message = lower_case_message
        rat_num = rat_message.count("rat")
        rat_num += rat_message.count(bot_id)
        if message.created_at.strftime("%m") == "06":  # Pride month!
            emote = "<:priderat:981564427801358416> "
        else:  # No special occasion, send the regular rat
            emote = ":rat: "  # This is a base emoji so we don't need the ID
        
        # insert rat count into database
        db.upsert_rat_count(message.author.id, message.guild.id, rat_num)

        await message.channel.send(emote * rat_num)

    # Magic 8 Ball function
    if message.content.startswith("!oracle"):
        # Thanks @PlusReed this is much better
        try:
            ball_result = choice(ball_choices)
            await message.channel.send(
                f"Squeek squeek! ({ball_result})",
                mention_author=True,  # Mention the user
                reference=message  # Set message_reference to the message.
            )
        except Exception:
            await message.channel.send(
                "Squeek squeek... "
                f"(Something went wrong, make {admin_id} fix it...)",
                mention_author=True,
                reference=message
            )
    
    # Rat count function
    if message.content.startswith("!ratcount"):
        # split the message into words
        words = message.content.split()
        # if the message is just !ratcount, get the total rat count
        if len(words) == 1:
            rat_count = db.get_aggregate_rat_count()
            await message.channel.send(f"There are {rat_count} total rats.", mention_author=True, reference=message)
        
        # if the message is !ratcount @user, get the rat count for that user
        elif len(words) == 2:
            user_id = words[1].replace("<", "").replace(">", "").replace("@", "").replace("!", "")
            rat_count = db.get_rat_count_for_user(user_id, message.guild.id)
            await message.channel.send(f"That user has {rat_count} rats in this server.", mention_author=True, reference=message)
        
        # if the message is !ratcount server, get the total rat count for the server
        elif len(words) == 2 and words[1] == "server":
            rat_count = db.get_aggregate_rat_count_by_server(message.guild.id)
            await message.channel.send(f"There are {rat_count} total rats in this server.", mention_author=True, reference=message)
        
        else:
            await message.channel.send("Invalid command. Usage: !ratcount, !ratcount @user, or !ratcount server", mention_author=True, reference=message)
        
        #rat_count = db.get_rat_count_for_user(message.author.id, message.guild.id)
        #await message.channel.send(f"You have {rat_count} rats in this server.", mention_author=True, reference=message)

client.run(getenv("TOKEN"))
