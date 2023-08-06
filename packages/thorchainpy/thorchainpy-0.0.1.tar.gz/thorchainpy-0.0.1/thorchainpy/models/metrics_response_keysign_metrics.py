from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.tss_metric import TssMetric


T = TypeVar("T", bound="MetricsResponseKeysignMetrics")


@attr.s(auto_attribs=True)
class MetricsResponseKeysignMetrics:
    """
    Attributes:
        tx_id (Union[Unset, str]):
        node_tss_times (Union[Unset, List['TssMetric']]):
    """

    tx_id: Union[Unset, str] = UNSET
    node_tss_times: Union[Unset, List["TssMetric"]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        tx_id = self.tx_id
        node_tss_times: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.node_tss_times, Unset):
            node_tss_times = []
            for node_tss_times_item_data in self.node_tss_times:
                node_tss_times_item = node_tss_times_item_data.to_dict()

                node_tss_times.append(node_tss_times_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if tx_id is not UNSET:
            field_dict["tx_id"] = tx_id
        if node_tss_times is not UNSET:
            field_dict["node_tss_times"] = node_tss_times

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.tss_metric import TssMetric

        d = src_dict.copy()
        tx_id = d.pop("tx_id", UNSET)

        node_tss_times = []
        _node_tss_times = d.pop("node_tss_times", UNSET)
        for node_tss_times_item_data in _node_tss_times or []:
            node_tss_times_item = TssMetric.from_dict(node_tss_times_item_data)

            node_tss_times.append(node_tss_times_item)

        metrics_response_keysign_metrics = cls(
            tx_id=tx_id,
            node_tss_times=node_tss_times,
        )

        metrics_response_keysign_metrics.additional_properties = d
        return metrics_response_keysign_metrics

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
