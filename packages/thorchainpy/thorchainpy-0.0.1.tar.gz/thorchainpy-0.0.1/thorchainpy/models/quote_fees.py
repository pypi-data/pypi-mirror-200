from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="QuoteFees")


@attr.s(auto_attribs=True)
class QuoteFees:
    """
    Attributes:
        asset (str):  Example: ETH.ETH.
        affiliate (str):  Example: 1234.
        outbound (str):  Example: 1234.
    """

    asset: str
    affiliate: str
    outbound: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        asset = self.asset
        affiliate = self.affiliate
        outbound = self.outbound

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "asset": asset,
                "affiliate": affiliate,
                "outbound": outbound,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        asset = d.pop("asset")

        affiliate = d.pop("affiliate")

        outbound = d.pop("outbound")

        quote_fees = cls(
            asset=asset,
            affiliate=affiliate,
            outbound=outbound,
        )

        quote_fees.additional_properties = d
        return quote_fees

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
