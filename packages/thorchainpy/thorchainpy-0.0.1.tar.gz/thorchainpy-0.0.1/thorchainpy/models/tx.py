from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.coin import Coin


T = TypeVar("T", bound="Tx")


@attr.s(auto_attribs=True)
class Tx:
    """
    Attributes:
        coins (List['Coin']):
        gas (List['Coin']):
        id (Union[Unset, str]):  Example: CF524818D42B63D25BBA0CCC4909F127CAA645C0F9CD07324F2824CC151A64C7.
        chain (Union[Unset, str]):  Example: BTC.
        from_address (Union[Unset, str]):  Example: bcrt1q0s4mg25tu6termrk8egltfyme4q7sg3h8kkydt.
        to_address (Union[Unset, str]):  Example: bcrt1qf3s7q037eancht7sg0aj995dht25rwrnqsf45e.
        memo (Union[Unset, str]):  Example: ADD:BTC.BTC:thor1zupk5lmc84r2dh738a9g3zscavannjy3nzplwt.
    """

    coins: List["Coin"]
    gas: List["Coin"]
    id: Union[Unset, str] = UNSET
    chain: Union[Unset, str] = UNSET
    from_address: Union[Unset, str] = UNSET
    to_address: Union[Unset, str] = UNSET
    memo: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        coins = []
        for coins_item_data in self.coins:
            coins_item = coins_item_data.to_dict()

            coins.append(coins_item)

        gas = []
        for gas_item_data in self.gas:
            gas_item = gas_item_data.to_dict()

            gas.append(gas_item)

        id = self.id
        chain = self.chain
        from_address = self.from_address
        to_address = self.to_address
        memo = self.memo

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "coins": coins,
                "gas": gas,
            }
        )
        if id is not UNSET:
            field_dict["id"] = id
        if chain is not UNSET:
            field_dict["chain"] = chain
        if from_address is not UNSET:
            field_dict["from_address"] = from_address
        if to_address is not UNSET:
            field_dict["to_address"] = to_address
        if memo is not UNSET:
            field_dict["memo"] = memo

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.coin import Coin

        d = src_dict.copy()
        coins = []
        _coins = d.pop("coins")
        for coins_item_data in _coins:
            coins_item = Coin.from_dict(coins_item_data)

            coins.append(coins_item)

        gas = []
        _gas = d.pop("gas")
        for gas_item_data in _gas:
            gas_item = Coin.from_dict(gas_item_data)

            gas.append(gas_item)

        id = d.pop("id", UNSET)

        chain = d.pop("chain", UNSET)

        from_address = d.pop("from_address", UNSET)

        to_address = d.pop("to_address", UNSET)

        memo = d.pop("memo", UNSET)

        tx = cls(
            coins=coins,
            gas=gas,
            id=id,
            chain=chain,
            from_address=from_address,
            to_address=to_address,
            memo=memo,
        )

        tx.additional_properties = d
        return tx

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
