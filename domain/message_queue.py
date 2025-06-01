from queue import Queue

from .packet import Message

class MessageQueue:
  def __init__(self, maxsize: int):
    self.queue = Queue(maxsize=maxsize)

  def push(self, item: Message):
    if not self.queue.full():
      self.queue.put(item)

  def pop(self) -> Message|None:
    if not self.queue.empty():
      return self.queue.get()
    return None
