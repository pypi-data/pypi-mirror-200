from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.quote_fees import QuoteFees


T = TypeVar("T", bound="QuoteSwapResponse")


@attr.s(auto_attribs=True)
class QuoteSwapResponse:
    """
    Attributes:
        inbound_address (str): the inbound address for the transaction on the source chain Example:
            bc1qjk3xzu5slu7mtmc8jc9yed3zqvkhkttm700g9a.
        expected_amount_out (str): the minimum amount of the target asset the user can expect to receive after fees
            Example: 10000.
        outbound_delay_blocks (int): the number of thorchain blocks the outbound will be delayed
        outbound_delay_seconds (int): the approximate seconds for the outbound delay before it will be sent
        fees (QuoteFees):
        slippage_bps (int): the swap slippage in basis points
        expiry (int): expiration timestamp in unix seconds Example: 1671660285.
        warning (str): static warning message Example: Do not cache this response. Do not send funds after the expiry..
        notes (str): chain specific quote notes Example: Transfer the inbound_address the asset with the memo. Do not
            use multi-in, multi-out transactions..
        memo (Union[Unset, str]): generated memo for the swap Example:
            =:ETH.ETH:0x1c7b17362c84287bd1184447e6dfeaf920c31bbe:1440450000:thor17gw75axcnr8747pkanye45pnrwk7p9c3cqncsv:100.
        inbound_confirmation_blocks (Union[Unset, int]): the approximate number of source chain blocks required before
            processing
        inbound_confirmation_seconds (Union[Unset, int]): the approximate seconds for block confirmations required
            before processing
        router (Union[Unset, str]): the EVM chain router contract address Example:
            0x3624525075b88B24ecc29CE226b0CEc1fFcB6976.
        dust_threshold (Union[Unset, str]): Defines the minimum transaction size for the chain in base units (sats, wei,
            uatom). Transctions with asset amounts lower than the dust_threshold are ignored. Example: 10000.
    """

    inbound_address: str
    expected_amount_out: str
    outbound_delay_blocks: int
    outbound_delay_seconds: int
    fees: "QuoteFees"
    slippage_bps: int
    expiry: int
    warning: str
    notes: str
    memo: Union[Unset, str] = UNSET
    inbound_confirmation_blocks: Union[Unset, int] = UNSET
    inbound_confirmation_seconds: Union[Unset, int] = UNSET
    router: Union[Unset, str] = UNSET
    dust_threshold: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        inbound_address = self.inbound_address
        expected_amount_out = self.expected_amount_out
        outbound_delay_blocks = self.outbound_delay_blocks
        outbound_delay_seconds = self.outbound_delay_seconds
        fees = self.fees.to_dict()

        slippage_bps = self.slippage_bps
        expiry = self.expiry
        warning = self.warning
        notes = self.notes
        memo = self.memo
        inbound_confirmation_blocks = self.inbound_confirmation_blocks
        inbound_confirmation_seconds = self.inbound_confirmation_seconds
        router = self.router
        dust_threshold = self.dust_threshold

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "inbound_address": inbound_address,
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
        if memo is not UNSET:
            field_dict["memo"] = memo
        if inbound_confirmation_blocks is not UNSET:
            field_dict["inbound_confirmation_blocks"] = inbound_confirmation_blocks
        if inbound_confirmation_seconds is not UNSET:
            field_dict["inbound_confirmation_seconds"] = inbound_confirmation_seconds
        if router is not UNSET:
            field_dict["router"] = router
        if dust_threshold is not UNSET:
            field_dict["dust_threshold"] = dust_threshold

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.quote_fees import QuoteFees

        d = src_dict.copy()
        inbound_address = d.pop("inbound_address")

        expected_amount_out = d.pop("expected_amount_out")

        outbound_delay_blocks = d.pop("outbound_delay_blocks")

        outbound_delay_seconds = d.pop("outbound_delay_seconds")

        fees = QuoteFees.from_dict(d.pop("fees"))

        slippage_bps = d.pop("slippage_bps")

        expiry = d.pop("expiry")

        warning = d.pop("warning")

        notes = d.pop("notes")

        memo = d.pop("memo", UNSET)

        inbound_confirmation_blocks = d.pop("inbound_confirmation_blocks", UNSET)

        inbound_confirmation_seconds = d.pop("inbound_confirmation_seconds", UNSET)

        router = d.pop("router", UNSET)

        dust_threshold = d.pop("dust_threshold", UNSET)

        quote_swap_response = cls(
            inbound_address=inbound_address,
            expected_amount_out=expected_amount_out,
            outbound_delay_blocks=outbound_delay_blocks,
            outbound_delay_seconds=outbound_delay_seconds,
            fees=fees,
            slippage_bps=slippage_bps,
            expiry=expiry,
            warning=warning,
            notes=notes,
            memo=memo,
            inbound_confirmation_blocks=inbound_confirmation_blocks,
            inbound_confirmation_seconds=inbound_confirmation_seconds,
            router=router,
            dust_threshold=dust_threshold,
        )

        quote_swap_response.additional_properties = d
        return quote_swap_response

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
