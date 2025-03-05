from enums import CellType

RANDOM_SEED = 2025

FIRE_PROBABILITIES = {
    CellType.FLOOR.value: 0.6,
    CellType.WALL.value: 0.1,
    CellType.EXIT.value: 0.0,
    CellType.FILLER.value: 0.0
}

SMOKE_PROBABILITIES = {
    CellType.FLOOR.value: 0.8,
    CellType.WALL.value: 0.0,
    CellType.EXIT.value: 0.0,
    CellType.FILLER.value: 0.01
}

FIRE_ACTIVITY = 0.3
SMOKE_ACTIVITY = 0.2

PEOPLE_COUNT = 5000
PANIC_DEGREE = 0.8

