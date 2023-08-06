from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="BanResponse")


@attr.s(auto_attribs=True)
class BanResponse:
    """
    Attributes:
        node_address (Union[Unset, str]):  Example: thor1f3s7q037eancht7sg0aj995dht25rwrnu4ats5.
        block_height (Union[Unset, int]):
        signers (Union[Unset, List[str]]):
    """

    node_address: Union[Unset, str] = UNSET
    block_height: Union[Unset, int] = UNSET
    signers: Union[Unset, List[str]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        node_address = self.node_address
        block_height = self.block_height
        signers: Union[Unset, List[str]] = UNSET
        if not isinstance(self.signers, Unset):
            signers = self.signers

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if node_address is not UNSET:
            field_dict["node_address"] = node_address
        if block_height is not UNSET:
            field_dict["block_height"] = block_height
        if signers is not UNSET:
            field_dict["signers"] = signers

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        node_address = d.pop("node_address", UNSET)

        block_height = d.pop("block_height", UNSET)

        signers = cast(List[str], d.pop("signers", UNSET))

        ban_response = cls(
            node_address=node_address,
            block_height=block_height,
            signers=signers,
        )

        ban_response.additional_properties = d
        return ban_response

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
