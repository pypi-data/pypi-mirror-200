from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="NodeChainHeight")


@attr.s(auto_attribs=True)
class NodeChainHeight:
    """
    Attributes:
        chain (str):  Example: BTC.
        height (int):  Example: 2000000.
    """

    chain: str
    height: int
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        chain = self.chain
        height = self.height

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "chain": chain,
                "height": height,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        chain = d.pop("chain")

        height = d.pop("height")

        node_chain_height = cls(
            chain=chain,
            height=height,
        )

        node_chain_height.additional_properties = d
        return node_chain_height

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
