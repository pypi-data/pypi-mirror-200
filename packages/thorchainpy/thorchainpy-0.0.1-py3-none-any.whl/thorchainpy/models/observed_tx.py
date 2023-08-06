from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.observed_tx_status import ObservedTxStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.tx import Tx


T = TypeVar("T", bound="ObservedTx")


@attr.s(auto_attribs=True)
class ObservedTx:
    """
    Attributes:
        tx (Tx):
        status (Union[Unset, ObservedTxStatus]):  Example: done.
        out_hashes (Union[Unset, List[str]]):
        block_height (Union[Unset, int]): same as external_observed_height, to be deprecated in favour of
            external_observed_height Example: 7581334.
        external_observed_height (Union[Unset, int]): the block height on the external source chain when the transaction
            was observed, not provided if chain is THOR Example: 7581334.
        signers (Union[Unset, List[str]]):
        observed_pub_key (Union[Unset, str]):  Example:
            thorpub1addwnpepq27ck6u44zl8qqdnmzjjc8rg72amrxrsp42p9vd7kt6marhy6ww76z8shwe.
        keysign_ms (Union[Unset, int]):  Example: 10000.
        finalise_height (Union[Unset, int]): same as external_confirmation_delay_height, to be deprecated in favour of
            external_confirmation_delay_height Example: 7581334.
        external_confirmation_delay_height (Union[Unset, int]): the block height on the external source chain when
            confirmation counting will be complete, not provided if chain is THOR Example: 7581334.
        aggregator (Union[Unset, str]): the outbound aggregator to use, will also match a suffix Example:
            0x69800327b38A4CeF30367Dec3f64c2f2386f3848.
        aggregator_target (Union[Unset, str]): the aggregator target asset provided to transferOutAndCall Example:
            0x0a44986b70527154e9F4290eC14e5f0D1C861822.
        aggregator_target_limit (Union[Unset, str]): the aggregator target asset limit provided to transferOutAndCall
            Example: 0x0a44986b70527154e9F4290eC14e5f0D1C861822.
    """

    tx: "Tx"
    status: Union[Unset, ObservedTxStatus] = UNSET
    out_hashes: Union[Unset, List[str]] = UNSET
    block_height: Union[Unset, int] = UNSET
    external_observed_height: Union[Unset, int] = UNSET
    signers: Union[Unset, List[str]] = UNSET
    observed_pub_key: Union[Unset, str] = UNSET
    keysign_ms: Union[Unset, int] = UNSET
    finalise_height: Union[Unset, int] = UNSET
    external_confirmation_delay_height: Union[Unset, int] = UNSET
    aggregator: Union[Unset, str] = UNSET
    aggregator_target: Union[Unset, str] = UNSET
    aggregator_target_limit: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        tx = self.tx.to_dict()

        status: Union[Unset, str] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        out_hashes: Union[Unset, List[str]] = UNSET
        if not isinstance(self.out_hashes, Unset):
            out_hashes = self.out_hashes

        block_height = self.block_height
        external_observed_height = self.external_observed_height
        signers: Union[Unset, List[str]] = UNSET
        if not isinstance(self.signers, Unset):
            signers = self.signers

        observed_pub_key = self.observed_pub_key
        keysign_ms = self.keysign_ms
        finalise_height = self.finalise_height
        external_confirmation_delay_height = self.external_confirmation_delay_height
        aggregator = self.aggregator
        aggregator_target = self.aggregator_target
        aggregator_target_limit = self.aggregator_target_limit

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "tx": tx,
            }
        )
        if status is not UNSET:
            field_dict["status"] = status
        if out_hashes is not UNSET:
            field_dict["out_hashes"] = out_hashes
        if block_height is not UNSET:
            field_dict["block_height"] = block_height
        if external_observed_height is not UNSET:
            field_dict["external_observed_height"] = external_observed_height
        if signers is not UNSET:
            field_dict["signers"] = signers
        if observed_pub_key is not UNSET:
            field_dict["observed_pub_key"] = observed_pub_key
        if keysign_ms is not UNSET:
            field_dict["keysign_ms"] = keysign_ms
        if finalise_height is not UNSET:
            field_dict["finalise_height"] = finalise_height
        if external_confirmation_delay_height is not UNSET:
            field_dict["external_confirmation_delay_height"] = external_confirmation_delay_height
        if aggregator is not UNSET:
            field_dict["aggregator"] = aggregator
        if aggregator_target is not UNSET:
            field_dict["aggregator_target"] = aggregator_target
        if aggregator_target_limit is not UNSET:
            field_dict["aggregator_target_limit"] = aggregator_target_limit

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.tx import Tx

        d = src_dict.copy()
        tx = Tx.from_dict(d.pop("tx"))

        _status = d.pop("status", UNSET)
        status: Union[Unset, ObservedTxStatus]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = ObservedTxStatus(_status)

        out_hashes = cast(List[str], d.pop("out_hashes", UNSET))

        block_height = d.pop("block_height", UNSET)

        external_observed_height = d.pop("external_observed_height", UNSET)

        signers = cast(List[str], d.pop("signers", UNSET))

        observed_pub_key = d.pop("observed_pub_key", UNSET)

        keysign_ms = d.pop("keysign_ms", UNSET)

        finalise_height = d.pop("finalise_height", UNSET)

        external_confirmation_delay_height = d.pop("external_confirmation_delay_height", UNSET)

        aggregator = d.pop("aggregator", UNSET)

        aggregator_target = d.pop("aggregator_target", UNSET)

        aggregator_target_limit = d.pop("aggregator_target_limit", UNSET)

        observed_tx = cls(
            tx=tx,
            status=status,
            out_hashes=out_hashes,
            block_height=block_height,
            external_observed_height=external_observed_height,
            signers=signers,
            observed_pub_key=observed_pub_key,
            keysign_ms=keysign_ms,
            finalise_height=finalise_height,
            external_confirmation_delay_height=external_confirmation_delay_height,
            aggregator=aggregator,
            aggregator_target=aggregator_target,
            aggregator_target_limit=aggregator_target_limit,
        )

        observed_tx.additional_properties = d
        return observed_tx

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
