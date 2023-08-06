from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="NodeNodePreflightStatus")


@attr.s(auto_attribs=True)
class NodeNodePreflightStatus:
    """
    Attributes:
        status (str): the next status of the node Example: Ready.
        reason (str): the reason for the transition to the next status Example: OK.
        code (int):
    """

    status: str
    reason: str
    code: int
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        status = self.status
        reason = self.reason
        code = self.code

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "status": status,
                "reason": reason,
                "code": code,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        status = d.pop("status")

        reason = d.pop("reason")

        code = d.pop("code")

        node_node_preflight_status = cls(
            status=status,
            reason=reason,
            code=code,
        )

        node_node_preflight_status.additional_properties = d
        return node_node_preflight_status

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
