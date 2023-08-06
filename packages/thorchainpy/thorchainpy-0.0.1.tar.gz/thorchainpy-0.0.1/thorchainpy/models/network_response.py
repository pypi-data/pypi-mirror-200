from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="NetworkResponse")


@attr.s(auto_attribs=True)
class NetworkResponse:
    """
    Attributes:
        bond_reward_rune (str): total amount of RUNE awarded to node operators Example: 857134475040.
        burned_bep_2_rune (str): total of burned BEP2 RUNE Example: 674699077345087.
        burned_erc_20_rune (str): total of burned ERC20 RUNE Example: 66369401654835.
        total_bond_units (str): total bonded RUNE Example: 0.
        total_reserve (str): total reserve RUNE Example: 21999180112172346.
        vaults_migrating (bool): Returns true if there exist RetiringVaults which have not finished migrating funds to
            new ActiveVaults
        gas_spent_rune (str): Sum of the gas the network has spent to send outbounds Example: 1000000000.
        gas_withheld_rune (str): Sum of the gas withheld from users to cover outbound gas Example: 1500000000.
        outbound_fee_multiplier (Union[Unset, str]): Current outbound fee multiplier, in basis points Example: 15000.
    """

    bond_reward_rune: str
    burned_bep_2_rune: str
    burned_erc_20_rune: str
    total_bond_units: str
    total_reserve: str
    vaults_migrating: bool
    gas_spent_rune: str
    gas_withheld_rune: str
    outbound_fee_multiplier: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        bond_reward_rune = self.bond_reward_rune
        burned_bep_2_rune = self.burned_bep_2_rune
        burned_erc_20_rune = self.burned_erc_20_rune
        total_bond_units = self.total_bond_units
        total_reserve = self.total_reserve
        vaults_migrating = self.vaults_migrating
        gas_spent_rune = self.gas_spent_rune
        gas_withheld_rune = self.gas_withheld_rune
        outbound_fee_multiplier = self.outbound_fee_multiplier

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "bond_reward_rune": bond_reward_rune,
                "burned_bep_2_rune": burned_bep_2_rune,
                "burned_erc_20_rune": burned_erc_20_rune,
                "total_bond_units": total_bond_units,
                "total_reserve": total_reserve,
                "vaults_migrating": vaults_migrating,
                "gas_spent_rune": gas_spent_rune,
                "gas_withheld_rune": gas_withheld_rune,
            }
        )
        if outbound_fee_multiplier is not UNSET:
            field_dict["outbound_fee_multiplier"] = outbound_fee_multiplier

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        bond_reward_rune = d.pop("bond_reward_rune")

        burned_bep_2_rune = d.pop("burned_bep_2_rune")

        burned_erc_20_rune = d.pop("burned_erc_20_rune")

        total_bond_units = d.pop("total_bond_units")

        total_reserve = d.pop("total_reserve")

        vaults_migrating = d.pop("vaults_migrating")

        gas_spent_rune = d.pop("gas_spent_rune")

        gas_withheld_rune = d.pop("gas_withheld_rune")

        outbound_fee_multiplier = d.pop("outbound_fee_multiplier", UNSET)

        network_response = cls(
            bond_reward_rune=bond_reward_rune,
            burned_bep_2_rune=burned_bep_2_rune,
            burned_erc_20_rune=burned_erc_20_rune,
            total_bond_units=total_bond_units,
            total_reserve=total_reserve,
            vaults_migrating=vaults_migrating,
            gas_spent_rune=gas_spent_rune,
            gas_withheld_rune=gas_withheld_rune,
            outbound_fee_multiplier=outbound_fee_multiplier,
        )

        network_response.additional_properties = d
        return network_response

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
