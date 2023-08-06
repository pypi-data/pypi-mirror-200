from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.thorname_alias import ThornameAlias


T = TypeVar("T", bound="Thorname")


@attr.s(auto_attribs=True)
class Thorname:
    """
    Attributes:
        preferred_asset (str):  Example: BTC.BTC.
        aliases (List['ThornameAlias']):
        name (Union[Unset, str]):  Example: thor.
        expire_block_height (Union[Unset, int]):  Example: 1234.
        owner (Union[Unset, str]):  Example: thor1f3s7q037eancht7sg0aj995dht25rwrnu4ats5.
    """

    preferred_asset: str
    aliases: List["ThornameAlias"]
    name: Union[Unset, str] = UNSET
    expire_block_height: Union[Unset, int] = UNSET
    owner: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        preferred_asset = self.preferred_asset
        aliases = []
        for aliases_item_data in self.aliases:
            aliases_item = aliases_item_data.to_dict()

            aliases.append(aliases_item)

        name = self.name
        expire_block_height = self.expire_block_height
        owner = self.owner

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "preferred_asset": preferred_asset,
                "aliases": aliases,
            }
        )
        if name is not UNSET:
            field_dict["name"] = name
        if expire_block_height is not UNSET:
            field_dict["expire_block_height"] = expire_block_height
        if owner is not UNSET:
            field_dict["owner"] = owner

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.thorname_alias import ThornameAlias

        d = src_dict.copy()
        preferred_asset = d.pop("preferred_asset")

        aliases = []
        _aliases = d.pop("aliases")
        for aliases_item_data in _aliases:
            aliases_item = ThornameAlias.from_dict(aliases_item_data)

            aliases.append(aliases_item)

        name = d.pop("name", UNSET)

        expire_block_height = d.pop("expire_block_height", UNSET)

        owner = d.pop("owner", UNSET)

        thorname = cls(
            preferred_asset=preferred_asset,
            aliases=aliases,
            name=name,
            expire_block_height=expire_block_height,
            owner=owner,
        )

        thorname.additional_properties = d
        return thorname

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
