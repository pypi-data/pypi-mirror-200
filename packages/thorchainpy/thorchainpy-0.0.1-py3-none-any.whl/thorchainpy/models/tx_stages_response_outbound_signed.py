from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="TxStagesResponseOutboundSigned")


@attr.s(auto_attribs=True)
class TxStagesResponseOutboundSigned:
    """
    Attributes:
        completed (bool): returns true if an external transaction has been signed and broadcast (and observed in its
            mempool)
        scheduled_outbound_height (Union[Unset, int]): THORChain height for which the external outbound is scheduled
            Example: 1234.
        blocks_since_scheduled (Union[Unset, int]): THORChain blocks since the scheduled outbound height Example: 1234.
    """

    completed: bool
    scheduled_outbound_height: Union[Unset, int] = UNSET
    blocks_since_scheduled: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        completed = self.completed
        scheduled_outbound_height = self.scheduled_outbound_height
        blocks_since_scheduled = self.blocks_since_scheduled

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "completed": completed,
            }
        )
        if scheduled_outbound_height is not UNSET:
            field_dict["scheduled_outbound_height"] = scheduled_outbound_height
        if blocks_since_scheduled is not UNSET:
            field_dict["blocks_since_scheduled"] = blocks_since_scheduled

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        completed = d.pop("completed")

        scheduled_outbound_height = d.pop("scheduled_outbound_height", UNSET)

        blocks_since_scheduled = d.pop("blocks_since_scheduled", UNSET)

        tx_stages_response_outbound_signed = cls(
            completed=completed,
            scheduled_outbound_height=scheduled_outbound_height,
            blocks_since_scheduled=blocks_since_scheduled,
        )

        tx_stages_response_outbound_signed.additional_properties = d
        return tx_stages_response_outbound_signed

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
