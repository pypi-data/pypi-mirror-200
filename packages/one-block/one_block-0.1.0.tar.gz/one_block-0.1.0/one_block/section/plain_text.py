from lib.blocks.base import Base, BasePlainText


class PlainText(Base):
    def __init__(self, text, emoji=True):
        self.base = BasePlainText(text, emoji)

    def json(self):
        return {
            'type': 'section',
            'text': self.base.json()
        }
