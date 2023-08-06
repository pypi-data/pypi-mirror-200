from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="VersionResponse")


@attr.s(auto_attribs=True)
class VersionResponse:
    """
    Attributes:
        current (str): current version Example: 0.17.0.
        next_ (str): next version Example: 0.18.0.
        querier (str): querier version Example: 0.16.0.
    """

    current: str
    next_: str
    querier: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        current = self.current
        next_ = self.next_
        querier = self.querier

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "current": current,
                "next": next_,
                "querier": querier,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        current = d.pop("current")

        next_ = d.pop("next")

        querier = d.pop("querier")

        version_response = cls(
            current=current,
            next_=next_,
            querier=querier,
        )

        version_response.additional_properties = d
        return version_response

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
