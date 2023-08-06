from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.observed_tx import ObservedTx
    from ..models.tss_keysign_metric import TssKeysignMetric


T = TypeVar("T", bound="TxResponse")


@attr.s(auto_attribs=True)
class TxResponse:
    """
    Attributes:
        observed_tx (Union[Unset, ObservedTx]):
        finalised_height (Union[Unset, int]): the thorchain height at which the outbound was finalised Example: 7581334.
        outbound_height (Union[Unset, int]): the thorchain height for which the outbound was scheduled Example: 1234.
        keysign_metric (Union[Unset, TssKeysignMetric]):
    """

    observed_tx: Union[Unset, "ObservedTx"] = UNSET
    finalised_height: Union[Unset, int] = UNSET
    outbound_height: Union[Unset, int] = UNSET
    keysign_metric: Union[Unset, "TssKeysignMetric"] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        observed_tx: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.observed_tx, Unset):
            observed_tx = self.observed_tx.to_dict()

        finalised_height = self.finalised_height
        outbound_height = self.outbound_height
        keysign_metric: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.keysign_metric, Unset):
            keysign_metric = self.keysign_metric.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if observed_tx is not UNSET:
            field_dict["observed_tx"] = observed_tx
        if finalised_height is not UNSET:
            field_dict["finalised_height"] = finalised_height
        if outbound_height is not UNSET:
            field_dict["outbound_height"] = outbound_height
        if keysign_metric is not UNSET:
            field_dict["keysign_metric"] = keysign_metric

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.observed_tx import ObservedTx
        from ..models.tss_keysign_metric import TssKeysignMetric

        d = src_dict.copy()
        _observed_tx = d.pop("observed_tx", UNSET)
        observed_tx: Union[Unset, ObservedTx]
        if isinstance(_observed_tx, Unset):
            observed_tx = UNSET
        else:
            observed_tx = ObservedTx.from_dict(_observed_tx)

        finalised_height = d.pop("finalised_height", UNSET)

        outbound_height = d.pop("outbound_height", UNSET)

        _keysign_metric = d.pop("keysign_metric", UNSET)
        keysign_metric: Union[Unset, TssKeysignMetric]
        if isinstance(_keysign_metric, Unset):
            keysign_metric = UNSET
        else:
            keysign_metric = TssKeysignMetric.from_dict(_keysign_metric)

        tx_response = cls(
            observed_tx=observed_tx,
            finalised_height=finalised_height,
            outbound_height=outbound_height,
            keysign_metric=keysign_metric,
        )

        tx_response.additional_properties = d
        return tx_response

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
