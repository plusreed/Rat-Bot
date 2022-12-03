from discord import Intents

INTENTS = Intents.default()

# We need message content, so set it to true.
INTENTS.message_content = True