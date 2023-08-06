from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.tss_metric import TssMetric


T = TypeVar("T", bound="TssKeysignMetric")


@attr.s(auto_attribs=True)
class TssKeysignMetric:
    """
    Attributes:
        node_tss_times (List['TssMetric']):
        tx_id (Union[Unset, str]):
    """

    node_tss_times: List["TssMetric"]
    tx_id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        node_tss_times = []
        for node_tss_times_item_data in self.node_tss_times:
            node_tss_times_item = node_tss_times_item_data.to_dict()

            node_tss_times.append(node_tss_times_item)

        tx_id = self.tx_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "node_tss_times": node_tss_times,
            }
        )
        if tx_id is not UNSET:
            field_dict["tx_id"] = tx_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.tss_metric import TssMetric

        d = src_dict.copy()
        node_tss_times = []
        _node_tss_times = d.pop("node_tss_times")
        for node_tss_times_item_data in _node_tss_times:
            node_tss_times_item = TssMetric.from_dict(node_tss_times_item_data)

            node_tss_times.append(node_tss_times_item)

        tx_id = d.pop("tx_id", UNSET)

        tss_keysign_metric = cls(
            node_tss_times=node_tss_times,
            tx_id=tx_id,
        )

        tss_keysign_metric.additional_properties = d
        return tss_keysign_metric

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
