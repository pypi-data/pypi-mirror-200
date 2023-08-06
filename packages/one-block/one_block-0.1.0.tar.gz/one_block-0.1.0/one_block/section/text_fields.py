from typing import List

from lib.blocks.base import Base


class TextFields(Base):
    def __init__(self, fields: List[Base]):
        self.fields = fields

    def json(self):
        return {
            'type': 'section',
            'fields': [
                field.json() for field in self.fields
            ]
        }
