from typing import Tuple

from domain.node import BaseNode
from domain.node import Node
from domain.node import TokenGeneratorNode
from domain.message_queue import MessageQueue
from shared.constants import QUEUE_MAX_SIZE
from shared.network import NETWORK_STRUCTURE


class NodeFactory:
  """Cria nodo da rede a partir do arquivo .cfg"""
  def __init__(self, config_file_path: str):
    self.config_file_path = config_file_path

  def __parse_config_file(self) -> Tuple[str, int, str, int, bool]:
    """lê config e retorna parâmetros para criação de um objeto Node"""
    with open(self.config_file_path, 'r') as f:
      lines = [line.strip() for line in f.readlines() if line.strip()]

    next_ip, next_port = lines[0].split(':')
    alias = lines[1]
    ip, port = NETWORK_STRUCTURE[alias]
    token_time = int(lines[2])
    is_gen = lines[3].lower() == 'true'

    return ip, int(port), next_ip, int(next_port), alias, token_time, is_gen


  def create_node(self) -> BaseNode:
    """cria objeto Node a partir do arquivo de config"""
    ip, port, next_ip, next_port, alias, token_time, is_gen = self.__parse_config_file()
    cls = TokenGeneratorNode if is_gen else Node
    return cls(ip, port, next_ip, next_port, alias, token_time, MessageQueue(QUEUE_MAX_SIZE))
