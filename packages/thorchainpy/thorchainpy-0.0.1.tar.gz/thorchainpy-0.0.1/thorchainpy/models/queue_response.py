from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="QueueResponse")


@attr.s(auto_attribs=True)
class QueueResponse:
    """
    Attributes:
        swap (int):
        outbound (int): number of signed outbound tx in the queue Example: 10.
        internal (int):
        scheduled_outbound_value (str): scheduled outbound value in RUNE
    """

    swap: int
    outbound: int
    internal: int
    scheduled_outbound_value: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        swap = self.swap
        outbound = self.outbound
        internal = self.internal
        scheduled_outbound_value = self.scheduled_outbound_value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "swap": swap,
                "outbound": outbound,
                "internal": internal,
                "scheduled_outbound_value": scheduled_outbound_value,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        swap = d.pop("swap")

        outbound = d.pop("outbound")

        internal = d.pop("internal")

        scheduled_outbound_value = d.pop("scheduled_outbound_value")

        queue_response = cls(
            swap=swap,
            outbound=outbound,
            internal=internal,
            scheduled_outbound_value=scheduled_outbound_value,
        )

        queue_response.additional_properties = d
        return queue_response

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
