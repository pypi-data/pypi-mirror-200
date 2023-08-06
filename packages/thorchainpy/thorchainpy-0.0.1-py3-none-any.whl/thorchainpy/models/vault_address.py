from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="VaultAddress")


@attr.s(auto_attribs=True)
class VaultAddress:
    """
    Attributes:
        chain (Union[Unset, str]):  Example: BTC.
        address (Union[Unset, str]):  Example: bc1qd45uzetakjvdy5ynjjyp4nlnj89am88e4e5jeq.
    """

    chain: Union[Unset, str] = UNSET
    address: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        chain = self.chain
        address = self.address

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if chain is not UNSET:
            field_dict["chain"] = chain
        if address is not UNSET:
            field_dict["address"] = address

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        chain = d.pop("chain", UNSET)

        address = d.pop("address", UNSET)

        vault_address = cls(
            chain=chain,
            address=address,
        )

        vault_address.additional_properties = d
        return vault_address

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
