from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.quote_fees import QuoteFees


T = TypeVar("T", bound="QuoteSaverDepositResponse")


@attr.s(auto_attribs=True)
class QuoteSaverDepositResponse:
    """
    Attributes:
        inbound_address (str): the inbound address for the transaction on the source chain Example:
            bc1qjk3xzu5slu7mtmc8jc9yed3zqvkhkttm700g9a.
        memo (str): generated memo for the deposit Example: +:ETH/ETH::thor17gw75axcnr8747pkanye45pnrwk7p9c3cqncsv:100.
        expected_amount_out (str): migrate to expected_amount_deposit (will be deprecated in v1.104) Example: 10000.
        fees (QuoteFees):
        slippage_bps (int): the swap slippage in basis points
        expiry (int): expiration timestamp in unix seconds Example: 1671660285.
        warning (str): static warning message Example: Do not cache this response. Do not send funds after the expiry..
        notes (str): chain specific quote notes Example: Transfer the inbound_address the asset with the memo. Do not
            use multi-in, multi-out transactions..
        expected_amount_deposit (Union[Unset, str]): the minimum amount of the target asset the user can expect to
            deposit after fees Example: 10000.
        inbound_confirmation_blocks (Union[Unset, int]): the approximate number of source chain blocks required before
            processing
        inbound_confirmation_seconds (Union[Unset, int]): the approximate seconds for block confirmations required
            before processing
        dust_threshold (Union[Unset, str]): Defines the minimum transaction size for the chain in base units (sats, wei,
            uatom). Transctions with asset amounts lower than the dust_threshold are ignored. Example: 10000.
    """

    inbound_address: str
    memo: str
    expected_amount_out: str
    fees: "QuoteFees"
    slippage_bps: int
    expiry: int
    warning: str
    notes: str
    expected_amount_deposit: Union[Unset, str] = UNSET
    inbound_confirmation_blocks: Union[Unset, int] = UNSET
    inbound_confirmation_seconds: Union[Unset, int] = UNSET
    dust_threshold: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        inbound_address = self.inbound_address
        memo = self.memo
        expected_amount_out = self.expected_amount_out
        fees = self.fees.to_dict()

        slippage_bps = self.slippage_bps
        expiry = self.expiry
        warning = self.warning
        notes = self.notes
        expected_amount_deposit = self.expected_amount_deposit
        inbound_confirmation_blocks = self.inbound_confirmation_blocks
        inbound_confirmation_seconds = self.inbound_confirmation_seconds
        dust_threshold = self.dust_threshold

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "inbound_address": inbound_address,
                "memo": memo,
                "expected_amount_out": expected_amount_out,
                "fees": fees,
                "slippage_bps": slippage_bps,
                "expiry": expiry,
                "warning": warning,
                "notes": notes,
            }
        )
        if expected_amount_deposit is not UNSET:
            field_dict["expected_amount_deposit"] = expected_amount_deposit
        if inbound_confirmation_blocks is not UNSET:
            field_dict["inbound_confirmation_blocks"] = inbound_confirmation_blocks
        if inbound_confirmation_seconds is not UNSET:
            field_dict["inbound_confirmation_seconds"] = inbound_confirmation_seconds
        if dust_threshold is not UNSET:
            field_dict["dust_threshold"] = dust_threshold

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.quote_fees import QuoteFees

        d = src_dict.copy()
        inbound_address = d.pop("inbound_address")

        memo = d.pop("memo")

        expected_amount_out = d.pop("expected_amount_out")

        fees = QuoteFees.from_dict(d.pop("fees"))

        slippage_bps = d.pop("slippage_bps")

        expiry = d.pop("expiry")

        warning = d.pop("warning")

        notes = d.pop("notes")

        expected_amount_deposit = d.pop("expected_amount_deposit", UNSET)

        inbound_confirmation_blocks = d.pop("inbound_confirmation_blocks", UNSET)

        inbound_confirmation_seconds = d.pop("inbound_confirmation_seconds", UNSET)

        dust_threshold = d.pop("dust_threshold", UNSET)

        quote_saver_deposit_response = cls(
            inbound_address=inbound_address,
            memo=memo,
            expected_amount_out=expected_amount_out,
            fees=fees,
            slippage_bps=slippage_bps,
            expiry=expiry,
            warning=warning,
            notes=notes,
            expected_amount_deposit=expected_amount_deposit,
            inbound_confirmation_blocks=inbound_confirmation_blocks,
            inbound_confirmation_seconds=inbound_confirmation_seconds,
            dust_threshold=dust_threshold,
        )

        quote_saver_deposit_response.additional_properties = d
        return quote_saver_deposit_response

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
