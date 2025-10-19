
from typing import Any, Dict, List, Type
import panel as pn

import param

from panel_reactflow.reactflow import ReactFlowGraph
from panel_reactflow.events import NodeCreation, NodeDeletion, NodeMove, NodeSelected, NodeDeselected
from panel_reactflow.events import EdgeCreation, EdgeDeletion, EdgeSelected, EdgeDeselected
from panel_reactflow.api import ReactFlowNode, Edge, Node, NodePort, PortDirection

class WorkflowNode:
    node_class_name = ""
    """Node class name, as it will appear in the reactflow side bar."""
    ports:List[NodePort]
    """List of node ports"""
    plugged_nodes:Dict[str, List['WorkflowNode']]
    """List of currently plugged ports, automatically updated by the ReactFlow class"""
    name:str

    def __init__(self,):
        """ ReactflowNode constructor used to instanciate the plugged_nodes dictionnary. It is necessary to call it in nodes constructors.
        """
        self.plugged_nodes = {}

    def create(self, ) -> pn.viewable.Viewable:
        """Function called by the Reactflow class to instanciate the content of the node
        """
        raise NotImplementedError

    def update(self, _):
        """Update the node content based on the input ports.

        Parameters
        ----------
        _ : Any
            Event requesting the update
        """
        self.update_outputs()
    
    def update_outputs(self, ):
        """Call the output function on all nodes plugged on output ports.
        """
        for port in self.ports:
            if port.direction == PortDirection.OUTPUT and port.name in self.plugged_nodes:
                for node in self.plugged_nodes[port.name]:
                    node.update(None)

    
    def get_node_json_value(self,) -> Dict[str, Any]:
        """ Returns a dictionnary describing the node content, this dictionnary can be obtain by other nodes in their update call.
        
        Returns
        ----------
        Dict[str, Any]
            Node properties
        """
        raise NotImplementedError
    
    def on_node_move(self, node_move:NodeMove):
        """Function triggered when a node is moved in the graph

        Parameters
        ----------
        node_move : NodeMove
            Node movement data
        """
        pass
    
    def on_node_selected(self, ):
        """Function triggered when a node is selected
        """
        pass
    
    def on_node_deselected(self, ):
        """Function triggered when a node is deselected
        """
        pass


class Workflow(ReactFlowGraph):

    def __init__(self, 
                    sizing_mode = "stretch_both", 
                    nodes_classes:List[Type[ReactFlowNode]] = [], 
                    initial_nodes:List[Node] = [],
                    initial_edges:List[Edge] = [],
                    display_side_bar:bool = True,
                    allow_edge_loops:bool = False,
                    **kwargs):
        """Node graph holoviz panel component

        Parameters
        ----------
        nodes_classes : List[Type[ReactFlowNode]], optional
            List of node classes that are present in the side bar, by default []
        initial_nodes : List[Node], optional
            List of nodes in the graph at its creation, by default []
        initial_edges : List[Edge], optional
            List of edges in the graph at its creation, by default []
        sizing_mode : str, optional
            Sizing mod of the Viewable, default at stretch_both to prevent the graph to be of zero size, by default "stretch_both"
        display_side_bar : bool, optional
            Display the side bar to drag and drop new nodes, by default True
        allow_edge_loops : bool, optional
            Allow to have edge loops in the graph (can lead to update infinite loops), by default False
        """
        super().__init__(
            sizing_mode = sizing_mode,
            nodes_classes = nodes_classes,
            initial_nodes = initial_nodes,
            initial_edges = initial_edges,
            display_side_bar = display_side_bar,
            allow_edge_loops = allow_edge_loops,
            **kwargs
        )

    def update_nodes(self, _:param.parameterized.Event):
        """Updates the nodes based on the noticed changes in the graph

        Parameters
        ----------
        _ : param.parameterized.Event
            Trigerring event
        """
        node_dict = {n["id"]: n for n in self.nodes}
        edge_dict = {e["id"]: e for e in self.edges}

        node_changes = self._check_node_change(node_dict)
        edge_changes = self._check_edge_change(edge_dict)
        
        if len([nc for nc in node_changes if type(nc) in [NodeCreation, NodeDeletion]]) +\
            len([ec for ec in edge_changes if type(ec) in [EdgeCreation, EdgeDeletion]]) > 0:
            self._build_node_tree()

            # Clearing nodes instances list from deleted nodes can lead to sync errors
            # self.nodes_instances = [node for node in self.nodes_instances if node.name in list(n["id"] for n in self.nodes)]

        for node_change in node_changes:
            if isinstance(node_change, NodeCreation):
                self.nodes_instances[self.item_names.index(node_change.node_name)].update(None)
            elif isinstance(node_change, NodeMove):
                self.nodes_instances[self.item_names.index(node_change.node_name)].on_node_move(node_change)
            elif isinstance(node_change, NodeSelected):
                self.nodes_instances[self.item_names.index(node_change.node_name)].on_node_selected()
            elif isinstance(node_change, NodeDeselected):
                self.nodes_instances[self.item_names.index(node_change.node_name)].on_node_deselected()

        for edge_change in edge_changes:
            if isinstance(edge_change, EdgeCreation):
                self.nodes_instances[self.item_names.index(edge_change.target)].update(None)
            elif isinstance(edge_change, EdgeDeletion):
                # Checking the node wasn't removed from the list (node deletion triggers an edge deletion)
                if edge_change.target in self.item_names:
                    self.nodes_instances[self.item_names.index(edge_change.target)].update(None)
            elif isinstance(edge_change, EdgeSelected):
                if self.edge_selection_callback is not None:
                    self.edge_selection_callback(edge_change)
            elif isinstance(edge_change, EdgeDeselected):
                if self.edge_deselection_callback is not None:
                    self.edge_deselection_callback(edge_change)

        # Calling every registered callbacks
        for node_change in node_changes:
            for callback in self._rf_event__callbacks[node_change.__class__]:
                callback(node_change)
                
        for edge_change in edge_changes:
            for callback in self._rf_event__callbacks[edge_change.__class__]:
                callback(edge_change)
                
        # Storing the current node and edge state for next call
        self.old_nodes = node_dict
        self.old_edges = edge_dict
         
    def _build_node_tree(self,):
        """Provides to the nodes who is plugged to them for the nodes updates
        """
        # Removing edges of the nodes that could have been removed in the event triggering the node tree building
        self.edges = [e for e in self.edges if e["source"] in self.item_names and e["target"] in self.item_names]

        for node in self.nodes_instances:
            node.plugged_nodes = {port.name : [] for port in node.ports}

        for edge in self.edges:
            source_node = [node for node in self.nodes_instances if node.name == edge["source"]][0]
            target_node = [node for node in self.nodes_instances if node.name == edge["target"]][0]

            source_port_name = edge["sourceHandle"]
            target_port_name = edge["targetHandle"]

            source_node.plugged_nodes[source_port_name].append(target_node)
            target_node.plugged_nodes[target_port_name].append(source_node)
