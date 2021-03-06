from random import choice

import discord

client = discord.Client()

activity_type = discord.ActivityType.listening
activity_name = "squeaks"

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
    print('We have logged in as {0.user}'.format(client))
    print(f'Setting presence to {activity_name}')
    
    activity = discord.Activity(type=activity_type, name=activity_name)
    await client.change_presence(activity=activity)

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # Rat emoji function
    lower_case_message = message.content.lower()
    lower_case_message = ''.join(lower_case_message.split())
    
    if (("rat" in lower_case_message) or (client.user in message.mentions)):
        rat_message = lower_case_message
        rat_num = rat_message.count("rat")
        rat_num += rat_message.count("671793984435126277")      
        await message.channel.send(':rat: ' * rat_num)

    # Magic 8 Ball function
    if message.content.startswith("!oracle"):
        # Thanks @PlusReed this is much better
        try:
            ball_result = choice(ball_choices)
            await message.channel.send(
                "{0.author.mention} Squeek squeek! ({1})".format(message, ball_result))
        except:
            await message.channel.send(
                "Squeek squeek... (Something went wrong, make <@457637280539082763> fix it...")

client.run('TOKEN')
