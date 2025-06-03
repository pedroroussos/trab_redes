import time
import threading
from logging import getLogger, Logger
import zlib
import random

from domain.node import BaseNode, TokenGeneratorNode
from domain.packet import Packet, Token, Message
from infrastructure.udp_service import UDPService
from shared.enum_classes import ErrorControl
from shared.constants import FAILURE_PROB

class RingManager:
  def __init__(self, node: BaseNode, udp_service: UDPService, logger: Logger):
    self.node = node
    self.udp_service = udp_service
    self.logger = logger

  def log(self, message: str):
    self.logger.info(f"[{self.node.alias}] {message}")

  def start(self):
    self.log("Starting node...")
    self.node.is_running = True

    if self.node.has_token:
      self.log("This node will initiate the token.")
      self.send_token()

    threading.Thread(target=self.listen, daemon=True).start()

  def listen(self):
    while self.node.is_running:
      try:
        raw_msg = self.udp_service.receive()
        packet = Packet.from_string(raw_msg)

        if isinstance(packet, Token):
          self.handle_token()
        elif isinstance(packet, Message):
          self.handle_message(packet)
      except TimeoutError:
        continue

  def handle_token(self):
    self.log("Received token.")
    self.node.has_token = True

    message = self.node.message_queue.pop()
    if message is None:
      self.log("No messages to send. Passing token.")
      self.send_token()
    else:
      self.log("Sending next message in queue.")
      self.send_message(message)

  def handle_message(self, message: Message):
    if self.is_message_from_self(message):
      if message.is_broadcast:
        self.log("Broadcast message completed the ring. Dropping.")
      else:
        self.handle_message_return(message)
      self.send_token()

    elif message.is_broadcast or self.is_message_for_self(message):
      self.process_received_message(message)
      self.send_message(message)

    else:
      self.log(f"Message not for this node (target is {message.target_alias}). Forwarding.")
      self.send_message(message)

  def is_message_from_self(self, message: Message) -> bool:
    return message.origin_alias == self.node.alias

  def is_message_for_self(self, message: Message) -> bool:
    return message.target_alias == self.node.alias

  def handle_message_return(self, message: Message):
    self.log("Message returned to origin.")
    if message.error_control == ErrorControl.NAK:
      self.log("NAK received. Requeuing message.")
      message.error_control = ErrorControl.MNE
      self.node.message_queue.push_front(message)
    elif message.error_control == ErrorControl.ACK:
      self.log("ACK received. Message successfully delivered.")
    elif message.error_control == ErrorControl.MNE:
      self.log("Target node does not exist. Deleting message.")

  def process_received_message(self, message: Message):
    self.log("Processing message addressed to this node.")
    if message.is_broadcast:
      self.log("Received broadcast message.")
      return

    if random.random() < FAILURE_PROB:
      self.log("Simulating CRC corruption")
      calculated_crc = zlib.crc32((message.content + 'xxx').encode())
    else:
      calculated_crc = zlib.crc32(message.content.encode())

    if calculated_crc == message.crc:
      self.log("CRC check passed. Sending ACK.")
      message.error_control = ErrorControl.ACK
    else:
      self.log("CRC check failed. Sending NAK.")
      message.error_control = ErrorControl.NAK

  def send_token(self):
    self.sleep_token_time()
    self.log("Sending token to next node.")
    token = Token()
    self.udp_service.send(repr(token), self.node.next_node_ip, self.node.next_node_port)
    self.node.has_token = False

  def send_message(self, message: Message):
    self.sleep_token_time()
    self.log(f"Forwarding message ({repr(message)}).")
    self.udp_service.send(repr(message), self.node.next_node_ip, self.node.next_node_port)

  def sleep_token_time(self):
    self.log(f"Sleeping for {self.node.token_time} seconds.")
    time.sleep(self.node.token_time)

  def stop(self):
    self.log("Node stopped.")
    self.node.is_running = False