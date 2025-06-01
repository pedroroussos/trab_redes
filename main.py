import time
import sys

from application.node_factory import NodeFactory
from application.ring_manager import RingManager
from infrastructure.udp_service import UDPService

def run_node(config_file_path: str) -> None:
  node_factory = NodeFactory(config_file_path)
  node = node_factory.create_node()
  udp = UDPService(node.ip, node.port)
  manager = RingManager(node, udp)

  manager.start()

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
