from enum import Enum


# initial set of object types
class ObjectType(Enum):
    HOST = "host"
    NETWORK = "network"
    ADDRESS_RANGE = "address-range"
    GROUP = "group"


# details level of result
class DetailsLevel(Enum):
    UID = "uid"
    STANDARD = "standard"
    FULL = "full"
