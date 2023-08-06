from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.constants_response_bool_values import ConstantsResponseBoolValues
    from ..models.constants_response_int_64_values import ConstantsResponseInt64Values
    from ..models.constants_response_string_values import ConstantsResponseStringValues


T = TypeVar("T", bound="ConstantsResponse")


@attr.s(auto_attribs=True)
class ConstantsResponse:
    """
    Attributes:
        int_64_values (Union[Unset, ConstantsResponseInt64Values]):  Example: {'AsgardSize': 40}.
        bool_values (Union[Unset, ConstantsResponseBoolValues]):  Example: {'StrictBondLiquidityRatio': True}.
        string_values (Union[Unset, ConstantsResponseStringValues]):  Example: {'DefaultPoolStatus': 'Staged'}.
    """

    int_64_values: Union[Unset, "ConstantsResponseInt64Values"] = UNSET
    bool_values: Union[Unset, "ConstantsResponseBoolValues"] = UNSET
    string_values: Union[Unset, "ConstantsResponseStringValues"] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        int_64_values: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.int_64_values, Unset):
            int_64_values = self.int_64_values.to_dict()

        bool_values: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.bool_values, Unset):
            bool_values = self.bool_values.to_dict()

        string_values: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.string_values, Unset):
            string_values = self.string_values.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if int_64_values is not UNSET:
            field_dict["int_64_values"] = int_64_values
        if bool_values is not UNSET:
            field_dict["bool_values"] = bool_values
        if string_values is not UNSET:
            field_dict["string_values"] = string_values

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.constants_response_bool_values import ConstantsResponseBoolValues
        from ..models.constants_response_int_64_values import ConstantsResponseInt64Values
        from ..models.constants_response_string_values import ConstantsResponseStringValues

        d = src_dict.copy()
        _int_64_values = d.pop("int_64_values", UNSET)
        int_64_values: Union[Unset, ConstantsResponseInt64Values]
        if isinstance(_int_64_values, Unset):
            int_64_values = UNSET
        else:
            int_64_values = ConstantsResponseInt64Values.from_dict(_int_64_values)

        _bool_values = d.pop("bool_values", UNSET)
        bool_values: Union[Unset, ConstantsResponseBoolValues]
        if isinstance(_bool_values, Unset):
            bool_values = UNSET
        else:
            bool_values = ConstantsResponseBoolValues.from_dict(_bool_values)

        _string_values = d.pop("string_values", UNSET)
        string_values: Union[Unset, ConstantsResponseStringValues]
        if isinstance(_string_values, Unset):
            string_values = UNSET
        else:
            string_values = ConstantsResponseStringValues.from_dict(_string_values)

        constants_response = cls(
            int_64_values=int_64_values,
            bool_values=bool_values,
            string_values=string_values,
        )

        constants_response.additional_properties = d
        return constants_response

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
