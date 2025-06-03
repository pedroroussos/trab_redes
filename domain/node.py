from dataclasses import dataclass

from .message_queue import MessageQueue


@dataclass
class BaseNode:
  ip: str
  port: int
  next_node_ip: str
  next_node_port: int
  alias: str
  token_time: int
  message_queue: MessageQueue

  is_running: bool = True
  has_token: bool = False

  def parse_config_file(self):
    pass

  def send_packet(self):
    pass

  def __str__(self):
    return f'{self.alias}'

@dataclass
class Node(BaseNode):
  pass

@dataclass
class TokenGeneratorNode(BaseNode):
  def __post_init__(self):
    self.has_token = True

  def monitor_token(self):
    pass

  def generate_token(self):
    pass

  def remove_token(self):
    pass