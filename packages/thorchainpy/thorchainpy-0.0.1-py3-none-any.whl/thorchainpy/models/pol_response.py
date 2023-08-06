from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="POLResponse")


@attr.s(auto_attribs=True)
class POLResponse:
    """
    Attributes:
        rune_deposited (str): total amount of RUNE deposited into the pools Example: 857134475040.
        rune_withdrawn (str): total amount of RUNE withdrawn from the pools Example: 0.
        value (str): total value of protocol's LP position in RUNE value Example: 21999180112172346.
        pnl (str): profit and loss of protocol owned liquidity Example: 21999180112172346.
        current_deposit (str): current amount of rune deposited Example: 21999180112172346.
    """

    rune_deposited: str
    rune_withdrawn: str
    value: str
    pnl: str
    current_deposit: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        rune_deposited = self.rune_deposited
        rune_withdrawn = self.rune_withdrawn
        value = self.value
        pnl = self.pnl
        current_deposit = self.current_deposit

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "rune_deposited": rune_deposited,
                "rune_withdrawn": rune_withdrawn,
                "value": value,
                "pnl": pnl,
                "current_deposit": current_deposit,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        rune_deposited = d.pop("rune_deposited")

        rune_withdrawn = d.pop("rune_withdrawn")

        value = d.pop("value")

        pnl = d.pop("pnl")

        current_deposit = d.pop("current_deposit")

        pol_response = cls(
            rune_deposited=rune_deposited,
            rune_withdrawn=rune_withdrawn,
            value=value,
            pnl=pnl,
            current_deposit=current_deposit,
        )

        pol_response.additional_properties = d
        return pol_response

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
