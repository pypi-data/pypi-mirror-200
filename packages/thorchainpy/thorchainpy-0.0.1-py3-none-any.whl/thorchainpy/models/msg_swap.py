from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.tx import Tx


T = TypeVar("T", bound="MsgSwap")


@attr.s(auto_attribs=True)
class MsgSwap:
    """
    Attributes:
        tx (Tx):
        target_asset (str): the asset to be swapped to Example: ETH.ETH.
        trade_target (str): the minimum amount of output asset to receive (else cancelling and refunding the swap)
        affiliate_basis_points (str): the affiliate fee in basis points
        destination (Union[Unset, str]): the destination address to receive the swap output Example:
            0x66fb1cd65b97fa40457b90b7d1ca6b92cb64b32b.
        affiliate_address (Union[Unset, str]): the affiliate address which will receive any affiliate fee Example:
            thor1f3s7q037eancht7sg0aj995dht25rwrnu4ats5.
        signer (Union[Unset, str]): the signer (sender) of the transaction
        aggregator (Union[Unset, str]): the contract address if an aggregator is specified for a non-THORChain SwapOut
        aggregator_target_address (Union[Unset, str]): the desired output asset of the aggregator SwapOut
        aggregator_target_limit (Union[Unset, str]): the minimum amount of SwapOut asset to receive (else cancelling the
            SwapOut and receiving THORChain's output)
        order_type (Union[Unset, int]): 0 if a market order (immediately completed or refunded), 1 if a limit order
            (held until fulfillable)
    """

    tx: "Tx"
    target_asset: str
    trade_target: str
    affiliate_basis_points: str
    destination: Union[Unset, str] = UNSET
    affiliate_address: Union[Unset, str] = UNSET
    signer: Union[Unset, str] = UNSET
    aggregator: Union[Unset, str] = UNSET
    aggregator_target_address: Union[Unset, str] = UNSET
    aggregator_target_limit: Union[Unset, str] = UNSET
    order_type: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        tx = self.tx.to_dict()

        target_asset = self.target_asset
        trade_target = self.trade_target
        affiliate_basis_points = self.affiliate_basis_points
        destination = self.destination
        affiliate_address = self.affiliate_address
        signer = self.signer
        aggregator = self.aggregator
        aggregator_target_address = self.aggregator_target_address
        aggregator_target_limit = self.aggregator_target_limit
        order_type = self.order_type

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "tx": tx,
                "target_asset": target_asset,
                "trade_target": trade_target,
                "affiliate_basis_points": affiliate_basis_points,
            }
        )
        if destination is not UNSET:
            field_dict["destination"] = destination
        if affiliate_address is not UNSET:
            field_dict["affiliate_address"] = affiliate_address
        if signer is not UNSET:
            field_dict["signer"] = signer
        if aggregator is not UNSET:
            field_dict["aggregator"] = aggregator
        if aggregator_target_address is not UNSET:
            field_dict["aggregator_target_address"] = aggregator_target_address
        if aggregator_target_limit is not UNSET:
            field_dict["aggregator_target_limit"] = aggregator_target_limit
        if order_type is not UNSET:
            field_dict["order_type"] = order_type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.tx import Tx

        d = src_dict.copy()
        tx = Tx.from_dict(d.pop("tx"))

        target_asset = d.pop("target_asset")

        trade_target = d.pop("trade_target")

        affiliate_basis_points = d.pop("affiliate_basis_points")

        destination = d.pop("destination", UNSET)

        affiliate_address = d.pop("affiliate_address", UNSET)

        signer = d.pop("signer", UNSET)

        aggregator = d.pop("aggregator", UNSET)

        aggregator_target_address = d.pop("aggregator_target_address", UNSET)

        aggregator_target_limit = d.pop("aggregator_target_limit", UNSET)

        order_type = d.pop("order_type", UNSET)

        msg_swap = cls(
            tx=tx,
            target_asset=target_asset,
            trade_target=trade_target,
            affiliate_basis_points=affiliate_basis_points,
            destination=destination,
            affiliate_address=affiliate_address,
            signer=signer,
            aggregator=aggregator,
            aggregator_target_address=aggregator_target_address,
            aggregator_target_limit=aggregator_target_limit,
            order_type=order_type,
        )

        msg_swap.additional_properties = d
        return msg_swap

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
