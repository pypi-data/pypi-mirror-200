from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="TxStagesResponseOutboundDelay")


@attr.s(auto_attribs=True)
class TxStagesResponseOutboundDelay:
    """
    Attributes:
        completed (bool): returns true if no transaction outbound delay remains
        remaining_delay_blocks (Union[Unset, int]): the number of remaining THORChain blocks the outbound will be
            delayed Example: 5.
        remaining_delay_seconds (Union[Unset, int]): the estimated remaining seconds of the outbound delay before it
            will be sent Example: 30.
    """

    completed: bool
    remaining_delay_blocks: Union[Unset, int] = UNSET
    remaining_delay_seconds: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        completed = self.completed
        remaining_delay_blocks = self.remaining_delay_blocks
        remaining_delay_seconds = self.remaining_delay_seconds

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "completed": completed,
            }
        )
        if remaining_delay_blocks is not UNSET:
            field_dict["remaining_delay_blocks"] = remaining_delay_blocks
        if remaining_delay_seconds is not UNSET:
            field_dict["remaining_delay_seconds"] = remaining_delay_seconds

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        completed = d.pop("completed")

        remaining_delay_blocks = d.pop("remaining_delay_blocks", UNSET)

        remaining_delay_seconds = d.pop("remaining_delay_seconds", UNSET)

        tx_stages_response_outbound_delay = cls(
            completed=completed,
            remaining_delay_blocks=remaining_delay_blocks,
            remaining_delay_seconds=remaining_delay_seconds,
        )

        tx_stages_response_outbound_delay.additional_properties = d
        return tx_stages_response_outbound_delay

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
