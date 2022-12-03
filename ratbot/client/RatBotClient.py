from os import getenv
from discord import Client
from ratbot.consts import PRESENCE
from ratbot.oracle import Oracle
from ratbot.ratmachine import RatMachine

class RatBotClient(Client):
    admin_id = getenv("ADMIN_ID")
    bot_id = getenv("BOT_ID")
    rat_machine = RatMachine(message = "")
    oracle = Oracle()

    async def on_ready(self):
        print(f"We have logged in as {self.user}")
        print(f"Setting presence")
        await self.__set_presence()

    async def on_message(self, message):
        if message.author == self.user:
            return # don't respond to self
        
        # set up rat_machine with new message
        self.rat_machine.message = message.content

        if (self.rat_machine.message_has_rat() or self.user in message.mentions):
            rat_message = self.rat_machine.make_rat_message()

            await message.channel.send(rat_message)

        if (message.content.startswith("!oracle")):
            # use the oracle class to get something
            response = self.oracle.pick()

            if (type(response) is bool and response is False):
                # whoops!
                await message.channel.send(
                    "Squeek squeek...",
                    f"(Something went wrong, make {self.admin_id} fix it...)",
                    mention_author = True,
                    reference = message
                )
            else:
                await message.channel.send(
                    f"Squeek squeek! ({response})",
                    mention_author = True,
                    reference = message
                )
        

    async def __set_presence(self):
        await self.change_presence(
            activity = PRESENCE
        )
