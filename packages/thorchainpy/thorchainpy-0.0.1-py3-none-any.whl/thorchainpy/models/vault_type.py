from enum import Enum


class VaultType(str, Enum):
    ASGARDVAULT = "AsgardVault"
    YGGDRASILVAULT = "YggdrasilVault"

    def __str__(self) -> str:
        return str(self.value)
