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
      origin_nickname, target_nickname, error_control, crc, content = msg.split(';')[1].split(':')
      return Message(origin_nickname, target_nickname, ErrorControl(error_control), int(crc), content)
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
  origin_nickname: str
  target_nickname: str
  error_control: ErrorControl
  crc: int
  content: str

  def __post_init__(self):
    self.num_seq = NumSeq.Message

  def __repr__(self):
    return f"""{self.num_seq};{self.origin_nickname}:\
               {self.target_nickname}:{self.error_control}:\
               {self.crc}:{self.content}"""