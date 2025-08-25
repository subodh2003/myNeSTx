import time
from nest.topology import *
from nest.topology.network import Network
from nest.topology.address_helper import AddressHelper
from nest.routing.routing_helper import RoutingHelper
import nest.config as config
config.set_value("delete_namespaces_on_termination", False)

def create_spine_leaf(s, l, n):
    try:
        # Create routers and hosts
        spines = [Router(f"sr{i}") for i in range(s)]
        leafs = [Router(f"lr{i}") for i in range(l)]
        nodes = [Node(f"n{i}") for i in range(n)]

        # Create networks with valid IP subnets
        rns = [Network(f"10.0.{i}.0/24") for i in range(s * l)]   # spine-leaf links
        lns = [Network(f"10.1.{i}.0/24") for i in range(l * n)]   # leaf-node links

        # Connect each spine to each leaf (unique network per connection)
        net_index = 0
        for spine in spines:
            for leaf in leafs:
                connect(spine, leaf, network=rns[net_index])
                net_index += 1

        # Connect each node to its corresponding leaf
        net_index = 0
        for i, leaf in enumerate(leafs):
            if i < len(nodes):   # one node per leaf
                connect(leaf, nodes[i], network=lns[net_index])
                net_index += 1

        # Assign addresses
        ah = AddressHelper()
        ah.assign_addresses()

        # Start routing (OSPF)
        rh = RoutingHelper(protocol="ospf")
        rh.populate_routing_tables()

        # Test connectivity (first two nodes)
        if len(nodes) >= 2:
            print("\n[TEST] Pinging n0 -> n1")
            nodes[0].ping(nodes[1])

    finally:
        print("Exiting...")


# Example: 2 spines, 4 leaves, 4 nodes
create_spine_leaf(2, 4, 4)
