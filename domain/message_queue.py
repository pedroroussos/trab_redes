from collections import deque

from .packet import Message


class MessageQueue:
  """representa a fila de mensagens de um nodo"""
  def __init__(self, max_size: int):
    self.queue = deque()
    self.max_size = max_size

  def push(self, item: Message):
    if len(self.queue) < self.max_size:
      self.queue.append(item)

  def push_front(self, item: Message):
    if len(self.queue) < self.max_size:
      self.queue.appendleft(item)

  def pop(self):
    if self.queue:
      return self.queue.popleft()
    return None

  def is_empty(self):
    return not self.queue