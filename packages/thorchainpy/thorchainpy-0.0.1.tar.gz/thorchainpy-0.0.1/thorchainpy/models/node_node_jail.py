from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="NodeNodeJail")


@attr.s(auto_attribs=True)
class NodeNodeJail:
    """
    Attributes:
        release_height (Union[Unset, int]):  Example: 1234.
        reason (Union[Unset, str]):
    """

    release_height: Union[Unset, int] = UNSET
    reason: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        release_height = self.release_height
        reason = self.reason

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if release_height is not UNSET:
            field_dict["release_height"] = release_height
        if reason is not UNSET:
            field_dict["reason"] = reason

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        release_height = d.pop("release_height", UNSET)

        reason = d.pop("reason", UNSET)

        node_node_jail = cls(
            release_height=release_height,
            reason=reason,
        )

        node_node_jail.additional_properties = d
        return node_node_jail

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
