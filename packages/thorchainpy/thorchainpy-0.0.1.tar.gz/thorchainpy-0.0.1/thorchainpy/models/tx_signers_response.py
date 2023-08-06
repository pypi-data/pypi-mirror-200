from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.observed_tx import ObservedTx
    from ..models.tx import Tx
    from ..models.tx_out_item import TxOutItem


T = TypeVar("T", bound="TxSignersResponse")


@attr.s(auto_attribs=True)
class TxSignersResponse:
    """
    Attributes:
        tx (ObservedTx):
        txs (List['ObservedTx']):
        actions (List['TxOutItem']):
        out_txs (List['Tx']):
        tx_id (Union[Unset, str]):  Example: CF524818D42B63D25BBA0CCC4909F127CAA645C0F9CD07324F2824CC151A64C7.
        height (Union[Unset, int]):  Example: 1234.
        finalised_height (Union[Unset, int]): the thorchain height at which the outbound was finalised Example: 7581334.
        updated_vault (Union[Unset, bool]):
        reverted (Union[Unset, bool]):
        outbound_height (Union[Unset, int]): the thorchain height for which the outbound was scheduled Example: 1234.
    """

    tx: "ObservedTx"
    txs: List["ObservedTx"]
    actions: List["TxOutItem"]
    out_txs: List["Tx"]
    tx_id: Union[Unset, str] = UNSET
    height: Union[Unset, int] = UNSET
    finalised_height: Union[Unset, int] = UNSET
    updated_vault: Union[Unset, bool] = UNSET
    reverted: Union[Unset, bool] = UNSET
    outbound_height: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        tx = self.tx.to_dict()

        txs = []
        for txs_item_data in self.txs:
            txs_item = txs_item_data.to_dict()

            txs.append(txs_item)

        actions = []
        for actions_item_data in self.actions:
            actions_item = actions_item_data.to_dict()

            actions.append(actions_item)

        out_txs = []
        for out_txs_item_data in self.out_txs:
            out_txs_item = out_txs_item_data.to_dict()

            out_txs.append(out_txs_item)

        tx_id = self.tx_id
        height = self.height
        finalised_height = self.finalised_height
        updated_vault = self.updated_vault
        reverted = self.reverted
        outbound_height = self.outbound_height

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "tx": tx,
                "txs": txs,
                "actions": actions,
                "out_txs": out_txs,
            }
        )
        if tx_id is not UNSET:
            field_dict["tx_id"] = tx_id
        if height is not UNSET:
            field_dict["height"] = height
        if finalised_height is not UNSET:
            field_dict["finalised_height"] = finalised_height
        if updated_vault is not UNSET:
            field_dict["updated_vault"] = updated_vault
        if reverted is not UNSET:
            field_dict["reverted"] = reverted
        if outbound_height is not UNSET:
            field_dict["outbound_height"] = outbound_height

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.observed_tx import ObservedTx
        from ..models.tx import Tx
        from ..models.tx_out_item import TxOutItem

        d = src_dict.copy()
        tx = ObservedTx.from_dict(d.pop("tx"))

        txs = []
        _txs = d.pop("txs")
        for txs_item_data in _txs:
            txs_item = ObservedTx.from_dict(txs_item_data)

            txs.append(txs_item)

        actions = []
        _actions = d.pop("actions")
        for actions_item_data in _actions:
            actions_item = TxOutItem.from_dict(actions_item_data)

            actions.append(actions_item)

        out_txs = []
        _out_txs = d.pop("out_txs")
        for out_txs_item_data in _out_txs:
            out_txs_item = Tx.from_dict(out_txs_item_data)

            out_txs.append(out_txs_item)

        tx_id = d.pop("tx_id", UNSET)

        height = d.pop("height", UNSET)

        finalised_height = d.pop("finalised_height", UNSET)

        updated_vault = d.pop("updated_vault", UNSET)

        reverted = d.pop("reverted", UNSET)

        outbound_height = d.pop("outbound_height", UNSET)

        tx_signers_response = cls(
            tx=tx,
            txs=txs,
            actions=actions,
            out_txs=out_txs,
            tx_id=tx_id,
            height=height,
            finalised_height=finalised_height,
            updated_vault=updated_vault,
            reverted=reverted,
            outbound_height=outbound_height,
        )

        tx_signers_response.additional_properties = d
        return tx_signers_response

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
