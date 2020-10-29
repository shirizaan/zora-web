from enum import IntEnum
from typing import Dict, List
import math
import random
from .constants import RoomAction
from .direction import Direction
from .enemy import Enemy


class RoomType(IntEnum):
  NO_ROOM_TYPE = -0x01
  PLAIN_ROOM = 0x00
  SPIKE_TRAP_ROOM = 0x01
  FOUR_SHORT_ROOM = 0x02
  FOUR_TALL_ROOM = 0x03
  AQUAMENTUS_ROOM = 0x04
  GLEEOK_ROOM = 0x05
  GOHMA_ROOM = 0x06
  HORIZONTAL_LINES = 0x07
  REVERSE_C = 0x08
  CIRCLE_BLOCK_WALL_ROOM = 0x09
  DOUBLE_BLOCK = 0x0A
  SECOND_QUEST_T_LIKE_ROOM = 0x0B
  MAZE_ROOM = 0x0C
  GRID_ROOM = 0x0D
  VERTICAL_CHUTE_ROOM = 0x0E
  HORIZONTAL_CHUTE_ROOM = 0x0F
  VERTICAL_LINES = 0x10
  ZIGZAG_ROOM = 0x11
  T_ROOM = 0x12
  VERTICAL_MOAT_ROOM = 0x13
  CIRCLE_MOAT_ROOM = 0x14
  POINTLESS_MOAT_ROOM = 0x15
  CHEVY_ROOM = 0x16
  NSU = 0x17
  HORIZONTAL_MOAT_ROOM = 0x18
  DOUBLE_MOAT_ROOM = 0x19
  DIAMOND_STAIR_ROOM = 0x1A
  NARROW_STAIR_ROOM = 0x1B
  SPIRAL_STAIR_ROOM = 0x1C
  DOUBLE_SIX_BLOCK_ROOM = 0x1D
  SINGLE_SIX_BLOCK_ROOM = 0x1E
  FIVE_PAIR_ROOM = 0x1F
  TURNSTILE_ROOM = 0x20
  ENTRANCE_ROOM = 0x21
  SINGLE_BLOCK_ROOM = 0x22
  TWO_BEAMOS_ROOM = 0x23
  FOUR_BEAMOS_ROOM = 0x24
  EMPTY_DOTTED_ROOM = 0x25
  BLACK_ROOM = 0x26
  KIDNAPPED_ROOM = 0x27
  BEAST_ROOM = 0x28
  TRIFORCE_ROOM = 0x29
  TRANSPORT_STAIRCASE = 0x3E
  ITEM_STAIRCASE = 0x3F

  ## Deprecated, don't use
  ELDER_PLACEHOLDER_ROOM_TYPE = 0x31
  HUNGRY_ENEMY_PLACEHOLDER_ROOM_TYPE = 0x32
  TRIFORCE_CHECK_PLACEHOLDER_ROOM_TYPE = 0x33

  def ShortNameMap(self) -> Dict["RoomType", str]:
    return {
        RoomType.PLAIN_ROOM: "Empty Room",
        RoomType.TRIFORCE_ROOM: "TriforceRm",
        RoomType.ENTRANCE_ROOM: "EntranceRm",
        RoomType.HORIZONTAL_MOAT_ROOM: "HorzMoat"
    }

  def GetShortName(self) -> str:
    #assert self in self.SHORT_NAMES
    try:
      return self.ShortNameMap()[self]
    except KeyError:
      return self.name[0:8]

  def AllowsDoorToDoorMovement(self, from_direction: Direction, to_direction: Direction,
                               has_ladder: bool) -> bool:
    # This room is a bit of an edge case so we handle it with custom logic.
    if self == RoomType.SECOND_QUEST_T_LIKE_ROOM:
      if (from_direction in [Direction.NORTH, Direction.EAST] and
          to_direction in [Direction.NORTH, Direction.EAST]):
        return True
      if (from_direction in [Direction.SOUTH, Direction.WEST] and
          to_direction in [Direction.SOUTH, Direction.WEST] and has_ladder):
        return True
      return False

    if self.HasWater() and not has_ladder:
      valid_directions = VALID_TRAVEL_DIRECTIONS_IN_WATER_ROOMS[self]
      if from_direction not in valid_directions or to_direction not in valid_directions:
        return False

    if self.HasMovementConstraints():
      valid_directions = VALID_TRAVEL_DIRECTIONS_IN_MOVEMENT_RESTRICTED_ROOMS[self]
      if from_direction not in valid_directions or to_direction not in valid_directions:
        return False
    return True

  def HasWater(self) -> bool:
    return self in VALID_TRAVEL_DIRECTIONS_IN_WATER_ROOMS.keys()

  def HasMovementConstraints(self) -> bool:
    return self in VALID_TRAVEL_DIRECTIONS_IN_MOVEMENT_RESTRICTED_ROOMS.keys() or self in [
        RoomType.TURNSTILE_ROOM, RoomType.KIDNAPPED_ROOM
    ]

  def HasOpenStairs(self) -> bool:
    return self in [
        RoomType.DIAMOND_STAIR_ROOM, RoomType.NARROW_STAIR_ROOM, RoomType.SPIRAL_STAIR_ROOM
    ]

  def HasUnobstructedStairs(self) -> bool:
    return self in [RoomType.NARROW_STAIR_ROOM, RoomType.SPIRAL_STAIR_ROOM]

  def CanHavePushBlock(self) -> bool:
    return self in [
        RoomType.HORIZONTAL_LINES, RoomType.VERTICAL_LINES, RoomType.SPIKE_TRAP_ROOM,
        RoomType.REVERSE_C, RoomType.DOUBLE_BLOCK, RoomType.MAZE_ROOM, RoomType.GRID_ROOM,
        RoomType.ZIGZAG_ROOM, RoomType.DIAMOND_STAIR_ROOM, RoomType.FIVE_PAIR_ROOM,
        RoomType.SINGLE_BLOCK_ROOM, RoomType.TURNSTILE_ROOM
    ]

  def CanHaveStairs(self) -> bool:
    return self in [
        #RoomType.CIRCLE_BLOCK_WALL_ROOM,
        RoomType.DIAMOND_STAIR_ROOM,
        RoomType.DOUBLE_BLOCK,
        RoomType.FIVE_PAIR_ROOM,
        RoomType.GOHMA_ROOM,
        RoomType.GRID_ROOM,
        RoomType.HORIZONTAL_LINES,
        RoomType.MAZE_ROOM,
        RoomType.NARROW_STAIR_ROOM,
        RoomType.REVERSE_C,
        RoomType.SINGLE_BLOCK_ROOM,
        RoomType.SPIKE_TRAP_ROOM,
        RoomType.SPIRAL_STAIR_ROOM,
        RoomType.VERTICAL_LINES,
        RoomType.ZIGZAG_ROOM
    ]

  def NeedsOffCenterStairReturnPosition(self) -> bool:
    return self in [
        RoomType.CIRCLE_BLOCK_WALL_ROOM, RoomType.DIAMOND_STAIR_ROOM, RoomType.FIVE_PAIR_ROOM,
        RoomType.HORIZONTAL_LINES, RoomType.SINGLE_BLOCK_ROOM, RoomType.SPIRAL_STAIR_ROOM,
        RoomType.VERTICAL_LINES
    ]

  def IsBadForBosses(self) -> bool:
    return self.value in [
        RoomType.HORIZONTAL_LINES, RoomType.CIRCLE_BLOCK_WALL_ROOM,
        RoomType.SECOND_QUEST_T_LIKE_ROOM, RoomType.MAZE_ROOM, RoomType.GRID_ROOM,
        RoomType.VERTICAL_CHUTE_ROOM, RoomType.HORIZONTAL_CHUTE_ROOM, RoomType.VERTICAL_LINES,
        RoomType.ZIGZAG_ROOM, RoomType.T_ROOM, RoomType.CHEVY_ROOM, RoomType.NSU,
        RoomType.SPIRAL_STAIR_ROOM, RoomType.SINGLE_SIX_BLOCK_ROOM, RoomType.DOUBLE_SIX_BLOCK_ROOM,
        RoomType.TURNSTILE_ROOM, RoomType.ENTRANCE_ROOM, RoomType.KIDNAPPED_ROOM,
        RoomType.TRIFORCE_ROOM, RoomType.DIAMOND_STAIR_ROOM
    ]

  def IsBadForTraps(self) -> bool:
    return self.value in [
        RoomType.HORIZONTAL_LINES, RoomType.VERTICAL_LINES, RoomType.REVERSE_C,
        RoomType.SECOND_QUEST_T_LIKE_ROOM, RoomType.T_ROOM, RoomType.SPIRAL_STAIR_ROOM,
        RoomType.TRIFORCE_ROOM, RoomType.ENTRANCE_ROOM, RoomType.POINTLESS_MOAT_ROOM,
        RoomType.CIRCLE_MOAT_ROOM
    ]

  def IsBadForPatra(self) -> bool:
    return self.value in [
        RoomType.HORIZONTAL_LINES, RoomType.REVERSE_C, RoomType.CIRCLE_BLOCK_WALL_ROOM,
        RoomType.SECOND_QUEST_T_LIKE_ROOM, RoomType.MAZE_ROOM, RoomType.VERTICAL_CHUTE_ROOM,
        RoomType.HORIZONTAL_CHUTE_ROOM, RoomType.VERTICAL_LINES, RoomType.T_ROOM,
        RoomType.CIRCLE_MOAT_ROOM, RoomType.POINTLESS_MOAT_ROOM, RoomType.CHEVY_ROOM, RoomType.NSU,
        RoomType.SPIRAL_STAIR_ROOM, RoomType.KIDNAPPED_ROOM, RoomType.TRIFORCE_ROOM
    ]

  def IsBadForLanmola(self) -> bool:
    return self.value in [
        RoomType.CIRCLE_BLOCK_WALL_ROOM, RoomType.DOUBLE_MOAT_ROOM, RoomType.SPIKE_TRAP_ROOM,
        RoomType.REVERSE_C, RoomType.AQUAMENTUS_ROOM, RoomType.DIAMOND_STAIR_ROOM,
        RoomType.VERTICAL_CHUTE_ROOM, RoomType.HORIZONTAL_CHUTE_ROOM, RoomType.HORIZONTAL_LINES,
        RoomType.NARROW_STAIR_ROOM, RoomType.SPIRAL_STAIR_ROOM, RoomType.T_ROOM,
        RoomType.VERTICAL_LINES, RoomType.MAZE_ROOM, RoomType.GRID_ROOM,
        RoomType.SECOND_QUEST_T_LIKE_ROOM, RoomType.TRIFORCE_ROOM, RoomType.TURNSTILE_ROOM,
        RoomType.ENTRANCE_ROOM, RoomType.CHEVY_ROOM, RoomType.NSU, RoomType.POINTLESS_MOAT_ROOM
    ]

  def IsPartitionedByBlockWalls(self) -> bool:
    return self.value in [
        #RoomType.VERTICAL_CHUTE_ROOM,RoomType.HORIZONTAL_CHUTE_ROOM,
        RoomType.CIRCLE_BLOCK_WALL_ROOM
    ]

  def IsHardToPlace(self) -> bool:
    return self.value in [
        RoomType.CIRCLE_BLOCK_WALL_ROOM, RoomType.VERTICAL_CHUTE_ROOM,
        RoomType.HORIZONTAL_CHUTE_ROOM, RoomType.TURNSTILE_ROOM, RoomType.T_ROOM,
        RoomType.SECOND_QUEST_T_LIKE_ROOM
    ]

  def GetRoomActionIfHasStairs(self) -> RoomAction:
    assert self.CanHaveStairs()
    if self == RoomType.DIAMOND_STAIR_ROOM:
      return RoomAction.PUSHABLE_BLOCK_OPENS_SHUTTER_DOORS
    elif self in [RoomType.NARROW_STAIR_ROOM, RoomType.SPIRAL_STAIR_ROOM]:
      return RoomAction.NO_ROOM_ACTION
    return RoomAction.PUSHABLE_BLOCK_MAKES_STAIRS_APPEAR

  def HasBeamoses(self) -> bool:
    return self.value in [RoomType.TWO_BEAMOS_ROOM, RoomType.FOUR_BEAMOS_ROOM]

  @classmethod
  def RandomValueOkayForStairs(cls, narrow_stair_room_okay: bool = False) -> "RoomType":
    while True:
      try:
        room_type = cls(random.randrange(0x0, 0x29))
      except ValueError:
        continue
      if room_type == RoomType.NARROW_STAIR_ROOM and not narrow_stair_room_okay:
        continue
      if room_type.CanHaveStairs():
        return room_type

  @classmethod
  def RandomValue(cls,
                  allow_hard_to_place: bool = True,
                  okay_for_enemy: Enemy = Enemy.NO_ENEMY) -> "RoomType":
    while True:
      try:
        room_type = cls(random.randrange(0x0, 0x29))
      except ValueError:
        continue
      enemy = okay_for_enemy
      if (enemy.IsBoss() or enemy == Enemy.RUPEE_BOSS) and room_type.IsBadForBosses():
        continue
      if room_type.HasWater() or room_type.HasMovementConstraints():
        continue

      if room_type.HasOpenStairs():
        continue
      if room_type in [
          RoomType.KIDNAPPED_ROOM, RoomType.TURNSTILE_ROOM, RoomType.ENTRANCE_ROOM,
          RoomType.BEAST_ROOM
      ]:
        continue
      if not allow_hard_to_place and room_type.IsHardToPlace():
        continue
      if room_type.IsBadForLanmola() and okay_for_enemy in [Enemy.RED_LANMOLA, Enemy.BLUE_LANMOLA]:
        continue
#      if room_type.HasBeamoses() and random.choice([True, False]):
#        continue
      if room_type.HasWater() and random.choice([True, True, True, False]):
        continue
      if room_type.IsBadForTraps() and random.choice([True, False]):
        continue
#      if room_type.IsBadForBosses() and random.choice([True, True, False]):
#        continue
      if room_type.IsBadForTraps() and okay_for_enemy.HasTraps():
        continue
      return room_type

  @classmethod
  def GetValidPositionForRoomType(cls,
                                  room_type_1: "RoomType",
                                  is_item_position: bool = False) -> int:
    return cls.GetValidPositionForRoomTypes(room_type_1, RoomType.NO_ROOM_TYPE, is_item_position)

  @classmethod
  def GetValidPositionForRoomTypes(cls,
                                   room_type_1: "RoomType",
                                   room_type_2: "RoomType",
                                   is_item_position: bool = False) -> int:
    #    x_offset = 2
    #    y_offset = 6 if is_item_position else 5
    while True:
      #      position_code = (0x10 * random.randint(x_offset + 0, x_offset + 11) +
      #                       random.randint(y_offset + 0, y_offset + 6))
      position_code = random.randint(0x20, 0xDC)
      if not cls.IsValidPositionForRoomType(position_code, room_type_1, is_item_position):
        continue
      if (room_type_2 is not RoomType.NO_ROOM_TYPE and
          not cls.IsValidPositionForRoomType(position_code, room_type_2, is_item_position)):
        continue
      return position_code

  @classmethod
  def IsValidPositionForRoomType(cls,
                                 position_code: int,
                                 room_type: "RoomType",
                                 is_item_position: bool = False) -> bool:
    #    return room_type.IsValidItemPosition(position_code)
    #
    #  def IsValidItemPosition(self, position_code: int, is_item_position : bool) -> bool:
    x_code = math.floor(position_code / 0x10)
    y_code = position_code % 0x10

    col = x_code - 2
    row = y_code - (6 if is_item_position else 5)

    # Technically 0x02 is an okay x_code but since we want to ensure the spot to the left is also
    # free for items that have repeated sprites (like the ladder and triforce)
    if col not in range(12):  # (2-D are valid values)
      return False
    if row not in range(7):  # (5-B are valid values)
      return False
    #if self == RoomType.ITEM_STAIRCASE:
    #  return (y_code == 0xA and x_code in range(0x7, 0xE)) or y_code == 0x0D
    # Don't allow item positions that are right in front of doorways
    if col in [5, 6] and row in [0, 6]:
      return False
    if col in [0, 1, 10, 11] and row == 3:
      return False
    if col in [0, 11] and row in [0, 6]:
      return False

    return ROOM_DATA[room_type.value][row][col] in [0, 5]


# Shoutouts to Imasock for creating this!

# normal tiles are 0
# blocks are 1
# water is 2
# statues are 3
# stairs are 4
# black tiles are 5

# yapf: disable

ROOM_DATA = [
 [ #plain
  [0,0,0,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,0,0,0,0]
 ],
 [ #spike_trap
  [0,0,0,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,0,0,0,0],
  [0,0,1,0,0,0,0,0,0,1,0,0],
  [0,1,0,0,0,0,0,0,0,0,1,0],
  [0,0,1,0,0,0,0,0,0,1,0,0],
  [0,0,0,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,0,0,0,0]
 ],
 [ #four_short
  [0,0,0,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,0,0,0,0],
  [0,0,1,0,0,0,0,0,0,1,0,0],
  [0,0,0,0,0,0,0,0,0,0,0,0],
  [0,0,1,0,0,0,0,0,0,1,0,0],
  [0,0,0,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,0,0,0,0]
 ],
 [ #four_tall
  [0,0,0,0,0,0,0,0,0,0,0,0],
  [0,0,1,0,0,0,0,0,0,1,0,0],
  [0,0,0,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,0,0,0,0],
  [0,0,1,0,0,0,0,0,0,1,0,0],
  [0,0,0,0,0,0,0,0,0,0,0,0]
 ],
 [ #aquamentus
  [0,0,0,0,0,0,0,1,1,1,1,1],
  [0,0,0,0,0,0,0,0,0,1,1,1],
  [0,0,0,0,0,0,0,0,0,0,1,1],
  [0,0,0,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,0,0,1,1],
  [0,0,0,0,0,0,0,0,0,1,1,1],
  [0,0,0,0,0,0,0,1,1,1,1,1]
 ],
 [ #gleeok
  [1,1,1,1,1,0,0,1,1,1,1,1],
  [1,1,1,1,0,0,0,0,1,1,1,1],
  [1,1,0,0,0,0,0,0,0,0,1,1],
  [0,0,0,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,0,0,0,0],
  [0,0,1,0,0,0,0,0,0,1,0,0],
  [0,0,0,0,0,0,0,0,0,0,0,0]
 ],
 [ #IsBadForPatra
  [0,0,0,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,0,0,0,0],
  [0,1,0,0,0,0,0,0,0,0,1,0],
  [0,0,0,0,0,0,0,0,0,0,0,0],
  [0,0,0,1,0,0,0,0,1,0,0,0],
  [3,0,0,0,0,0,0,0,0,0,0,3]
 ],
 [# three_rows
  [0,0,0,0,0,0,0,0,0,0,0,0],
  [0,1,1,1,1,1,1,1,1,1,1,0],
  [0,0,0,0,0,0,0,0,0,0,0,0],
  [0,1,1,1,1,1,1,1,1,1,1,0],
  [0,0,0,0,0,0,0,0,0,0,0,0],
  [0,1,1,1,1,1,1,1,1,1,1,0],
  [0,0,0,0,0,0,0,0,0,0,0,0]
 ],
 [ #reverse_c
  [0,0,0,0,0,0,0,0,0,0,0,0],
  [0,1,1,1,1,1,1,1,1,1,1,0],
  [0,0,0,0,0,0,0,0,0,0,1,0],
  [0,0,0,0,0,0,0,0,0,0,1,0],
  [0,0,0,0,0,0,0,0,0,0,1,0],
  [0,1,1,1,1,1,1,1,1,1,1,0],
  [0,0,0,0,0,0,0,0,0,0,0,0]
 ],
 [ #circle_wall
  [0,0,0,0,0,0,0,0,0,0,0,0],
  [0,0,1,1,1,1,1,1,1,1,0,0],
  [0,0,1,9,9,9,9,9,9,1,0,0],
  [0,0,1,9,9,9,9,9,9,1,0,0],
  [0,0,1,9,9,9,9,9,9,1,0,0],
  [0,0,1,1,1,1,1,1,1,1,0,0],
  [0,0,0,0,0,0,0,0,0,0,0,0]
 ],
 [ #double_block
  [0,0,0,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,1,0,0,1,0,0,0,0],
  [0,0,0,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,0,0,0,0]
 ],
 [ # 2Q T-like room
  [0,2,2,0,0,0,0,0,0,0,0,0],
  [0,2,2,2,2,2,2,2,2,2,2,0],
  [0,2,2,2,2,2,2,2,2,2,2,0],
  [0,2,0,0,0,0,0,0,0,2,2,0],
  [0,2,2,0,0,0,0,0,0,2,2,0],
  [0,2,2,0,0,0,0,0,0,2,2,0],
  [0,2,2,0,0,0,0,0,0,2,2,0]
 ],
 [ #maze
  [0,1,0,1,0,0,0,0,0,0,0,0],
  [0,1,0,1,1,1,0,1,1,1,0,0],
  [0,1,0,0,0,1,0,0,0,1,1,1],
  [0,1,0,1,0,1,0,0,0,1,0,0],
  [0,1,1,1,0,1,0,0,0,1,0,0],
  [0,0,0,0,0,1,0,1,0,1,0,1],
  [0,0,1,0,0,0,0,1,0,0,0,1]
 ],
 [ #grid
  [0,0,0,0,0,0,0,0,0,0,0,0],
  [0,1,0,1,0,1,1,0,1,0,1,0],
  [0,0,0,0,0,0,0,0,0,0,0,0],
  [0,1,0,1,0,1,1,0,1,0,1,0],
  [0,0,0,0,0,0,0,0,0,0,0,0],
  [0,1,0,1,0,1,1,0,1,0,1,0],
  [0,0,0,0,0,0,0,0,0,0,0,0]
 ],
 [ #vert_chute
  [0,0,0,0,1,0,0,1,0,0,0,0],
  [0,0,0,0,1,0,0,1,0,0,0,0],
  [0,0,0,0,1,0,0,1,0,0,0,0],
  [0,0,0,0,1,0,0,1,0,0,0,0],
  [0,0,0,0,1,0,0,1,0,0,0,0],
  [0,0,0,0,1,0,0,1,0,0,0,0],
  [0,0,0,0,1,0,0,1,0,0,0,0]
 ],
 [ #horiz_chute
  [0,0,0,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,0,0,0,0],
  [1,1,1,1,1,1,1,1,1,1,1,1],
  [0,0,0,0,0,0,0,0,0,0,0,0],
  [1,1,1,1,1,1,1,1,1,1,1,1],
  [0,0,0,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,0,0,0,0]
 ],
 [ # Vertical lines
  [0,0,0,0,0,0,0,0,0,0,0,0],
  [0,1,0,1,0,1,1,0,1,0,1,0],
  [0,1,0,1,0,1,1,0,1,0,1,0],
  [0,1,0,1,0,1,1,0,1,0,1,0],
  [0,1,0,1,0,1,1,0,1,0,1,0],
  [0,1,0,1,0,1,1,0,1,0,1,0],
  [0,0,0,0,0,0,0,0,0,0,0,0]
 ],
 [ #zigzag
  [0,0,1,0,0,0,0,0,0,0,0,1],
  [0,1,0,0,0,1,0,0,0,0,1,0],
  [0,0,0,0,1,0,0,0,0,1,0,0],
  [0,0,0,1,0,0,0,0,1,0,0,0],
  [0,0,1,0,0,0,0,1,0,0,0,0],
  [0,1,0,0,0,0,1,0,0,0,1,0],
  [1,0,0,0,0,0,0,0,0,1,0,0]
 ],
 [ #t_room
  [0,0,0,0,0,0,0,0,0,0,0,0],
  [0,2,2,2,2,2,2,2,2,2,2,0],
  [0,2,2,2,2,2,2,2,2,2,2,0],
  [0,2,2,0,0,0,0,0,0,2,2,0],
  [0,2,2,0,0,0,0,0,0,2,2,0],
  [0,2,2,2,2,0,0,2,2,2,2,0],
  [0,2,2,2,2,0,0,2,2,2,2,0]
 ],
 [ #vert_moat
  [0,0,0,0,0,0,0,0,2,0,0,0],
  [0,0,0,0,0,0,0,0,2,0,0,0],
  [0,0,0,0,0,0,0,0,2,0,0,0],
  [0,0,0,0,0,0,0,0,2,0,0,0],
  [0,0,0,0,0,0,0,0,2,0,0,0],
  [0,0,0,0,0,0,0,0,2,0,0,0],
  [0,0,0,0,0,0,0,0,2,0,0,0]
 ],
 [ #circle_moat
  [0,0,0,0,0,0,0,0,0,0,0,0],
  [0,2,2,2,2,2,2,2,2,2,2,0],
  [0,2,0,0,0,0,0,0,0,0,2,0],
  [0,2,0,0,0,0,0,0,0,0,2,0],
  [0,2,0,0,0,0,0,0,0,0,2,0],
  [0,2,2,2,2,2,2,2,2,2,2,0],
  [0,0,0,0,0,0,0,0,0,0,0,0]
 ],
 [ #pointless_moat
  [0,0,0,0,0,0,0,0,0,0,0,0],
  [0,2,2,2,0,0,0,0,2,2,2,0],
  [0,2,0,0,0,0,0,0,0,0,2,0],
  [0,2,0,2,2,2,2,2,2,0,2,0],
  [0,2,0,0,0,0,0,0,0,0,2,0],
  [0,2,2,2,0,0,0,0,2,2,2,0],
  [0,0,0,0,0,0,0,0,0,0,0,0]
 ],
 [ #chevy
  [2,2,2,2,2,0,0,2,2,2,2,2],
  [2,0,0,0,2,2,2,2,0,0,0,2],
  [2,0,2,2,2,0,0,2,2,2,0,2],
  [0,0,2,0,0,0,0,0,0,2,0,0],
  [2,0,2,2,2,0,0,2,2,2,0,2],
  [2,0,0,0,2,2,2,2,0,0,0,2],
  [2,2,2,2,2,0,0,2,2,2,2,2]
 ],
 [ #nsu
  [2,2,2,2,2,0,0,2,2,2,2,2],
  [2,0,0,0,2,0,0,0,0,2,0,2],
  [2,0,2,0,2,0,2,2,0,2,0,2],
  [0,0,2,0,2,0,0,2,0,2,0,0],
  [2,0,2,0,2,2,0,2,0,2,0,2],
  [2,0,2,0,0,0,0,2,0,0,0,2],
  [2,2,2,2,2,0,0,2,2,2,2,2]
 ],
 [ #horiz_moat
  [0,0,0,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,0,0,0,0],
  [2,2,2,2,2,2,2,2,2,2,2,2],
  [0,0,0,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,0,0,0,0]
 ],
 [ #double_moat
  [0,0,0,0,0,0,0,0,0,0,0,0],
  [2,2,2,2,2,2,2,2,2,2,2,2],
  [0,0,0,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,0,0,0,0],
  [2,2,2,2,2,2,2,2,2,2,2,2],
  [0,0,0,0,0,0,0,0,0,0,0,0]
 ],
 [ #diamond_stair
  [0,0,0,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,1,0,0,0,0,0],
  [0,0,0,0,0,1,9,1,0,0,0,0],
  [0,0,0,0,1,9,4,9,1,0,0,0],
  [0,0,0,0,0,1,9,1,0,0,0,0],
  [0,0,0,0,0,0,1,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,0,0,0,0]
 ],
 [ #narrow_stair
  [0,0,0,0,0,0,0,0,1,1,1,1],
  [0,0,0,0,0,0,0,0,1,1,1,1],
  [0,0,0,0,0,0,0,0,0,1,1,1],
  [0,0,0,0,0,0,0,0,0,0,0,4],
  [0,0,0,0,0,0,0,0,0,1,1,1],
  [0,0,0,0,0,0,0,0,1,1,1,1],
  [0,0,0,0,0,0,0,0,1,1,1,1]
 ],
 [ #spiral_stair
  [0,0,0,0,0,0,0,0,0,0,1,0],
  [0,1,1,1,1,1,1,1,1,0,1,0],
  [0,1,0,0,0,0,0,4,1,0,1,0],
  [0,1,0,0,0,1,1,1,1,0,1,0],
  [0,1,0,0,0,0,0,0,0,0,1,0],
  [0,1,1,1,1,1,1,1,1,1,1,0],
  [0,0,0,0,0,0,0,0,0,0,0,0]
 ],
 [ #double_six
  [0,0,0,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,0,0,0,0],
  [0,0,1,1,0,0,0,0,1,1,0,0],
  [0,0,1,1,0,0,0,0,1,1,0,0],
  [0,0,1,1,0,0,0,0,1,1,0,0],
  [0,0,0,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,0,0,0,0]
 ],
 [ #single_six
  [0,0,0,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,1,1,0,0,0,0,0],
  [0,0,0,0,0,1,1,0,0,0,0,0],
  [0,0,0,0,0,1,1,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,0,0,0,0]
 ],
 [ #five_pair
  [0,0,0,0,0,0,0,0,0,0,0,0],
  [0,1,1,0,0,0,0,0,0,1,1,0],
  [0,0,0,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,1,1,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,0,0,0,0],
  [0,1,1,0,0,0,0,0,0,1,1,0],
  [0,0,0,0,0,0,0,0,0,0,0,0]
 ],
 [ #second_quest_pushblock
  [1,1,1,1,1,0,0,1,1,1,1,1],
  [1,1,1,1,1,1,0,1,1,1,1,1],
  [1,1,1,1,1,1,0,1,1,1,1,1],
  [0,0,0,0,0,0,1,0,0,0,0,0],
  [1,1,1,1,1,1,0,1,1,1,1,1],
  [1,1,1,1,1,1,0,1,1,1,1,1],
  [1,1,1,1,1,0,0,1,1,1,1,1]
 ],
 [ #entrance
  [0,0,0,0,0,0,0,0,0,0,0,0],
  [0,3,0,0,3,0,0,3,0,0,3,0],
  [0,0,0,0,0,0,0,0,0,0,0,0],
  [0,3,0,0,3,0,0,3,0,0,3,0],
  [0,0,0,0,0,0,0,0,0,0,0,0],
  [0,3,0,0,3,0,0,3,0,0,3,0],
  [0,0,0,0,0,0,0,0,0,0,0,0]
 ],
 [ #single_block
  [0,0,0,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,1,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,0,0,0,0]
 ],
 [ #two_fireball
  [0,0,0,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,3,0,0,3,0,0,0,0],
  [0,0,0,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,0,0,0,0]
 ],
 [ #four_fireball
  [3,0,0,0,0,0,0,0,0,0,0,3],
  [0,0,0,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,0,0,0,0],
  [3,0,0,0,0,0,0,0,0,0,0,3]
 ],
 [ #desert
  [0,0,0,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,0,0,0,0]
 ],
 [ #black
  [0,0,0,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,0,0,0,0]
 ],
 [ #zelda_room
  [1,1,1,1,1,1,1,1,1,1,1,1],
  [1,0,0,0,1,5,5,1,0,0,0,1],
  [1,0,1,1,5,5,5,5,1,1,0,1],
  [1,0,1,1,5,5,5,5,1,1,0,1],
  [1,0,0,0,1,0,0,1,0,0,0,1],
  [1,0,0,0,0,0,0,0,0,0,0,1],
  [1,0,1,0,0,0,0,0,0,1,0,1]
 ],
 [ #gannon_room
  [1,5,5,0,0,0,0,0,0,5,5,1],
  [5,5,0,0,5,0,0,5,0,0,5,5],
  [5,5,0,5,5,0,0,5,5,0,5,5],
  [5,5,0,5,5,0,0,5,5,0,5,5],
  [5,5,0,0,0,5,5,0,0,0,5,5],
  [5,5,5,5,0,0,0,0,5,5,5,5],
  [1,5,5,5,0,0,0,0,5,5,5,1]
 ],
 [ #triforce_room
  [0,0,0,0,0,0,0,0,0,0,0,0],
  [0,1,1,1,1,1,1,1,1,1,1,0],
  [0,1,0,0,3,0,0,3,0,0,1,0],
  [0,1,0,3,0,0,0,0,3,0,1,0],
  [0,1,0,0,0,0,0,0,0,0,1,0],
  [0,1,1,1,1,0,0,1,1,1,1,0],
  [0,0,0,0,0,0,0,0,0,0,0,0]
 ],
]

# yapf: enable

# Rooms where mobility is restricted without a ladder.
# Note that while the player can exit and enter through any door in a CIRCLE_MOAT_ROOM, we keep
# it in this Dict since a room item may not be abssle to be picked up without the ladder.
VALID_TRAVEL_DIRECTIONS_IN_WATER_ROOMS: Dict[RoomType, List[Direction]] = {
    RoomType.CIRCLE_MOAT_ROOM: [Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST],
    RoomType.DOUBLE_MOAT_ROOM: [Direction.EAST, Direction.WEST],
    RoomType.HORIZONTAL_MOAT_ROOM: [Direction.EAST, Direction.SOUTH, Direction.WEST],
    RoomType.VERTICAL_MOAT_ROOM: [Direction.SOUTH, Direction.WEST, Direction.NORTH],
    RoomType.CHEVY_ROOM: [],
    RoomType.SECOND_QUEST_T_LIKE_ROOM: [Direction.NORTH, Direction.EAST],
    RoomType.POINTLESS_MOAT_ROOM: [
        Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST
    ],
    RoomType.NSU: [Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST],
    RoomType.T_ROOM: [Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST]
}

VALID_TRAVEL_DIRECTIONS_IN_MOVEMENT_RESTRICTED_ROOMS: Dict[RoomType, List[Direction]] = {
    RoomType.HORIZONTAL_CHUTE_ROOM: [Direction.EAST, Direction.WEST],
    RoomType.VERTICAL_CHUTE_ROOM: [Direction.NORTH, Direction.SOUTH],
    RoomType.T_ROOM: [Direction.WEST, Direction.NORTH, Direction.EAST],
    RoomType.SECOND_QUEST_T_LIKE_ROOM: [Direction.NORTH, Direction.EAST],
    RoomType.CIRCLE_BLOCK_WALL_ROOM: [
        Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST
    ],
    RoomType.KIDNAPPED_ROOM: [Direction.SOUTH]
}
