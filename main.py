import time
import sys
import threading
from logging import basicConfig, getLogger, INFO

from application.node_factory import NodeFactory
from application.ring_manager import RingManager
from infrastructure.udp_service import UDPService
from domain.node import BaseNode
from domain.packet import Packet

basicConfig(
  filename='token_ring.log',
  filemode='a',
  level= INFO,
  format='%(asctime)s %(levelname)s: %(message)s'
)

logger = getLogger(__name__)

def start_input_loop(node: BaseNode):
  def input_loop():
    print(f"[{node.alias}] Ready to send messages. Format: <dest>:<msg>")
    while True:
      try:
        raw = input()
        try:
          message = Packet.from_string(raw)
          logger.info(f"[{node}] Adding message ({message}) to queue")
          node.message_queue.push(message)
        except Exception as e:
          print("Invalid format. Use: 2000;<origin_alias>:<target_alias>:<error_control>:<CRC>:<message>")
          continue
      except Exception as e:
        print(f"Error sending message: {e}")
  threading.Thread(target=input_loop, daemon=True).start()

def run_node(config_file_path: str) -> None:
  node_factory = NodeFactory(config_file_path)
  node = node_factory.create_node()
  udp = UDPService(node.ip, node.port, logger)
  manager = RingManager(node, udp, logger)
  manager.start()
  start_input_loop(node)

  try:
    while True:
      time.sleep(1)
  except KeyboardInterrupt:
    manager.stop()
    udp.close()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python main.py <config_file>")
        sys.exit(1)

    run_node(sys.argv[1])
