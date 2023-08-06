from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.keygen_metric import KeygenMetric
    from ..models.metrics_response_keysign_metrics import MetricsResponseKeysignMetrics


T = TypeVar("T", bound="MetricsResponse")


@attr.s(auto_attribs=True)
class MetricsResponse:
    """
    Attributes:
        keygen (Union[Unset, List['KeygenMetric']]):
        keysign (Union[Unset, MetricsResponseKeysignMetrics]):
    """

    keygen: Union[Unset, List["KeygenMetric"]] = UNSET
    keysign: Union[Unset, "MetricsResponseKeysignMetrics"] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        keygen: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.keygen, Unset):
            keygen = []
            for componentsschemas_keygen_metrics_response_item_data in self.keygen:
                componentsschemas_keygen_metrics_response_item = (
                    componentsschemas_keygen_metrics_response_item_data.to_dict()
                )

                keygen.append(componentsschemas_keygen_metrics_response_item)

        keysign: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.keysign, Unset):
            keysign = self.keysign.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if keygen is not UNSET:
            field_dict["keygen"] = keygen
        if keysign is not UNSET:
            field_dict["keysign"] = keysign

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.keygen_metric import KeygenMetric
        from ..models.metrics_response_keysign_metrics import MetricsResponseKeysignMetrics

        d = src_dict.copy()
        keygen = []
        _keygen = d.pop("keygen", UNSET)
        for componentsschemas_keygen_metrics_response_item_data in _keygen or []:
            componentsschemas_keygen_metrics_response_item = KeygenMetric.from_dict(
                componentsschemas_keygen_metrics_response_item_data
            )

            keygen.append(componentsschemas_keygen_metrics_response_item)

        _keysign = d.pop("keysign", UNSET)
        keysign: Union[Unset, MetricsResponseKeysignMetrics]
        if isinstance(_keysign, Unset):
            keysign = UNSET
        else:
            keysign = MetricsResponseKeysignMetrics.from_dict(_keysign)

        metrics_response = cls(
            keygen=keygen,
            keysign=keysign,
        )

        metrics_response.additional_properties = d
        return metrics_response

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
