import json
import socket
from logging import Logger


class UDPService():
  def __init__(self, host, port, logger: Logger):
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    self.sock.bind((host, port))
    self.sock.settimeout(2)
    self.logger = logger

  def send(self, message: str, ip: str, port: int):
    data = message.encode()
    self.sock.sendto(data, (ip, port))

  def receive(self) -> str:
    try:
      data, _ = self.sock.recvfrom(2048)
      return data.decode()
    except:
      raise TimeoutError

  def close(self):
    self.sock.close()