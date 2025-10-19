
from panel_reactflow.nodes import FloatInputNode, PrintInputNode
from panel_reactflow.reactflow import ReactFlowGraph
from panel_reactflow.api import Node, Edge

def test_remove_node_empty():
    empty_graph = ReactFlowGraph(nodes_classes=[FloatInputNode], initial_nodes=[], initial_edges=[])

    node = FloatInputNode()
    empty_graph.add_node(Node("node", node, 0, 0))
    empty_graph.remove_nodes(["node"])
    
    assert set(empty_graph.item_names) == set([])
    assert len(empty_graph.item_ports) == 0
    assert len(empty_graph.items) == 0
    assert len(empty_graph.edges) == 0

def test_remove_node_with_nodes():
    node = FloatInputNode()
    node_instance = Node("node", node, 0, 0)
    node2 = FloatInputNode()

    two_nodes_graph = ReactFlowGraph(nodes_classes=[FloatInputNode], initial_nodes=[
        node_instance,
    ], initial_edges=[])

    two_nodes_graph.add_node(Node("node2", node2, 0, 0))
    two_nodes_graph.remove_nodes(["node2"])

    assert set(two_nodes_graph.item_names) == set(["node"])
    assert len(two_nodes_graph.item_ports) == 1
    assert len(two_nodes_graph.items) == 1
    assert len(two_nodes_graph.edges) == 0

def test_remove_node_all_nodes():
    node = FloatInputNode()
    node_instance = Node("node", node, 0, 0)
    node2 = FloatInputNode()

    two_nodes_graph = ReactFlowGraph(nodes_classes=[FloatInputNode], initial_nodes=[
        node_instance,
    ], initial_edges=[])

    two_nodes_graph.add_node(Node("node2", node2, 0, 0))
    two_nodes_graph.remove_nodes(["node", "node2"])

    assert set(two_nodes_graph.item_names) == set([])
    assert len(two_nodes_graph.item_ports) == 0
    assert len(two_nodes_graph.items) == 0
    assert len(two_nodes_graph.edges) == 0

def test_remove_node_wrong_type():
    node = FloatInputNode()
    node_instance = Node("node", node, 0, 0)
    node2 = FloatInputNode()

    two_nodes_graph = ReactFlowGraph(nodes_classes=[FloatInputNode], initial_nodes=[
        node_instance,
    ], initial_edges=[])

    two_nodes_graph.add_node(Node("node2", node2, 0, 0))
    try:
        two_nodes_graph.remove_nodes("node")
    except AssertionError:
        return
    
    raise AssertionError("Removing nodes did not raise an assertion error when a non-list was provided.")


"""
        Cant test directly on .edges and .nodes without opening the gui
"""
# def test_remove_node_with_edge():
#     node = FloatInputNode()
#     node_instance = Node("node", node, 0, 0)
#     node2 = PrintInputNode()
#     node_instance2 = Node("node2", node2, 0, 0)
#     node3 = FloatInputNode()
#     node_instance3 = Node("node3", node3, 0, 0)

#     two_nodes_graph = ReactFlowGraph(nodes_classes=[FloatInputNode, PrintInputNode], initial_nodes=[
#         node_instance,
#         node_instance2,
#         node_instance3,
#     ], initial_edges=[
#         Edge("node", "Output", "node2", "Input"),
#     ])

#     two_nodes_graph.remove_nodes(["node2"])

#     assert set(two_nodes_graph.item_names) == set(["node", "node3"])
#     assert len(two_nodes_graph.item_ports) == 2
#     assert len(two_nodes_graph.items) == 2
#     assert len(two_nodes_graph.edges) == 0

# def test_remove_node_with_other_edge():
#     node = FloatInputNode()
#     node_instance = Node("node", node, 0, 0)
#     node2 = PrintInputNode()
#     node_instance2 = Node("node2", node2, 0, 0)
#     node3 = FloatInputNode()
#     node_instance3 = Node("node3", node3, 0, 0)

#     two_nodes_graph = ReactFlowGraph(nodes_classes=[FloatInputNode, PrintInputNode], initial_nodes=[
#         node_instance,
#         node_instance2,
#         node_instance3,
#     ], initial_edges=[
#         Edge("node", "Output", "node2", "Input"),
#     ])

#     two_nodes_graph.remove_nodes(["node3"])

#     assert set(two_nodes_graph.item_names) == set(["node", "node2"])
#     assert len(two_nodes_graph.item_ports) == 2
#     assert len(two_nodes_graph.items) == 2
#     assert len(two_nodes_graph.edges) == 1
