from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.tx import Tx
    from ..models.tx_stages_response import TxStagesResponse
    from ..models.tx_status_response_planned_out_txs_item import TxStatusResponsePlannedOutTxsItem


T = TypeVar("T", bound="TxStatusResponse")


@attr.s(auto_attribs=True)
class TxStatusResponse:
    """
    Attributes:
        stages (TxStagesResponse):
        tx (Union[Unset, Tx]):
        planned_out_txs (Union[Unset, List['TxStatusResponsePlannedOutTxsItem']]):
        out_txs (Union[Unset, List['Tx']]):
    """

    stages: "TxStagesResponse"
    tx: Union[Unset, "Tx"] = UNSET
    planned_out_txs: Union[Unset, List["TxStatusResponsePlannedOutTxsItem"]] = UNSET
    out_txs: Union[Unset, List["Tx"]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        stages = self.stages.to_dict()

        tx: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.tx, Unset):
            tx = self.tx.to_dict()

        planned_out_txs: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.planned_out_txs, Unset):
            planned_out_txs = []
            for planned_out_txs_item_data in self.planned_out_txs:
                planned_out_txs_item = planned_out_txs_item_data.to_dict()

                planned_out_txs.append(planned_out_txs_item)

        out_txs: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.out_txs, Unset):
            out_txs = []
            for out_txs_item_data in self.out_txs:
                out_txs_item = out_txs_item_data.to_dict()

                out_txs.append(out_txs_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "stages": stages,
            }
        )
        if tx is not UNSET:
            field_dict["tx"] = tx
        if planned_out_txs is not UNSET:
            field_dict["planned_out_txs"] = planned_out_txs
        if out_txs is not UNSET:
            field_dict["out_txs"] = out_txs

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.tx import Tx
        from ..models.tx_stages_response import TxStagesResponse
        from ..models.tx_status_response_planned_out_txs_item import TxStatusResponsePlannedOutTxsItem

        d = src_dict.copy()
        stages = TxStagesResponse.from_dict(d.pop("stages"))

        _tx = d.pop("tx", UNSET)
        tx: Union[Unset, Tx]
        if isinstance(_tx, Unset):
            tx = UNSET
        else:
            tx = Tx.from_dict(_tx)

        planned_out_txs = []
        _planned_out_txs = d.pop("planned_out_txs", UNSET)
        for planned_out_txs_item_data in _planned_out_txs or []:
            planned_out_txs_item = TxStatusResponsePlannedOutTxsItem.from_dict(planned_out_txs_item_data)

            planned_out_txs.append(planned_out_txs_item)

        out_txs = []
        _out_txs = d.pop("out_txs", UNSET)
        for out_txs_item_data in _out_txs or []:
            out_txs_item = Tx.from_dict(out_txs_item_data)

            out_txs.append(out_txs_item)

        tx_status_response = cls(
            stages=stages,
            tx=tx,
            planned_out_txs=planned_out_txs,
            out_txs=out_txs,
        )

        tx_status_response.additional_properties = d
        return tx_status_response

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
