import time
import threading

from domain.node import BaseNode
from domain.packet import Packet, Token
from infrastructure.udp_service import UDPService

class RingManager:
  def __init__(self, node: BaseNode, udp_service: UDPService):
    self.node = node
    self.udp_service = udp_service

  def log(self, msg):
    print(f"[{self.node}] {msg}")

  def start(self):
    self.log("Starting node...")
    listener = threading.Thread(target=self.listen, daemon=True)
    listener.start()

    if self.node.has_token:
      time.sleep(1)
      self.send_token()

  def listen(self):
    while self.node.is_running:
      try:
        msg = self.udp_service.receive()
        print("received message")
        packet = Packet.from_string(msg)
        if isinstance(packet, Token):
          self.receive_token()
      except TimeoutError:
        continue

  def send_token(self):
    self.log("Holding token...")
    time.sleep(self.node.token_time)
    self.log("Sending token to next node...")
    msg = repr(Token())
    self.udp_service.send(msg, self.node.next_node_ip, self.node.next_node_port)

  def receive_token(self):
    self.log("Received token.")
    self.send_token()

  def stop(self):
    self.node.is_running = False