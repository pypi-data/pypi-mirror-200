from enum import Enum


class ObservedTxStatus(str, Enum):
    DONE = "done"
    INCOMPLETE = "incomplete"

    def __str__(self) -> str:
        return str(self.value)
