import logging
import logging.handlers
from os import getenv
import discord
from dotenv import load_dotenv
from ratbot.consts.intents import INTENTS
from ratbot.client import RatBotClient

# Load from .env
load_dotenv()

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
logging.getLogger('discord.http').setLevel(logging.INFO)

handler = logging.handlers.RotatingFileHandler(
    filename = "rat_bot.log",
    encoding = "utf-8",
    maxBytes = 32 * 1024 * 1024,
    backupCount = 5
)
date_format = "%m/%d/%Y %H:%M:%S"
formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', date_format, style='{')
handler.setFormatter(formatter)
logger.addHandler(handler)

client = RatBotClient(intents = INTENTS)
client.run(getenv("TOKEN"), log_handler = handler)