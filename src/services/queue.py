from .abc import QueueABC


class QueueService(QueueABC):
    def push(self, element):
        ...
