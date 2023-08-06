from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="LiquidityProvider")


@attr.s(auto_attribs=True)
class LiquidityProvider:
    """
    Attributes:
        asset (str):  Example: BNB.BNB.
        units (str):  Example: 0.
        pending_rune (str):  Example: 0.
        pending_asset (str):  Example: 242000000.
        rune_deposit_value (str):  Example: 0.
        asset_deposit_value (str):  Example: 0.
        rune_redeem_value (str):  Example: 0.
        asset_redeem_value (str):  Example: 0.
        luvi_deposit_value (str):  Example: 0.
        luvi_redeem_value (str):  Example: 0.
        luvi_growth_pct (str):  Example: 0.
        rune_address (Union[Unset, str]):  Example: thor1xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx.
        asset_address (Union[Unset, str]):  Example: bnb1xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx.
        last_add_height (Union[Unset, int]):  Example: 82745.
        last_withdraw_height (Union[Unset, int]):  Example: 82745.
        pending_tx_id (Union[Unset, str]):  Example: C4C876802xxxxxxxxxxBC408829878446A37011EBBA0C5CAA3DD64A548879CB228.
    """

    asset: str
    units: str
    pending_rune: str
    pending_asset: str
    rune_deposit_value: str
    asset_deposit_value: str
    rune_redeem_value: str
    asset_redeem_value: str
    luvi_deposit_value: str
    luvi_redeem_value: str
    luvi_growth_pct: str
    rune_address: Union[Unset, str] = UNSET
    asset_address: Union[Unset, str] = UNSET
    last_add_height: Union[Unset, int] = UNSET
    last_withdraw_height: Union[Unset, int] = UNSET
    pending_tx_id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        asset = self.asset
        units = self.units
        pending_rune = self.pending_rune
        pending_asset = self.pending_asset
        rune_deposit_value = self.rune_deposit_value
        asset_deposit_value = self.asset_deposit_value
        rune_redeem_value = self.rune_redeem_value
        asset_redeem_value = self.asset_redeem_value
        luvi_deposit_value = self.luvi_deposit_value
        luvi_redeem_value = self.luvi_redeem_value
        luvi_growth_pct = self.luvi_growth_pct
        rune_address = self.rune_address
        asset_address = self.asset_address
        last_add_height = self.last_add_height
        last_withdraw_height = self.last_withdraw_height
        pending_tx_id = self.pending_tx_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "asset": asset,
                "units": units,
                "pending_rune": pending_rune,
                "pending_asset": pending_asset,
                "rune_deposit_value": rune_deposit_value,
                "asset_deposit_value": asset_deposit_value,
                "rune_redeem_value": rune_redeem_value,
                "asset_redeem_value": asset_redeem_value,
                "luvi_deposit_value": luvi_deposit_value,
                "luvi_redeem_value": luvi_redeem_value,
                "luvi_growth_pct": luvi_growth_pct,
            }
        )
        if rune_address is not UNSET:
            field_dict["rune_address"] = rune_address
        if asset_address is not UNSET:
            field_dict["asset_address"] = asset_address
        if last_add_height is not UNSET:
            field_dict["last_add_height"] = last_add_height
        if last_withdraw_height is not UNSET:
            field_dict["last_withdraw_height"] = last_withdraw_height
        if pending_tx_id is not UNSET:
            field_dict["pending_tx_id"] = pending_tx_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        asset = d.pop("asset")

        units = d.pop("units")

        pending_rune = d.pop("pending_rune")

        pending_asset = d.pop("pending_asset")

        rune_deposit_value = d.pop("rune_deposit_value")

        asset_deposit_value = d.pop("asset_deposit_value")

        rune_redeem_value = d.pop("rune_redeem_value")

        asset_redeem_value = d.pop("asset_redeem_value")

        luvi_deposit_value = d.pop("luvi_deposit_value")

        luvi_redeem_value = d.pop("luvi_redeem_value")

        luvi_growth_pct = d.pop("luvi_growth_pct")

        rune_address = d.pop("rune_address", UNSET)

        asset_address = d.pop("asset_address", UNSET)

        last_add_height = d.pop("last_add_height", UNSET)

        last_withdraw_height = d.pop("last_withdraw_height", UNSET)

        pending_tx_id = d.pop("pending_tx_id", UNSET)

        liquidity_provider = cls(
            asset=asset,
            units=units,
            pending_rune=pending_rune,
            pending_asset=pending_asset,
            rune_deposit_value=rune_deposit_value,
            asset_deposit_value=asset_deposit_value,
            rune_redeem_value=rune_redeem_value,
            asset_redeem_value=asset_redeem_value,
            luvi_deposit_value=luvi_deposit_value,
            luvi_redeem_value=luvi_redeem_value,
            luvi_growth_pct=luvi_growth_pct,
            rune_address=rune_address,
            asset_address=asset_address,
            last_add_height=last_add_height,
            last_withdraw_height=last_withdraw_height,
            pending_tx_id=pending_tx_id,
        )

        liquidity_provider.additional_properties = d
        return liquidity_provider

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
