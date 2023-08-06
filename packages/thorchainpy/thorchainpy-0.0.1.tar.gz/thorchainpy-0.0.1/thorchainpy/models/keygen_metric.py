from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.keygen_metric_node_keygen_metric import KeygenMetricNodeKeygenMetric


T = TypeVar("T", bound="KeygenMetric")


@attr.s(auto_attribs=True)
class KeygenMetric:
    """
    Attributes:
        node_tss_times (List['KeygenMetricNodeKeygenMetric']):
        pub_key (Union[Unset, str]):
    """

    node_tss_times: List["KeygenMetricNodeKeygenMetric"]
    pub_key: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        node_tss_times = []
        for node_tss_times_item_data in self.node_tss_times:
            node_tss_times_item = node_tss_times_item_data.to_dict()

            node_tss_times.append(node_tss_times_item)

        pub_key = self.pub_key

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "node_tss_times": node_tss_times,
            }
        )
        if pub_key is not UNSET:
            field_dict["pub_key"] = pub_key

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.keygen_metric_node_keygen_metric import KeygenMetricNodeKeygenMetric

        d = src_dict.copy()
        node_tss_times = []
        _node_tss_times = d.pop("node_tss_times")
        for node_tss_times_item_data in _node_tss_times:
            node_tss_times_item = KeygenMetricNodeKeygenMetric.from_dict(node_tss_times_item_data)

            node_tss_times.append(node_tss_times_item)

        pub_key = d.pop("pub_key", UNSET)

        keygen_metric = cls(
            node_tss_times=node_tss_times,
            pub_key=pub_key,
        )

        keygen_metric.additional_properties = d
        return keygen_metric

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
