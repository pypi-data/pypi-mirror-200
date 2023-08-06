from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, cast

import attr

from ..models.node_status import NodeStatus

if TYPE_CHECKING:
    from ..models.node_chain_height import NodeChainHeight
    from ..models.node_node_bond_providers import NodeNodeBondProviders
    from ..models.node_node_jail import NodeNodeJail
    from ..models.node_node_preflight_status import NodeNodePreflightStatus
    from ..models.node_node_pub_key_set import NodeNodePubKeySet


T = TypeVar("T", bound="Node")


@attr.s(auto_attribs=True)
class Node:
    """
    Attributes:
        node_address (str):  Example: thor1f3s7q037eancht7sg0aj995dht25rwrnu4ats5.
        status (NodeStatus):  Example: Active.
        pub_key_set (NodeNodePubKeySet):
        validator_cons_pub_key (str): the consensus pub key for the node Example:
            thor104gsqwta048e80j909g6y9kkqdjrw0lff866ew.
        peer_id (str): the P2PID (:6040/p2pid endpoint) of the node Example:
            16Uiu2HAmRgsiryer3pWCPJz18PQZDFFs1GBqCPGGJczrQXdoTBMk.
        active_block_height (int): the block height at which the node became active Example: 123456.
        status_since (int): the block height of the current provided information for the node Example: 100000.
        node_operator_address (str):  Example: thor1f3s7q037eancht7sg0aj995dht25rwrnu4ats5.
        total_bond (str): current node bond Example: 123456789.
        bond_providers (NodeNodeBondProviders):
        signer_membership (List[str]): the set of vault public keys of which the node is a member
        requested_to_leave (bool):
        forced_to_leave (bool): indicates whether the node has been forced to leave by the network, typically via ban
        leave_height (int):
        ip_address (str):  Example: 10.20.30.40.
        version (str): the currently set version of the node Example: 0.35.0.
        slash_points (int): the accumlated slash points, reset at churn but excessive slash points may carry over
            Example: 42.
        jail (NodeNodeJail):
        current_award (str):  Example: 123456.
        observe_chains (List['NodeChainHeight']): the last observed heights for all chain by the node
        preflight_status (NodeNodePreflightStatus):
    """

    node_address: str
    status: NodeStatus
    pub_key_set: "NodeNodePubKeySet"
    validator_cons_pub_key: str
    peer_id: str
    active_block_height: int
    status_since: int
    node_operator_address: str
    total_bond: str
    bond_providers: "NodeNodeBondProviders"
    signer_membership: List[str]
    requested_to_leave: bool
    forced_to_leave: bool
    leave_height: int
    ip_address: str
    version: str
    slash_points: int
    jail: "NodeNodeJail"
    current_award: str
    observe_chains: List["NodeChainHeight"]
    preflight_status: "NodeNodePreflightStatus"
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        node_address = self.node_address
        status = self.status.value

        pub_key_set = self.pub_key_set.to_dict()

        validator_cons_pub_key = self.validator_cons_pub_key
        peer_id = self.peer_id
        active_block_height = self.active_block_height
        status_since = self.status_since
        node_operator_address = self.node_operator_address
        total_bond = self.total_bond
        bond_providers = self.bond_providers.to_dict()

        signer_membership = self.signer_membership

        requested_to_leave = self.requested_to_leave
        forced_to_leave = self.forced_to_leave
        leave_height = self.leave_height
        ip_address = self.ip_address
        version = self.version
        slash_points = self.slash_points
        jail = self.jail.to_dict()

        current_award = self.current_award
        observe_chains = []
        for observe_chains_item_data in self.observe_chains:
            observe_chains_item = observe_chains_item_data.to_dict()

            observe_chains.append(observe_chains_item)

        preflight_status = self.preflight_status.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "node_address": node_address,
                "status": status,
                "pub_key_set": pub_key_set,
                "validator_cons_pub_key": validator_cons_pub_key,
                "peer_id": peer_id,
                "active_block_height": active_block_height,
                "status_since": status_since,
                "node_operator_address": node_operator_address,
                "total_bond": total_bond,
                "bond_providers": bond_providers,
                "signer_membership": signer_membership,
                "requested_to_leave": requested_to_leave,
                "forced_to_leave": forced_to_leave,
                "leave_height": leave_height,
                "ip_address": ip_address,
                "version": version,
                "slash_points": slash_points,
                "jail": jail,
                "current_award": current_award,
                "observe_chains": observe_chains,
                "preflight_status": preflight_status,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.node_chain_height import NodeChainHeight
        from ..models.node_node_bond_providers import NodeNodeBondProviders
        from ..models.node_node_jail import NodeNodeJail
        from ..models.node_node_preflight_status import NodeNodePreflightStatus
        from ..models.node_node_pub_key_set import NodeNodePubKeySet

        d = src_dict.copy()
        node_address = d.pop("node_address")

        status = NodeStatus(d.pop("status"))

        pub_key_set = NodeNodePubKeySet.from_dict(d.pop("pub_key_set"))

        validator_cons_pub_key = d.pop("validator_cons_pub_key")

        peer_id = d.pop("peer_id")

        active_block_height = d.pop("active_block_height")

        status_since = d.pop("status_since")

        node_operator_address = d.pop("node_operator_address")

        total_bond = d.pop("total_bond")

        bond_providers = NodeNodeBondProviders.from_dict(d.pop("bond_providers"))

        signer_membership = cast(List[str], d.pop("signer_membership"))

        requested_to_leave = d.pop("requested_to_leave")

        forced_to_leave = d.pop("forced_to_leave")

        leave_height = d.pop("leave_height")

        ip_address = d.pop("ip_address")

        version = d.pop("version")

        slash_points = d.pop("slash_points")

        jail = NodeNodeJail.from_dict(d.pop("jail"))

        current_award = d.pop("current_award")

        observe_chains = []
        _observe_chains = d.pop("observe_chains")
        for observe_chains_item_data in _observe_chains:
            observe_chains_item = NodeChainHeight.from_dict(observe_chains_item_data)

            observe_chains.append(observe_chains_item)

        preflight_status = NodeNodePreflightStatus.from_dict(d.pop("preflight_status"))

        node = cls(
            node_address=node_address,
            status=status,
            pub_key_set=pub_key_set,
            validator_cons_pub_key=validator_cons_pub_key,
            peer_id=peer_id,
            active_block_height=active_block_height,
            status_since=status_since,
            node_operator_address=node_operator_address,
            total_bond=total_bond,
            bond_providers=bond_providers,
            signer_membership=signer_membership,
            requested_to_leave=requested_to_leave,
            forced_to_leave=forced_to_leave,
            leave_height=leave_height,
            ip_address=ip_address,
            version=version,
            slash_points=slash_points,
            jail=jail,
            current_award=current_award,
            observe_chains=observe_chains,
            preflight_status=preflight_status,
        )

        node.additional_properties = d
        return node

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
