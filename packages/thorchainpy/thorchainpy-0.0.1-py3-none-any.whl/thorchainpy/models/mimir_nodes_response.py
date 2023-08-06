from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.mimir_nodes_response_mimir_vote import MimirNodesResponseMimirVote


T = TypeVar("T", bound="MimirNodesResponse")


@attr.s(auto_attribs=True)
class MimirNodesResponse:
    """
    Attributes:
        mimirs (Union[Unset, List['MimirNodesResponseMimirVote']]):
    """

    mimirs: Union[Unset, List["MimirNodesResponseMimirVote"]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        mimirs: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.mimirs, Unset):
            mimirs = []
            for mimirs_item_data in self.mimirs:
                mimirs_item = mimirs_item_data.to_dict()

                mimirs.append(mimirs_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if mimirs is not UNSET:
            field_dict["mimirs"] = mimirs

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.mimir_nodes_response_mimir_vote import MimirNodesResponseMimirVote

        d = src_dict.copy()
        mimirs = []
        _mimirs = d.pop("mimirs", UNSET)
        for mimirs_item_data in _mimirs or []:
            mimirs_item = MimirNodesResponseMimirVote.from_dict(mimirs_item_data)

            mimirs.append(mimirs_item)

        mimir_nodes_response = cls(
            mimirs=mimirs,
        )

        mimir_nodes_response.additional_properties = d
        return mimir_nodes_response

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
