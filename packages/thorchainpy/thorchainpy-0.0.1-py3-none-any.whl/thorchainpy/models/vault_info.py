from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

import attr

if TYPE_CHECKING:
    from ..models.vault_router import VaultRouter


T = TypeVar("T", bound="VaultInfo")


@attr.s(auto_attribs=True)
class VaultInfo:
    """
    Attributes:
        pub_key (str):  Example: thorpub1addwnpepq068dr0x7ue973drmq4eqmzhcq3650n7nx5fhgn9gl207luxp6vaklu52tc.
        routers (List['VaultRouter']):
    """

    pub_key: str
    routers: List["VaultRouter"]
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        pub_key = self.pub_key
        routers = []
        for routers_item_data in self.routers:
            routers_item = routers_item_data.to_dict()

            routers.append(routers_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "pub_key": pub_key,
                "routers": routers,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.vault_router import VaultRouter

        d = src_dict.copy()
        pub_key = d.pop("pub_key")

        routers = []
        _routers = d.pop("routers")
        for routers_item_data in _routers:
            routers_item = VaultRouter.from_dict(routers_item_data)

            routers.append(routers_item)

        vault_info = cls(
            pub_key=pub_key,
            routers=routers,
        )

        vault_info.additional_properties = d
        return vault_info

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
