from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="TxStagesResponseInboundConfirmationCounted")


@attr.s(auto_attribs=True)
class TxStagesResponseInboundConfirmationCounted:
    """
    Attributes:
        completed (bool): returns true if no transaction confirmation counting remains to be done
        counting_start_height (Union[Unset, int]): the THORChain block height when confirmation counting began Example:
            1234.
        chain (Union[Unset, str]): the external source chain for which confirmation counting takes place Example: BTC.
        external_observed_height (Union[Unset, int]): the block height on the external source chain when the transaction
            was observed Example: 16042625.
        external_confirmation_delay_height (Union[Unset, int]): the block height on the external source chain when
            confirmation counting will be complete Example: 16042626.
        remaining_confirmation_seconds (Union[Unset, int]): the estimated remaining seconds before confirmation counting
            completes Example: 600.
    """

    completed: bool
    counting_start_height: Union[Unset, int] = UNSET
    chain: Union[Unset, str] = UNSET
    external_observed_height: Union[Unset, int] = UNSET
    external_confirmation_delay_height: Union[Unset, int] = UNSET
    remaining_confirmation_seconds: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        completed = self.completed
        counting_start_height = self.counting_start_height
        chain = self.chain
        external_observed_height = self.external_observed_height
        external_confirmation_delay_height = self.external_confirmation_delay_height
        remaining_confirmation_seconds = self.remaining_confirmation_seconds

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "completed": completed,
            }
        )
        if counting_start_height is not UNSET:
            field_dict["counting_start_height"] = counting_start_height
        if chain is not UNSET:
            field_dict["chain"] = chain
        if external_observed_height is not UNSET:
            field_dict["external_observed_height"] = external_observed_height
        if external_confirmation_delay_height is not UNSET:
            field_dict["external_confirmation_delay_height"] = external_confirmation_delay_height
        if remaining_confirmation_seconds is not UNSET:
            field_dict["remaining_confirmation_seconds"] = remaining_confirmation_seconds

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        completed = d.pop("completed")

        counting_start_height = d.pop("counting_start_height", UNSET)

        chain = d.pop("chain", UNSET)

        external_observed_height = d.pop("external_observed_height", UNSET)

        external_confirmation_delay_height = d.pop("external_confirmation_delay_height", UNSET)

        remaining_confirmation_seconds = d.pop("remaining_confirmation_seconds", UNSET)

        tx_stages_response_inbound_confirmation_counted = cls(
            completed=completed,
            counting_start_height=counting_start_height,
            chain=chain,
            external_observed_height=external_observed_height,
            external_confirmation_delay_height=external_confirmation_delay_height,
            remaining_confirmation_seconds=remaining_confirmation_seconds,
        )

        tx_stages_response_inbound_confirmation_counted.additional_properties = d
        return tx_stages_response_inbound_confirmation_counted

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
