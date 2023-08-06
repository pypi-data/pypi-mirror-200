from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="InboundAddress")


@attr.s(auto_attribs=True)
class InboundAddress:
    """
    Attributes:
        halted (bool): Returns true if trading is unavailable for this chain, either because trading is halted globally
            or specifically for this chain
        chain (Union[Unset, str]):  Example: BTC.
        pub_key (Union[Unset, str]):  Example:
            thorpub1addwnpepq2jqhv5rdqlkusfxy05stfzcgslhhz5qh8pxetw5ry2aa6awgdh3shq8s82.
        address (Union[Unset, str]):  Example: bc1qn9esxuw8ca7ts8l6w66kdh800s09msvutydc46.
        router (Union[Unset, str]):  Example: 0xD37BbE5744D730a1d98d8DC97c42F0Ca46aD7146.
        global_trading_paused (Union[Unset, bool]): Returns true if trading is paused globally
        chain_trading_paused (Union[Unset, bool]): Returns true if trading is paused for this chain
        chain_lp_actions_paused (Union[Unset, bool]): Returns true if LP actions are paused for this chain
        gas_rate (Union[Unset, str]): The minimum fee rate used by vaults to send outbound TXs. The actual fee rate may
            be higher. For EVM chains this is returned in gwei (1e9). Example: 214.
        gas_rate_units (Union[Unset, str]): Units of the gas_rate. Example: satsperbyte.
        outbound_tx_size (Union[Unset, str]): Avg size of outbound TXs on each chain. For UTXO chains it may be larger
            than average, as it takes into account vault consolidation txs, which can have many vouts Example: 1000.
        outbound_fee (Union[Unset, str]): The total outbound fee charged to the user for outbound txs in the gas asset
            of the chain. Example: 428000.
        dust_threshold (Union[Unset, str]): Defines the minimum transaction size for the chain in base units (sats, wei,
            uatom). Transactions with asset amounts lower than the dust_threshold are ignored. Example: 10000.
    """

    halted: bool
    chain: Union[Unset, str] = UNSET
    pub_key: Union[Unset, str] = UNSET
    address: Union[Unset, str] = UNSET
    router: Union[Unset, str] = UNSET
    global_trading_paused: Union[Unset, bool] = UNSET
    chain_trading_paused: Union[Unset, bool] = UNSET
    chain_lp_actions_paused: Union[Unset, bool] = UNSET
    gas_rate: Union[Unset, str] = UNSET
    gas_rate_units: Union[Unset, str] = UNSET
    outbound_tx_size: Union[Unset, str] = UNSET
    outbound_fee: Union[Unset, str] = UNSET
    dust_threshold: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        halted = self.halted
        chain = self.chain
        pub_key = self.pub_key
        address = self.address
        router = self.router
        global_trading_paused = self.global_trading_paused
        chain_trading_paused = self.chain_trading_paused
        chain_lp_actions_paused = self.chain_lp_actions_paused
        gas_rate = self.gas_rate
        gas_rate_units = self.gas_rate_units
        outbound_tx_size = self.outbound_tx_size
        outbound_fee = self.outbound_fee
        dust_threshold = self.dust_threshold

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "halted": halted,
            }
        )
        if chain is not UNSET:
            field_dict["chain"] = chain
        if pub_key is not UNSET:
            field_dict["pub_key"] = pub_key
        if address is not UNSET:
            field_dict["address"] = address
        if router is not UNSET:
            field_dict["router"] = router
        if global_trading_paused is not UNSET:
            field_dict["global_trading_paused"] = global_trading_paused
        if chain_trading_paused is not UNSET:
            field_dict["chain_trading_paused"] = chain_trading_paused
        if chain_lp_actions_paused is not UNSET:
            field_dict["chain_lp_actions_paused"] = chain_lp_actions_paused
        if gas_rate is not UNSET:
            field_dict["gas_rate"] = gas_rate
        if gas_rate_units is not UNSET:
            field_dict["gas_rate_units"] = gas_rate_units
        if outbound_tx_size is not UNSET:
            field_dict["outbound_tx_size"] = outbound_tx_size
        if outbound_fee is not UNSET:
            field_dict["outbound_fee"] = outbound_fee
        if dust_threshold is not UNSET:
            field_dict["dust_threshold"] = dust_threshold

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        halted = d.pop("halted")

        chain = d.pop("chain", UNSET)

        pub_key = d.pop("pub_key", UNSET)

        address = d.pop("address", UNSET)

        router = d.pop("router", UNSET)

        global_trading_paused = d.pop("global_trading_paused", UNSET)

        chain_trading_paused = d.pop("chain_trading_paused", UNSET)

        chain_lp_actions_paused = d.pop("chain_lp_actions_paused", UNSET)

        gas_rate = d.pop("gas_rate", UNSET)

        gas_rate_units = d.pop("gas_rate_units", UNSET)

        outbound_tx_size = d.pop("outbound_tx_size", UNSET)

        outbound_fee = d.pop("outbound_fee", UNSET)

        dust_threshold = d.pop("dust_threshold", UNSET)

        inbound_address = cls(
            halted=halted,
            chain=chain,
            pub_key=pub_key,
            address=address,
            router=router,
            global_trading_paused=global_trading_paused,
            chain_trading_paused=chain_trading_paused,
            chain_lp_actions_paused=chain_lp_actions_paused,
            gas_rate=gas_rate,
            gas_rate_units=gas_rate_units,
            outbound_tx_size=outbound_tx_size,
            outbound_fee=outbound_fee,
            dust_threshold=dust_threshold,
        )

        inbound_address.additional_properties = d
        return inbound_address

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
