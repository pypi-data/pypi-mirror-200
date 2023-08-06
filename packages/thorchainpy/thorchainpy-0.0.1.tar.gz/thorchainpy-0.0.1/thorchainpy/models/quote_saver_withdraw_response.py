from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.quote_fees import QuoteFees


T = TypeVar("T", bound="QuoteSaverWithdrawResponse")


@attr.s(auto_attribs=True)
class QuoteSaverWithdrawResponse:
    """
    Attributes:
        inbound_address (str): the inbound address for the transaction on the source chain Example:
            bc1qjk3xzu5slu7mtmc8jc9yed3zqvkhkttm700g9a.
        memo (str): generated memo for the withdraw, the client can use this OR send the dust amount Example:
            =:ETH.ETH:0x1c7b17362c84287bd1184447e6dfeaf920c31bbe:1440450000:thor17gw75axcnr8747pkanye45pnrwk7p9c3cqncsv:100.
        dust_amount (str): the dust amount of the target asset the user should send to initialize the withdraw, the
            client can send this OR provide the memo Example: 10000.
        expected_amount_out (str): the minimum amount of the target asset the user can expect to withdraw after fees in
            1e8 decimals Example: 10000.
        outbound_delay_blocks (int): the number of thorchain blocks the outbound will be delayed
        outbound_delay_seconds (int): the approximate seconds for the outbound delay before it will be sent
        fees (QuoteFees):
        slippage_bps (int): the swap slippage in basis points
        expiry (int): expiration timestamp in unix seconds Example: 1671660285.
        warning (str): static warning message Example: Do not cache this response. Do not send funds after the expiry..
        notes (str): chain specific quote notes Example: Transfer the inbound_address the asset with the memo. Do not
            use multi-in, multi-out transactions..
        dust_threshold (Union[Unset, str]): Defines the minimum transaction size for the chain in base units (sats, wei,
            uatom). Transctions with asset amounts lower than the dust_threshold are ignored. Example: 10000.
    """

    inbound_address: str
    memo: str
    dust_amount: str
    expected_amount_out: str
    outbound_delay_blocks: int
    outbound_delay_seconds: int
    fees: "QuoteFees"
    slippage_bps: int
    expiry: int
    warning: str
    notes: str
    dust_threshold: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        inbound_address = self.inbound_address
        memo = self.memo
        dust_amount = self.dust_amount
        expected_amount_out = self.expected_amount_out
        outbound_delay_blocks = self.outbound_delay_blocks
        outbound_delay_seconds = self.outbound_delay_seconds
        fees = self.fees.to_dict()

        slippage_bps = self.slippage_bps
        expiry = self.expiry
        warning = self.warning
        notes = self.notes
        dust_threshold = self.dust_threshold

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "inbound_address": inbound_address,
                "memo": memo,
                "dust_amount": dust_amount,
                "expected_amount_out": expected_amount_out,
                "outbound_delay_blocks": outbound_delay_blocks,
                "outbound_delay_seconds": outbound_delay_seconds,
                "fees": fees,
                "slippage_bps": slippage_bps,
                "expiry": expiry,
                "warning": warning,
                "notes": notes,
            }
        )
        if dust_threshold is not UNSET:
            field_dict["dust_threshold"] = dust_threshold

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.quote_fees import QuoteFees

        d = src_dict.copy()
        inbound_address = d.pop("inbound_address")

        memo = d.pop("memo")

        dust_amount = d.pop("dust_amount")

        expected_amount_out = d.pop("expected_amount_out")

        outbound_delay_blocks = d.pop("outbound_delay_blocks")

        outbound_delay_seconds = d.pop("outbound_delay_seconds")

        fees = QuoteFees.from_dict(d.pop("fees"))

        slippage_bps = d.pop("slippage_bps")

        expiry = d.pop("expiry")

        warning = d.pop("warning")

        notes = d.pop("notes")

        dust_threshold = d.pop("dust_threshold", UNSET)

        quote_saver_withdraw_response = cls(
            inbound_address=inbound_address,
            memo=memo,
            dust_amount=dust_amount,
            expected_amount_out=expected_amount_out,
            outbound_delay_blocks=outbound_delay_blocks,
            outbound_delay_seconds=outbound_delay_seconds,
            fees=fees,
            slippage_bps=slippage_bps,
            expiry=expiry,
            warning=warning,
            notes=notes,
            dust_threshold=dust_threshold,
        )

        quote_saver_withdraw_response.additional_properties = d
        return quote_saver_withdraw_response

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
