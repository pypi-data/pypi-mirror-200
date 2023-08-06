from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="TxStagesResponseInboundObserved")


@attr.s(auto_attribs=True)
class TxStagesResponseInboundObserved:
    """
    Attributes:
        completed (bool): returns true if no transaction observation remains to be done
        started (Union[Unset, bool]): returns true if any nodes have observed the transaction
    """

    completed: bool
    started: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        completed = self.completed
        started = self.started

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "completed": completed,
            }
        )
        if started is not UNSET:
            field_dict["started"] = started

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        completed = d.pop("completed")

        started = d.pop("started", UNSET)

        tx_stages_response_inbound_observed = cls(
            completed=completed,
            started=started,
        )

        tx_stages_response_inbound_observed.additional_properties = d
        return tx_stages_response_inbound_observed

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
