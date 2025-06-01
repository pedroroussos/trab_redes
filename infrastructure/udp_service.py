import json
import socket

class UDPService():
  def __init__(self, host, port):
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    self.sock.bind((host, port))
    self.sock.settimeout(2)

  def send(self, message: str, ip: str, port: int):
    print(f"sending {message} to {ip}:{port}")
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