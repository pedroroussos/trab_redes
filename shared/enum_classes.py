from enum import Enum

class BaseEnum(Enum):
  def __str__(self):
    return str(self.value)

class ErrorControl(BaseEnum):
  MNE = 'maquina_nao_existe'
  ACK = 'ACK'
  NAK = 'NAK'

class NumSeq(BaseEnum):
  Token = '1000'
  Message = '2000'
