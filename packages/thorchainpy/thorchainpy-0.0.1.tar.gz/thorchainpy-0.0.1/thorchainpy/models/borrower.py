from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="Borrower")


@attr.s(auto_attribs=True)
class Borrower:
    """
    Attributes:
        owner (str):  Example: bnb1xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx.
        asset (str):  Example: BNB.BNB.
        debt_up (str):  Example: 123456.
        debt_down (str):  Example: 123456.
        collateral_up (str):  Example: 123456.
        collateral_down (str):  Example: 123456.
        last_open_height (int):  Example: 82745.
        last_repay_height (int):  Example: 82745.
    """

    owner: str
    asset: str
    debt_up: str
    debt_down: str
    collateral_up: str
    collateral_down: str
    last_open_height: int
    last_repay_height: int
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        owner = self.owner
        asset = self.asset
        debt_up = self.debt_up
        debt_down = self.debt_down
        collateral_up = self.collateral_up
        collateral_down = self.collateral_down
        last_open_height = self.last_open_height
        last_repay_height = self.last_repay_height

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "owner": owner,
                "asset": asset,
                "debt_up": debt_up,
                "debt_down": debt_down,
                "collateral_up": collateral_up,
                "collateral_down": collateral_down,
                "last_open_height": last_open_height,
                "last_repay_height": last_repay_height,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        owner = d.pop("owner")

        asset = d.pop("asset")

        debt_up = d.pop("debt_up")

        debt_down = d.pop("debt_down")

        collateral_up = d.pop("collateral_up")

        collateral_down = d.pop("collateral_down")

        last_open_height = d.pop("last_open_height")

        last_repay_height = d.pop("last_repay_height")

        borrower = cls(
            owner=owner,
            asset=asset,
            debt_up=debt_up,
            debt_down=debt_down,
            collateral_up=collateral_up,
            collateral_down=collateral_down,
            last_open_height=last_open_height,
            last_repay_height=last_repay_height,
        )

        borrower.additional_properties = d
        return borrower

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
