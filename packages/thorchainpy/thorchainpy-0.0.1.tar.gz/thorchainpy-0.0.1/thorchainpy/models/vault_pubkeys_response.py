from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

import attr

if TYPE_CHECKING:
    from ..models.vault_info import VaultInfo


T = TypeVar("T", bound="VaultPubkeysResponse")


@attr.s(auto_attribs=True)
class VaultPubkeysResponse:
    """
    Attributes:
        asgard (List['VaultInfo']):
        yggdrasil (List['VaultInfo']):
    """

    asgard: List["VaultInfo"]
    yggdrasil: List["VaultInfo"]
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        asgard = []
        for asgard_item_data in self.asgard:
            asgard_item = asgard_item_data.to_dict()

            asgard.append(asgard_item)

        yggdrasil = []
        for yggdrasil_item_data in self.yggdrasil:
            yggdrasil_item = yggdrasil_item_data.to_dict()

            yggdrasil.append(yggdrasil_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "asgard": asgard,
                "yggdrasil": yggdrasil,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.vault_info import VaultInfo

        d = src_dict.copy()
        asgard = []
        _asgard = d.pop("asgard")
        for asgard_item_data in _asgard:
            asgard_item = VaultInfo.from_dict(asgard_item_data)

            asgard.append(asgard_item)

        yggdrasil = []
        _yggdrasil = d.pop("yggdrasil")
        for yggdrasil_item_data in _yggdrasil:
            yggdrasil_item = VaultInfo.from_dict(yggdrasil_item_data)

            yggdrasil.append(yggdrasil_item)

        vault_pubkeys_response = cls(
            asgard=asgard,
            yggdrasil=yggdrasil,
        )

        vault_pubkeys_response.additional_properties = d
        return vault_pubkeys_response

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
