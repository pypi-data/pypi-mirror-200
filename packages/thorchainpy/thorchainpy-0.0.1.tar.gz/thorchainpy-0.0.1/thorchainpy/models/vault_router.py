from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="VaultRouter")


@attr.s(auto_attribs=True)
class VaultRouter:
    """
    Attributes:
        chain (Union[Unset, str]):  Example: ETH.
        router (Union[Unset, str]):  Example: 0x3624525075b88B24ecc29CE226b0CEc1fFcB6976.
    """

    chain: Union[Unset, str] = UNSET
    router: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        chain = self.chain
        router = self.router

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if chain is not UNSET:
            field_dict["chain"] = chain
        if router is not UNSET:
            field_dict["router"] = router

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        chain = d.pop("chain", UNSET)

        router = d.pop("router", UNSET)

        vault_router = cls(
            chain=chain,
            router=router,
        )

        vault_router.additional_properties = d
        return vault_router

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
