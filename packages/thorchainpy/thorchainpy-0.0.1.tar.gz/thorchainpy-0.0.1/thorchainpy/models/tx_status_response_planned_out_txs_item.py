from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

import attr

if TYPE_CHECKING:
    from ..models.coin import Coin


T = TypeVar("T", bound="TxStatusResponsePlannedOutTxsItem")


@attr.s(auto_attribs=True)
class TxStatusResponsePlannedOutTxsItem:
    """
    Attributes:
        chain (str):  Example: BTC.
        to_address (str):  Example: bcrt1qf3s7q037eancht7sg0aj995dht25rwrnqsf45e.
        coin (Coin):
        refund (bool): returns true if the planned transaction has a refund memo
    """

    chain: str
    to_address: str
    coin: "Coin"
    refund: bool
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        chain = self.chain
        to_address = self.to_address
        coin = self.coin.to_dict()

        refund = self.refund

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "chain": chain,
                "to_address": to_address,
                "coin": coin,
                "refund": refund,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.coin import Coin

        d = src_dict.copy()
        chain = d.pop("chain")

        to_address = d.pop("to_address")

        coin = Coin.from_dict(d.pop("coin"))

        refund = d.pop("refund")

        tx_status_response_planned_out_txs_item = cls(
            chain=chain,
            to_address=to_address,
            coin=coin,
            refund=refund,
        )

        tx_status_response_planned_out_txs_item.additional_properties = d
        return tx_status_response_planned_out_txs_item

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
