from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="InvariantResponse")


@attr.s(auto_attribs=True)
class InvariantResponse:
    """
    Attributes:
        invariant (str): The name of the invariant. Example: asgard.
        broken (bool): Returns true if the invariant is broken.
        msg (str): Informative message about the invariant result. Example: insolvent: 200000rune
            oversolvent: 1btc/btc.
    """

    invariant: str
    broken: bool
    msg: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        invariant = self.invariant
        broken = self.broken
        msg = self.msg

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "invariant": invariant,
                "broken": broken,
                "msg": msg,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        invariant = d.pop("invariant")

        broken = d.pop("broken")

        msg = d.pop("msg")

        invariant_response = cls(
            invariant=invariant,
            broken=broken,
            msg=msg,
        )

        invariant_response.additional_properties = d
        return invariant_response

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
