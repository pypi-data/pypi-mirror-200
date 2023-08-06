from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="TxStagesResponseInboundFinalised")


@attr.s(auto_attribs=True)
class TxStagesResponseInboundFinalised:
    """
    Attributes:
        completed (bool): returns true if the inbound transaction has been finalised (THORChain agreeing it exists)
    """

    completed: bool
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        completed = self.completed

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "completed": completed,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        completed = d.pop("completed")

        tx_stages_response_inbound_finalised = cls(
            completed=completed,
        )

        tx_stages_response_inbound_finalised.additional_properties = d
        return tx_stages_response_inbound_finalised

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
