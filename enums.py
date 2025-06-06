from enum import Enum


class Side(Enum):
  TOP = 'TOP'
  RIGHT = 'RIGHT'
  BOTTOM = 'BOTTOM'
  LEFT = 'LEFT'
  INLINE = 'INLINE'
  BLOCK = 'BLOCK'
  ALL = 'ALL'


class HAlignment:
  LEFT = 'LEFT'
  CENTER = 'CENTER'
  RIGHT = 'RIGHT'


class VAlignment:
  TOP = 'TOP'
  MIDDLE = 'MIDDLE'
  BOTTOM = 'BOTTOM'