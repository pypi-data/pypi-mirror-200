from enum import IntEnum, auto


class DBStep(IntEnum):
    """
    Steps to create a db instance to rethinkdb as a source
    """
    CREATE = auto()  # 1
    CONNECT = auto()
    COLLECT = auto()
    DELETE = auto()  # 4


class DBSend(IntEnum):
    """
    Steps to create a db instance to rethinkdb as a destiny
    """
    CREATE = auto()  # 1
    CONNECT = auto()
    SEND = auto()  # 3
