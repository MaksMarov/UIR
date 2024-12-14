from enum import Enum

# ����������� ��������
class IntentionalDirection(Enum):
    NONE = 0
    STRAIGHT = 1
    RIGHT = 2
    LEFT = 3
    U_TURN = 4
    
# ����������� ������
class CellDirection(Enum):
    NONE = 0
    NORTH = 1
    EAST = 2
    SOUTH = 3
    WEST = 4
    
class GenerationPriority():
    EW = -1
    NONE = 0
    NS = 1
    
# ���� ������
class CellType(Enum):
    EMPTY = 0
    UD_ROAD = 1
    TRAFFIC_LIGHT = 2
    ROADSIDE = 3
    MD_ROAD = 4

# ��������� ������� ���������
class LightSignal(Enum):
    TURNED_OFF = 0
    RED = 1
    YELLOW = 2
    GREEN = 3
    
# ���������� �������� ����������
class CrossroadLightState(Enum):
    TURN_OFF_ALL = 0
    WAITING = 1
    ALLOW_NS = 2
    ALLOW_EW = 3
    BUN_ALL = 4
    ALLOW_ALL = 5
    
# ��������� ����������� ���������
class TrafficLightControllerState(Enum):
    TURNED_OFF = 0
    SIMPLE = 1
    ADAPTIVE = 2
    
# ���� �����������
class CrossroadType(Enum):
    NONE = 0
    SINGLE_LANE = 1
    TWO_LANE = 2
    THREE_LANE = 3