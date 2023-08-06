from typing import List

from lib.blocks.accessory import Accessory, Option


class Overflow(Accessory):
    def __init__(self, action_id, options: List[Option]):
        self.action_id = action_id
        self.options = options

    def json(self):
        return {
            'type': 'overflow',
            'options': [option.json() for option in self.options],
            'action_id': self.action_id
        }
