from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.keysign_response_keysign_info import KeysignResponseKeysignInfo


T = TypeVar("T", bound="KeysignResponse")


@attr.s(auto_attribs=True)
class KeysignResponse:
    """
    Attributes:
        keysign (Union[Unset, KeysignResponseKeysignInfo]):
        signature (Union[Unset, str]):
    """

    keysign: Union[Unset, "KeysignResponseKeysignInfo"] = UNSET
    signature: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        keysign: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.keysign, Unset):
            keysign = self.keysign.to_dict()

        signature = self.signature

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if keysign is not UNSET:
            field_dict["keysign"] = keysign
        if signature is not UNSET:
            field_dict["signature"] = signature

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.keysign_response_keysign_info import KeysignResponseKeysignInfo

        d = src_dict.copy()
        _keysign = d.pop("keysign", UNSET)
        keysign: Union[Unset, KeysignResponseKeysignInfo]
        if isinstance(_keysign, Unset):
            keysign = UNSET
        else:
            keysign = KeysignResponseKeysignInfo.from_dict(_keysign)

        signature = d.pop("signature", UNSET)

        keysign_response = cls(
            keysign=keysign,
            signature=signature,
        )

        keysign_response.additional_properties = d
        return keysign_response

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
