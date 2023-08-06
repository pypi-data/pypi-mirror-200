from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.coin import Coin


T = TypeVar("T", bound="TxOutItem")


@attr.s(auto_attribs=True)
class TxOutItem:
    """
    Attributes:
        chain (str):  Example: ETH.
        to_address (str):  Example: 0x66fb1cd65b97fa40457b90b7d1ca6b92cb64b32b.
        coin (Coin):
        max_gas (List['Coin']):
        height (int):  Example: 1234.
        vault_pub_key (Union[Unset, str]):  Example:
            thorpub1addwnpepqt45wmsxj29xpgdrdsvg2h3dx68qeapgykw3hlyj6vuds2r0pnkwx5gt9m4.
        memo (Union[Unset, str]):  Example: OUT:208BF0ACD78C89A0534B0457BA0867B101961A2319C1E49DD28676526904BBEA.
        gas_rate (Union[Unset, int]):
        in_hash (Union[Unset, str]):  Example: 208BF0ACD78C89A0534B0457BA0867B101961A2319C1E49DD28676526904BBEA.
        out_hash (Union[Unset, str]):  Example: 0D0B2FDB6DAD6E5FD3C5E46D39128F9DA15E96F0B2CC054CE059EA3532B150FB.
    """

    chain: str
    to_address: str
    coin: "Coin"
    max_gas: List["Coin"]
    height: int
    vault_pub_key: Union[Unset, str] = UNSET
    memo: Union[Unset, str] = UNSET
    gas_rate: Union[Unset, int] = UNSET
    in_hash: Union[Unset, str] = UNSET
    out_hash: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        chain = self.chain
        to_address = self.to_address
        coin = self.coin.to_dict()

        max_gas = []
        for max_gas_item_data in self.max_gas:
            max_gas_item = max_gas_item_data.to_dict()

            max_gas.append(max_gas_item)

        height = self.height
        vault_pub_key = self.vault_pub_key
        memo = self.memo
        gas_rate = self.gas_rate
        in_hash = self.in_hash
        out_hash = self.out_hash

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "chain": chain,
                "to_address": to_address,
                "coin": coin,
                "max_gas": max_gas,
                "height": height,
            }
        )
        if vault_pub_key is not UNSET:
            field_dict["vault_pub_key"] = vault_pub_key
        if memo is not UNSET:
            field_dict["memo"] = memo
        if gas_rate is not UNSET:
            field_dict["gas_rate"] = gas_rate
        if in_hash is not UNSET:
            field_dict["in_hash"] = in_hash
        if out_hash is not UNSET:
            field_dict["out_hash"] = out_hash

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.coin import Coin

        d = src_dict.copy()
        chain = d.pop("chain")

        to_address = d.pop("to_address")

        coin = Coin.from_dict(d.pop("coin"))

        max_gas = []
        _max_gas = d.pop("max_gas")
        for max_gas_item_data in _max_gas:
            max_gas_item = Coin.from_dict(max_gas_item_data)

            max_gas.append(max_gas_item)

        height = d.pop("height")

        vault_pub_key = d.pop("vault_pub_key", UNSET)

        memo = d.pop("memo", UNSET)

        gas_rate = d.pop("gas_rate", UNSET)

        in_hash = d.pop("in_hash", UNSET)

        out_hash = d.pop("out_hash", UNSET)

        tx_out_item = cls(
            chain=chain,
            to_address=to_address,
            coin=coin,
            max_gas=max_gas,
            height=height,
            vault_pub_key=vault_pub_key,
            memo=memo,
            gas_rate=gas_rate,
            in_hash=in_hash,
            out_hash=out_hash,
        )

        tx_out_item.additional_properties = d
        return tx_out_item

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
