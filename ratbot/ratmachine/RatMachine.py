from datetime import datetime
from os import getenv

class RatMachine:
    """Counts rats"""
    normal_rat = ":rat: "
    pride_rat = "<:priderat:981564427801358416> "
    pride_month = 6
    bot_id = getenv("BOT_ID")

    def __init__(self, message: str):
        self.__message = message
        self.__message_prep()

    def __message_prep(self):
        self.__message = self.__message.lower()
        self.__message = "".join(self.__message.split())

    def message_has_rat(self):
        return "rat" in self.__message

    @property
    def message(self):
        return self.__message

    @message.setter
    def message(self, value):
        self.__message = value
        self.__message_prep()
    
    @property
    def rat_count(self):
        rat_num = self.__message.count("rat")
        rat_num += self.__message.count(self.bot_id)

        return rat_num

    def make_rat_message(self):
        today = datetime.today()
        count = self.rat_count
        rat_to_use = self.normal_rat

        # use pride rat if month is 6
        if (today.month == self.pride_month):
            rat_to_use = self.pride_rat
        
        return rat_to_use * count

        
