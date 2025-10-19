
from panel_reactflow.nodes import FloatInputNode
from panel_reactflow.reactflow import ReactFlowGraph
from panel_reactflow.api import Node, Edge

"""
        Cant test directly on .edges and .nodes without opening the gui
"""

def test_add_node_empty():
    empty_graph = ReactFlowGraph(nodes_classes=[FloatInputNode], initial_nodes=[], initial_edges=[])

    node = FloatInputNode()
    empty_graph.add_node(Node("node", node, 0, 0))
    
    assert set(empty_graph.item_names) == set(["node"])
    assert set(empty_graph.nodes_instances) == set([node] )
    assert len(empty_graph.item_ports) == 1
    assert len(empty_graph.items) == 1
    assert len(empty_graph.edges) == 0

def test_add_node_with_nodes():
    node = FloatInputNode()
    node_instance = Node("node", node, 0, 0)
    node2 = FloatInputNode()

    two_nodes_graph = ReactFlowGraph(nodes_classes=[FloatInputNode], initial_nodes=[
        node_instance,
    ], initial_edges=[])

    two_nodes_graph.add_node(Node("node2", node2, 0, 0))

    assert set(two_nodes_graph.item_names) == set(["node", "node2"])
    assert set(two_nodes_graph.nodes_instances) == set([node, node2] )
    assert len(two_nodes_graph.item_ports) == 2
    assert len(two_nodes_graph.items) == 2
    assert len(two_nodes_graph.edges) == 0
