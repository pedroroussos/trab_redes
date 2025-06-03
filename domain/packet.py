from dataclasses import dataclass
from shared.enum_classes import ErrorControl
from shared.enum_classes import NumSeq

@dataclass
class Packet:
  pass

  @staticmethod
  def from_string(msg: str) -> 'Packet':
    packet_id = msg.split(';')[0]

    if packet_id == NumSeq.Token.value:
      return Token()
    elif packet_id == NumSeq.Message.value:
      origin_alias, target_alias, error_control, crc, content = msg.split(';')[1].split(':')
      return Message(origin_alias, target_alias, ErrorControl(error_control), int(crc), content)
    else:
      raise ValueError(f'invalid message: {msg}')


@dataclass
class Token(Packet):
  pass

  def __post_init__(self):
    self.num_seq = NumSeq.Token

  def __repr__(self):
    return f'{self.num_seq}'


@dataclass
class Message(Packet):
  origin_alias: str
  target_alias: str
  error_control: ErrorControl
  crc: int
  content: str

  is_broadcast: bool = False

  def __post_init__(self):
    self.num_seq = NumSeq.Message
    self.is_broadcast = self.target_alias == 'TODOS'

  def __repr__(self):
    return f"""{self.num_seq};{self.origin_alias}:{self.target_alias}:{self.error_control}:{self.crc}:{self.content}"""