
from panel_reactflow.nodes import FloatInputNode
from panel_reactflow.reactflow import ReactFlowGraph
from panel_reactflow.api import Node, Edge

def test_init_empty():
    empty_graph = ReactFlowGraph(nodes_classes=[FloatInputNode], initial_nodes=[], initial_edges=[])

    assert empty_graph.nodes_classes == [FloatInputNode]
    assert empty_graph.nodes == []
    assert empty_graph.edges == [] 

def test_init_with_one_node():
    node = FloatInputNode()
    node_instance = Node("node", node, 0, 0)
    one_node_graph = ReactFlowGraph(nodes_classes=[FloatInputNode], initial_nodes=[
        node_instance
    ], initial_edges=[])

    assert one_node_graph.nodes_classes == [FloatInputNode]
    assert one_node_graph.item_names == ["node"]
    assert one_node_graph.nodes_instances == [node] 
    assert len(one_node_graph.item_ports) == 1
    assert len(one_node_graph.items) == 1
    assert len(one_node_graph.edges) == 0

def test_init_with_nodes():
    node = FloatInputNode()
    node_instance = Node("node", node, 0, 0)
    node2 = FloatInputNode()
    node_instance2 = Node("node2", node2, 0, 0)

    two_nodes_graph = ReactFlowGraph(nodes_classes=[FloatInputNode], initial_nodes=[
        node_instance,
        node_instance2
    ], initial_edges=[])

    assert two_nodes_graph.nodes_classes == [FloatInputNode]
    assert set(two_nodes_graph.item_names) == set(["node", "node2"])
    assert set(two_nodes_graph.nodes_instances) == set([node, node2] )
    assert len(two_nodes_graph.item_ports) == 2
    assert len(two_nodes_graph.items) == 2
    assert len(two_nodes_graph.edges) == 0
