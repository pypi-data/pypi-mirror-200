from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="LastBlock")


@attr.s(auto_attribs=True)
class LastBlock:
    """
    Attributes:
        chain (str):
        last_observed_in (int):
        last_signed_out (int):
        thorchain (int):
    """

    chain: str
    last_observed_in: int
    last_signed_out: int
    thorchain: int
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        chain = self.chain
        last_observed_in = self.last_observed_in
        last_signed_out = self.last_signed_out
        thorchain = self.thorchain

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "chain": chain,
                "last_observed_in": last_observed_in,
                "last_signed_out": last_signed_out,
                "thorchain": thorchain,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        chain = d.pop("chain")

        last_observed_in = d.pop("last_observed_in")

        last_signed_out = d.pop("last_signed_out")

        thorchain = d.pop("thorchain")

        last_block = cls(
            chain=chain,
            last_observed_in=last_observed_in,
            last_signed_out=last_signed_out,
            thorchain=thorchain,
        )

        last_block.additional_properties = d
        return last_block

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
