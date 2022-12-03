from random import choice
from typing import Union # Amazon must be fuming rn
from ratbot.consts import BALL_CHOICES

class Oracle:
    choices = BALL_CHOICES

    def pick(self) -> Union[str, bool]:
        try:
            ball_result = choice(self.choices)
            return ball_result
        except Exception:
            return False