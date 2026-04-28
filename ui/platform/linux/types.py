from enum import IntEnum


class EventType(IntEnum):
    KEY_PRESS = 2
    EXPOSE = 12
    CONFIGURE_NOTIFY = 22
    CLIENT_MESSAGE = 33


class LineStyle(IntEnum):
    SOLID = 0


class CapStyle(IntEnum):
    BUTT = 1


class JoinStyle(IntEnum):
    MITER = 0


# GC component mask bits (subset of X.h)
GC_FOREGROUND = 1 << 3
GC_BACKGROUND = 1 << 4
GC_LINE_WIDTH = 1 << 12
GC_FONT = 1 << 14


# Event selection mask bits
EXPOSURE_MASK = 1 << 15
STRUCTURE_NOTIFY_MASK = 1 << 17


def default_event_mask() -> int:
    return EXPOSURE_MASK | STRUCTURE_NOTIFY_MASK
