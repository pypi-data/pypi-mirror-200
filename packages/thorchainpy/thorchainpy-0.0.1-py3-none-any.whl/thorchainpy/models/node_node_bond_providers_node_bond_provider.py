from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="NodeNodeBondProvidersNodeBondProvider")


@attr.s(auto_attribs=True)
class NodeNodeBondProvidersNodeBondProvider:
    """
    Attributes:
        bond_address (Union[Unset, str]):
        bond (Union[Unset, str]):
    """

    bond_address: Union[Unset, str] = UNSET
    bond: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        bond_address = self.bond_address
        bond = self.bond

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if bond_address is not UNSET:
            field_dict["bond_address"] = bond_address
        if bond is not UNSET:
            field_dict["bond"] = bond

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        bond_address = d.pop("bond_address", UNSET)

        bond = d.pop("bond", UNSET)

        node_node_bond_providers_node_bond_provider = cls(
            bond_address=bond_address,
            bond=bond,
        )

        node_node_bond_providers_node_bond_provider.additional_properties = d
        return node_node_bond_providers_node_bond_provider

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
