from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="NodeNodePubKeySet")


@attr.s(auto_attribs=True)
class NodeNodePubKeySet:
    """
    Attributes:
        secp256k1 (Union[Unset, str]):  Example:
            thorpub1addwnpepq27ck6u44zl8qqdnmzjjc8rg72amrxrsp42p9vd7kt6marhy6ww76z8shwe.
        ed25519 (Union[Unset, str]):  Example:
            thorpub1addwnpepq27ck6u44zl8qqdnmzjjc8rg72amrxrsp42p9vd7kt6marhy6ww76z8shwe.
    """

    secp256k1: Union[Unset, str] = UNSET
    ed25519: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        secp256k1 = self.secp256k1
        ed25519 = self.ed25519

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if secp256k1 is not UNSET:
            field_dict["secp256k1"] = secp256k1
        if ed25519 is not UNSET:
            field_dict["ed25519"] = ed25519

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        secp256k1 = d.pop("secp256k1", UNSET)

        ed25519 = d.pop("ed25519", UNSET)

        node_node_pub_key_set = cls(
            secp256k1=secp256k1,
            ed25519=ed25519,
        )

        node_node_pub_key_set.additional_properties = d
        return node_node_pub_key_set

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
