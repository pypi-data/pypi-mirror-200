from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.node_node_bond_providers_node_bond_provider import NodeNodeBondProvidersNodeBondProvider


T = TypeVar("T", bound="NodeNodeBondProviders")


@attr.s(auto_attribs=True)
class NodeNodeBondProviders:
    """
    Attributes:
        node_operator_fee (Union[Unset, str]): node operator fee in basis points
        providers (Union[Unset, NodeNodeBondProvidersNodeBondProvider]):
    """

    node_operator_fee: Union[Unset, str] = UNSET
    providers: Union[Unset, "NodeNodeBondProvidersNodeBondProvider"] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        node_operator_fee = self.node_operator_fee
        providers: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.providers, Unset):
            providers = self.providers.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if node_operator_fee is not UNSET:
            field_dict["node_operator_fee"] = node_operator_fee
        if providers is not UNSET:
            field_dict["providers"] = providers

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.node_node_bond_providers_node_bond_provider import NodeNodeBondProvidersNodeBondProvider

        d = src_dict.copy()
        node_operator_fee = d.pop("node_operator_fee", UNSET)

        _providers = d.pop("providers", UNSET)
        providers: Union[Unset, NodeNodeBondProvidersNodeBondProvider]
        if isinstance(_providers, Unset):
            providers = UNSET
        else:
            providers = NodeNodeBondProvidersNodeBondProvider.from_dict(_providers)

        node_node_bond_providers = cls(
            node_operator_fee=node_operator_fee,
            providers=providers,
        )

        node_node_bond_providers.additional_properties = d
        return node_node_bond_providers

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
