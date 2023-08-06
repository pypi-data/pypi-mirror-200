from lib.blocks.base import Base


class Divider(Base):
    def json(self):
        return {
            'type': 'divider'
        }
