from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.tx_stages_response_inbound_confirmation_counted import TxStagesResponseInboundConfirmationCounted
    from ..models.tx_stages_response_inbound_finalised import TxStagesResponseInboundFinalised
    from ..models.tx_stages_response_inbound_observed import TxStagesResponseInboundObserved
    from ..models.tx_stages_response_outbound_delay import TxStagesResponseOutboundDelay
    from ..models.tx_stages_response_outbound_signed import TxStagesResponseOutboundSigned
    from ..models.tx_stages_response_swap_finalised import TxStagesResponseSwapFinalised


T = TypeVar("T", bound="TxStagesResponse")


@attr.s(auto_attribs=True)
class TxStagesResponse:
    """
    Attributes:
        inbound_observed (TxStagesResponseInboundObserved):
        inbound_finalised (TxStagesResponseInboundFinalised):
        inbound_confirmation_counted (Union[Unset, TxStagesResponseInboundConfirmationCounted]):
        swap_finalised (Union[Unset, TxStagesResponseSwapFinalised]):
        outbound_delay (Union[Unset, TxStagesResponseOutboundDelay]):
        outbound_signed (Union[Unset, TxStagesResponseOutboundSigned]):
    """

    inbound_observed: "TxStagesResponseInboundObserved"
    inbound_finalised: "TxStagesResponseInboundFinalised"
    inbound_confirmation_counted: Union[Unset, "TxStagesResponseInboundConfirmationCounted"] = UNSET
    swap_finalised: Union[Unset, "TxStagesResponseSwapFinalised"] = UNSET
    outbound_delay: Union[Unset, "TxStagesResponseOutboundDelay"] = UNSET
    outbound_signed: Union[Unset, "TxStagesResponseOutboundSigned"] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        inbound_observed = self.inbound_observed.to_dict()

        inbound_finalised = self.inbound_finalised.to_dict()

        inbound_confirmation_counted: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.inbound_confirmation_counted, Unset):
            inbound_confirmation_counted = self.inbound_confirmation_counted.to_dict()

        swap_finalised: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.swap_finalised, Unset):
            swap_finalised = self.swap_finalised.to_dict()

        outbound_delay: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.outbound_delay, Unset):
            outbound_delay = self.outbound_delay.to_dict()

        outbound_signed: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.outbound_signed, Unset):
            outbound_signed = self.outbound_signed.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "inbound_observed": inbound_observed,
                "inbound_finalised": inbound_finalised,
            }
        )
        if inbound_confirmation_counted is not UNSET:
            field_dict["inbound_confirmation_counted"] = inbound_confirmation_counted
        if swap_finalised is not UNSET:
            field_dict["swap_finalised"] = swap_finalised
        if outbound_delay is not UNSET:
            field_dict["outbound_delay"] = outbound_delay
        if outbound_signed is not UNSET:
            field_dict["outbound_signed"] = outbound_signed

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.tx_stages_response_inbound_confirmation_counted import TxStagesResponseInboundConfirmationCounted
        from ..models.tx_stages_response_inbound_finalised import TxStagesResponseInboundFinalised
        from ..models.tx_stages_response_inbound_observed import TxStagesResponseInboundObserved
        from ..models.tx_stages_response_outbound_delay import TxStagesResponseOutboundDelay
        from ..models.tx_stages_response_outbound_signed import TxStagesResponseOutboundSigned
        from ..models.tx_stages_response_swap_finalised import TxStagesResponseSwapFinalised

        d = src_dict.copy()
        inbound_observed = TxStagesResponseInboundObserved.from_dict(d.pop("inbound_observed"))

        inbound_finalised = TxStagesResponseInboundFinalised.from_dict(d.pop("inbound_finalised"))

        _inbound_confirmation_counted = d.pop("inbound_confirmation_counted", UNSET)
        inbound_confirmation_counted: Union[Unset, TxStagesResponseInboundConfirmationCounted]
        if isinstance(_inbound_confirmation_counted, Unset):
            inbound_confirmation_counted = UNSET
        else:
            inbound_confirmation_counted = TxStagesResponseInboundConfirmationCounted.from_dict(
                _inbound_confirmation_counted
            )

        _swap_finalised = d.pop("swap_finalised", UNSET)
        swap_finalised: Union[Unset, TxStagesResponseSwapFinalised]
        if isinstance(_swap_finalised, Unset):
            swap_finalised = UNSET
        else:
            swap_finalised = TxStagesResponseSwapFinalised.from_dict(_swap_finalised)

        _outbound_delay = d.pop("outbound_delay", UNSET)
        outbound_delay: Union[Unset, TxStagesResponseOutboundDelay]
        if isinstance(_outbound_delay, Unset):
            outbound_delay = UNSET
        else:
            outbound_delay = TxStagesResponseOutboundDelay.from_dict(_outbound_delay)

        _outbound_signed = d.pop("outbound_signed", UNSET)
        outbound_signed: Union[Unset, TxStagesResponseOutboundSigned]
        if isinstance(_outbound_signed, Unset):
            outbound_signed = UNSET
        else:
            outbound_signed = TxStagesResponseOutboundSigned.from_dict(_outbound_signed)

        tx_stages_response = cls(
            inbound_observed=inbound_observed,
            inbound_finalised=inbound_finalised,
            inbound_confirmation_counted=inbound_confirmation_counted,
            swap_finalised=swap_finalised,
            outbound_delay=outbound_delay,
            outbound_signed=outbound_signed,
        )

        tx_stages_response.additional_properties = d
        return tx_stages_response

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
