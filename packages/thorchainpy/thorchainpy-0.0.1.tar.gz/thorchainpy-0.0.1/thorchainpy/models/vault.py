from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.vault_type import VaultType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.coin import Coin
    from ..models.vault_address import VaultAddress
    from ..models.vault_router import VaultRouter


T = TypeVar("T", bound="Vault")


@attr.s(auto_attribs=True)
class Vault:
    """
    Attributes:
        coins (List['Coin']):
        routers (List['VaultRouter']):
        addresses (List['VaultAddress']):
        block_height (Union[Unset, int]):
        pub_key (Union[Unset, str]):
        type (Union[Unset, VaultType]):
        status (Union[Unset, str]):
        status_since (Union[Unset, int]):
        membership (Union[Unset, List[str]]): the list of node public keys which are members of the vault
        chains (Union[Unset, List[str]]):
        inbound_tx_count (Union[Unset, int]):
        outbound_tx_count (Union[Unset, int]):
        pending_tx_block_heights (Union[Unset, List[int]]):
    """

    coins: List["Coin"]
    routers: List["VaultRouter"]
    addresses: List["VaultAddress"]
    block_height: Union[Unset, int] = UNSET
    pub_key: Union[Unset, str] = UNSET
    type: Union[Unset, VaultType] = UNSET
    status: Union[Unset, str] = UNSET
    status_since: Union[Unset, int] = UNSET
    membership: Union[Unset, List[str]] = UNSET
    chains: Union[Unset, List[str]] = UNSET
    inbound_tx_count: Union[Unset, int] = UNSET
    outbound_tx_count: Union[Unset, int] = UNSET
    pending_tx_block_heights: Union[Unset, List[int]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        coins = []
        for coins_item_data in self.coins:
            coins_item = coins_item_data.to_dict()

            coins.append(coins_item)

        routers = []
        for routers_item_data in self.routers:
            routers_item = routers_item_data.to_dict()

            routers.append(routers_item)

        addresses = []
        for addresses_item_data in self.addresses:
            addresses_item = addresses_item_data.to_dict()

            addresses.append(addresses_item)

        block_height = self.block_height
        pub_key = self.pub_key
        type: Union[Unset, str] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type.value

        status = self.status
        status_since = self.status_since
        membership: Union[Unset, List[str]] = UNSET
        if not isinstance(self.membership, Unset):
            membership = self.membership

        chains: Union[Unset, List[str]] = UNSET
        if not isinstance(self.chains, Unset):
            chains = self.chains

        inbound_tx_count = self.inbound_tx_count
        outbound_tx_count = self.outbound_tx_count
        pending_tx_block_heights: Union[Unset, List[int]] = UNSET
        if not isinstance(self.pending_tx_block_heights, Unset):
            pending_tx_block_heights = self.pending_tx_block_heights

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "coins": coins,
                "routers": routers,
                "addresses": addresses,
            }
        )
        if block_height is not UNSET:
            field_dict["block_height"] = block_height
        if pub_key is not UNSET:
            field_dict["pub_key"] = pub_key
        if type is not UNSET:
            field_dict["type"] = type
        if status is not UNSET:
            field_dict["status"] = status
        if status_since is not UNSET:
            field_dict["status_since"] = status_since
        if membership is not UNSET:
            field_dict["membership"] = membership
        if chains is not UNSET:
            field_dict["chains"] = chains
        if inbound_tx_count is not UNSET:
            field_dict["inbound_tx_count"] = inbound_tx_count
        if outbound_tx_count is not UNSET:
            field_dict["outbound_tx_count"] = outbound_tx_count
        if pending_tx_block_heights is not UNSET:
            field_dict["pending_tx_block_heights"] = pending_tx_block_heights

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.coin import Coin
        from ..models.vault_address import VaultAddress
        from ..models.vault_router import VaultRouter

        d = src_dict.copy()
        coins = []
        _coins = d.pop("coins")
        for coins_item_data in _coins:
            coins_item = Coin.from_dict(coins_item_data)

            coins.append(coins_item)

        routers = []
        _routers = d.pop("routers")
        for routers_item_data in _routers:
            routers_item = VaultRouter.from_dict(routers_item_data)

            routers.append(routers_item)

        addresses = []
        _addresses = d.pop("addresses")
        for addresses_item_data in _addresses:
            addresses_item = VaultAddress.from_dict(addresses_item_data)

            addresses.append(addresses_item)

        block_height = d.pop("block_height", UNSET)

        pub_key = d.pop("pub_key", UNSET)

        _type = d.pop("type", UNSET)
        type: Union[Unset, VaultType]
        if isinstance(_type, Unset):
            type = UNSET
        else:
            type = VaultType(_type)

        status = d.pop("status", UNSET)

        status_since = d.pop("status_since", UNSET)

        membership = cast(List[str], d.pop("membership", UNSET))

        chains = cast(List[str], d.pop("chains", UNSET))

        inbound_tx_count = d.pop("inbound_tx_count", UNSET)

        outbound_tx_count = d.pop("outbound_tx_count", UNSET)

        pending_tx_block_heights = cast(List[int], d.pop("pending_tx_block_heights", UNSET))

        vault = cls(
            coins=coins,
            routers=routers,
            addresses=addresses,
            block_height=block_height,
            pub_key=pub_key,
            type=type,
            status=status,
            status_since=status_since,
            membership=membership,
            chains=chains,
            inbound_tx_count=inbound_tx_count,
            outbound_tx_count=outbound_tx_count,
            pending_tx_block_heights=pending_tx_block_heights,
        )

        vault.additional_properties = d
        return vault

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
