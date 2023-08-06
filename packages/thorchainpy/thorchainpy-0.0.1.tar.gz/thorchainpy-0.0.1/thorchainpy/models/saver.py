from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="Saver")


@attr.s(auto_attribs=True)
class Saver:
    """
    Attributes:
        asset (str):  Example: BNB.BNB.
        asset_address (str):  Example: bnb1xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx.
        units (str):  Example: 0.
        asset_deposit_value (str):  Example: 0.
        asset_redeem_value (str):  Example: 0.
        growth_pct (str):  Example: 0.02.
        last_add_height (Union[Unset, int]):  Example: 82745.
        last_withdraw_height (Union[Unset, int]):  Example: 82745.
    """

    asset: str
    asset_address: str
    units: str
    asset_deposit_value: str
    asset_redeem_value: str
    growth_pct: str
    last_add_height: Union[Unset, int] = UNSET
    last_withdraw_height: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        asset = self.asset
        asset_address = self.asset_address
        units = self.units
        asset_deposit_value = self.asset_deposit_value
        asset_redeem_value = self.asset_redeem_value
        growth_pct = self.growth_pct
        last_add_height = self.last_add_height
        last_withdraw_height = self.last_withdraw_height

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "asset": asset,
                "asset_address": asset_address,
                "units": units,
                "asset_deposit_value": asset_deposit_value,
                "asset_redeem_value": asset_redeem_value,
                "growth_pct": growth_pct,
            }
        )
        if last_add_height is not UNSET:
            field_dict["last_add_height"] = last_add_height
        if last_withdraw_height is not UNSET:
            field_dict["last_withdraw_height"] = last_withdraw_height

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        asset = d.pop("asset")

        asset_address = d.pop("asset_address")

        units = d.pop("units")

        asset_deposit_value = d.pop("asset_deposit_value")

        asset_redeem_value = d.pop("asset_redeem_value")

        growth_pct = d.pop("growth_pct")

        last_add_height = d.pop("last_add_height", UNSET)

        last_withdraw_height = d.pop("last_withdraw_height", UNSET)

        saver = cls(
            asset=asset,
            asset_address=asset_address,
            units=units,
            asset_deposit_value=asset_deposit_value,
            asset_redeem_value=asset_redeem_value,
            growth_pct=growth_pct,
            last_add_height=last_add_height,
            last_withdraw_height=last_withdraw_height,
        )

        saver.additional_properties = d
        return saver

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
