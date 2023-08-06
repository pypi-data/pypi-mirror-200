from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="Pool")


@attr.s(auto_attribs=True)
class Pool:
    """
    Attributes:
        balance_rune (str):  Example: 13460619152985.
        balance_asset (str):  Example: 3197744873.
        asset (str):  Example: BTC.BTC.
        lp_units (str): the total pool liquidity provider units Example: 14694928607473.
        pool_units (str): the total pool units, this is the sum of LP and synth units Example: 14694928607473.
        status (str):  Example: Available.
        synth_units (str): the total synth units in the pool Example: 0.
        synth_supply (str): the total supply of synths for the asset Example: 0.
        pending_inbound_rune (str):  Example: 464993836.
        pending_inbound_asset (str):  Example: 101713319.
        savers_depth (str): the balance of L1 asset deposited into the Savers Vault Example: 199998.
        savers_units (str): the number of units owned by Savers Example: 199998.
        synth_mint_paused (bool): whether additional synths cannot be minted Example: True.
        synth_supply_remaining (str): the amount of synth supply remaining before the current max supply is reached
            Example: 123456.
        loan_collateral (str): the amount of collateral collects for loans Example: 123456.
        decimals (Union[Unset, int]):  Example: 6.
    """

    balance_rune: str
    balance_asset: str
    asset: str
    lp_units: str
    pool_units: str
    status: str
    synth_units: str
    synth_supply: str
    pending_inbound_rune: str
    pending_inbound_asset: str
    savers_depth: str
    savers_units: str
    synth_mint_paused: bool
    synth_supply_remaining: str
    loan_collateral: str
    decimals: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        balance_rune = self.balance_rune
        balance_asset = self.balance_asset
        asset = self.asset
        lp_units = self.lp_units
        pool_units = self.pool_units
        status = self.status
        synth_units = self.synth_units
        synth_supply = self.synth_supply
        pending_inbound_rune = self.pending_inbound_rune
        pending_inbound_asset = self.pending_inbound_asset
        savers_depth = self.savers_depth
        savers_units = self.savers_units
        synth_mint_paused = self.synth_mint_paused
        synth_supply_remaining = self.synth_supply_remaining
        loan_collateral = self.loan_collateral
        decimals = self.decimals

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "balance_rune": balance_rune,
                "balance_asset": balance_asset,
                "asset": asset,
                "LP_units": lp_units,
                "pool_units": pool_units,
                "status": status,
                "synth_units": synth_units,
                "synth_supply": synth_supply,
                "pending_inbound_rune": pending_inbound_rune,
                "pending_inbound_asset": pending_inbound_asset,
                "savers_depth": savers_depth,
                "savers_units": savers_units,
                "synth_mint_paused": synth_mint_paused,
                "synth_supply_remaining": synth_supply_remaining,
                "loan_collateral": loan_collateral,
            }
        )
        if decimals is not UNSET:
            field_dict["decimals"] = decimals

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        balance_rune = d.pop("balance_rune")

        balance_asset = d.pop("balance_asset")

        asset = d.pop("asset")

        lp_units = d.pop("LP_units")

        pool_units = d.pop("pool_units")

        status = d.pop("status")

        synth_units = d.pop("synth_units")

        synth_supply = d.pop("synth_supply")

        pending_inbound_rune = d.pop("pending_inbound_rune")

        pending_inbound_asset = d.pop("pending_inbound_asset")

        savers_depth = d.pop("savers_depth")

        savers_units = d.pop("savers_units")

        synth_mint_paused = d.pop("synth_mint_paused")

        synth_supply_remaining = d.pop("synth_supply_remaining")

        loan_collateral = d.pop("loan_collateral")

        decimals = d.pop("decimals", UNSET)

        pool = cls(
            balance_rune=balance_rune,
            balance_asset=balance_asset,
            asset=asset,
            lp_units=lp_units,
            pool_units=pool_units,
            status=status,
            synth_units=synth_units,
            synth_supply=synth_supply,
            pending_inbound_rune=pending_inbound_rune,
            pending_inbound_asset=pending_inbound_asset,
            savers_depth=savers_depth,
            savers_units=savers_units,
            synth_mint_paused=synth_mint_paused,
            synth_supply_remaining=synth_supply_remaining,
            loan_collateral=loan_collateral,
            decimals=decimals,
        )

        pool.additional_properties = d
        return pool

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
