from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.tx_out_item import TxOutItem


T = TypeVar("T", bound="KeysignResponseKeysignInfo")


@attr.s(auto_attribs=True)
class KeysignResponseKeysignInfo:
    """
    Attributes:
        tx_array (List['TxOutItem']):
        height (Union[Unset, int]): the block(s) in which a tx out item is scheduled to be signed and moved from the
            scheduled outbound queue to the outbound queue
    """

    tx_array: List["TxOutItem"]
    height: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        tx_array = []
        for tx_array_item_data in self.tx_array:
            tx_array_item = tx_array_item_data.to_dict()

            tx_array.append(tx_array_item)

        height = self.height

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "tx_array": tx_array,
            }
        )
        if height is not UNSET:
            field_dict["height"] = height

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.tx_out_item import TxOutItem

        d = src_dict.copy()
        tx_array = []
        _tx_array = d.pop("tx_array")
        for tx_array_item_data in _tx_array:
            tx_array_item = TxOutItem.from_dict(tx_array_item_data)

            tx_array.append(tx_array_item)

        height = d.pop("height", UNSET)

        keysign_response_keysign_info = cls(
            tx_array=tx_array,
            height=height,
        )

        keysign_response_keysign_info.additional_properties = d
        return keysign_response_keysign_info

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
