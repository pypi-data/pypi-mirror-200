from enum import Enum


class NodeStatus(str, Enum):
    ACTIVE = "Active"
    DISABLED = "Disabled"
    STANDBY = "Standby"
    WHITELISTED = "Whitelisted"

    def __str__(self) -> str:
        return str(self.value)
