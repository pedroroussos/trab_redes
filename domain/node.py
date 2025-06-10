from dataclasses import dataclass, field
import time
import threading

from .message_queue import MessageQueue
from shared.constants import TOKEN_TIMEOUT
from .packet import Token


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
  """representa um nodo comum"""
  pass

@dataclass
class TokenGeneratorNode(BaseNode):
  """representa um nodo gerador de tokens"""
  token_timeout: float = TOKEN_TIMEOUT
  token_arrival_times: list = field(default_factory=list)
  monitoring_thread: threading.Thread = field(init=False, default=None)
  has_token: bool = True

  def __post_init__(self):
    self.has_token = True

  def register_token_arrival(self):
    now = time.time()
    self.token_arrival_times.append(now)

    self.token_arrival_times = [
      t for t in self.token_arrival_times if now - t <= self.token_timeout
    ]

  def monitor_token(self, ring_manager):
    def _monitor():
      while self.is_running:
        time.sleep(self.token_timeout)

        now = time.time()
        recent_tokens = [
          t for t in self.token_arrival_times if now - t <= self.token_timeout
        ]

        if not recent_tokens:
          ring_manager.log("No token received recently. Generating a new token.")
          ring_manager.send_token()
        elif len(recent_tokens) > 1:
          ring_manager.log("Multiple tokens detected. Removing excess tokens.")
          self.remove_token()

    self.monitoring_thread = threading.Thread(target=_monitor, daemon=True)
    self.monitoring_thread.start()

  def generate_token(self):
      self.has_token = True  # For clarity, though the token will be sent immediately
      return Token()

  def remove_token(self):
      self.has_token = False