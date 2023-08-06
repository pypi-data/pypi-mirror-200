from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="MimirNodesResponseMimirVote")


@attr.s(auto_attribs=True)
class MimirNodesResponseMimirVote:
    """
    Attributes:
        key (Union[Unset, str]):
        value (Union[Unset, int]):
        signer (Union[Unset, str]):
    """

    key: Union[Unset, str] = UNSET
    value: Union[Unset, int] = UNSET
    signer: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        key = self.key
        value = self.value
        signer = self.signer

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if key is not UNSET:
            field_dict["key"] = key
        if value is not UNSET:
            field_dict["value"] = value
        if signer is not UNSET:
            field_dict["signer"] = signer

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        key = d.pop("key", UNSET)

        value = d.pop("value", UNSET)

        signer = d.pop("signer", UNSET)

        mimir_nodes_response_mimir_vote = cls(
            key=key,
            value=value,
            signer=signer,
        )

        mimir_nodes_response_mimir_vote.additional_properties = d
        return mimir_nodes_response_mimir_vote

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
