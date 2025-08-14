
from pathlib import Path
from typing import Any, Callable, Dict, List, NamedTuple, Type
import panel as pn

from panel.custom import Child, Children, ReactComponent, ESMEvent
import param

from reactflow_api import NodeCreation, NodeDeletion, NodeChange, NodeMove, NodeSelected, NodeDeselected
from reactflow_api import EdgeCreation, EdgeDeletion, EdgeSelected, EdgeDeselected, EdgeChange
from reactflow_api import NodeCreation, ReactFlowNode, EdgeInstance, NodeInstance, NodePort, PortDirection, PortPosition
# reactflow site : https://reactflow.dev/learn
# reactflow github :https://github.com/xyflow/xyflow/tree/main/packages/react
# reactflow custom component : https://reactflow.dev/learn/customization/custom-nodes
# tutorials : https://reactflow.dev/examples/

# confetti example : https://panel.holoviz.org/reference/custom_components/ReactComponent.html#dependency-imports

# /* esm.sh - reactflow@11.11.4 */
# import "/@reactflow/background@11.3.14/es2022/background.mjs";
# import "/@reactflow/controls@11.2.14/es2022/controls.mjs";
# import "/@reactflow/core@11.11.4/es2022/core.mjs";
# import "/@reactflow/minimap@11.7.14/es2022/minimap.mjs";
# import "/@reactflow/node-resizer@2.2.14/es2022/node-resizer.mjs";
# import "/@reactflow/node-toolbar@1.3.14/es2022/node-toolbar.mjs";
# export * from "/reactflow@11.11.4/es2022/reactflow.mjs";
# export { default } from "/reactflow@11.11.4/es2022/reactflow.mjs";

def make_css(node_name):
    return """.react-flow__node-{node_name} {
  padding: 10px;
  border-radius: 3px;
  min-width: 150px;
  font-size: 12px;
  color: #222;
  text-align: center;
  border-width: 1px;
  border-style: solid;
  border-color: #1a192b;
  background-color: white;
}

}

.react-flow__node-{node_name}.selectable:hover {
      box-shadow: 0 1px 4px 1px rgba(0, 0, 0, 0.08);
}
.react-flow__node-{node_name}.selectable.selected,
    .react-flow__node-{node_name}.selectable:focus,
    .react-flow__node-{node_name}.selectable:focus-visible {
      box-shadow: 0 0 0 0.5px #1a192b;
}
    """.replace("{node_name}", node_name)
"""Basic node display that is added to the default style.css"""



class ReactFlow(ReactComponent):

    edges = param.List()
    """List of edges in the graph. Contains dictionnaries such as :
        ```
        {
            "source": Source node name,
            "sourceHandle": Source port name,
            "target": Target node name,
            "targetHandle": Target port name,
            "id": edge ID,
        } 
        ```"""
    nodes = param.List()
    """List of nodes in the graph. Contains dictionnaries such as :
        ```
        {
            "id": Node ID/name,
            "type":'panelWidget',
            "position":{"x":X coordinate,"y":Y coordinage},
            "data":{"label":Displayed name}
        }
        ```"""
    item_ports = param.List()
    """List of currently instanciated ports"""
    
    initial_nodes = param.List()
    """List of nodes as provided by the user during the Reactflow construction."""
    initial_edges = param.List()
    """List of edges as provided by the user during the Reactflow construction."""

    items = Children()
    """List of Viewables assiciated to each node."""
    item_names = param.List()
    """List of node names, in the same order as items."""
    
    display_side_bar = param.Boolean()
    """Display the side bar to drag and drop new nodes."""
    allow_edge_loops = param.Boolean()
    """Allow to have edge loops in the graph (can lead to update infinite loops)."""

    nodes_classes: List[Type[ReactFlowNode]] = []
    """Provided nodes classes that are instanciated when a node is dragged from the sidebar."""
    nodes_instances: List[ReactFlowNode] = []
    """All node instance in the graph."""

    node_class_labels = param.List()
    """List of node class names as displayed in the sidebar."""

    _importmap = {
        "imports": {
            "reactflow": "https://esm.sh/reactflow@11.11.4", 
        }
    }
    """Imports from the esm.sh website"""
    
    _stylesheets = [
                        "https://unpkg.com/reactflow@11.11.4/dist/style.css",
                        make_css("dndnode"),
                        make_css("input"),
                        make_css("panelWidget"),
                        Path(Path(__file__).parent / "dnd_flow.css"),
                    ]
    """CSS elements to customize the graph appearance"""
    
    _esm = Path(__file__).parent / "reactflow.js"
    """Javascrip file containing the reactflow graph definition"""

    def __init__(self, 
                    sizing_mode = "stretch_both", 
                    nodes_classes:List[Type[ReactFlowNode]] = [], 
                    initial_nodes:List[NodeInstance] = [],
                    initial_edges:List[EdgeInstance] = [],
                    display_side_bar:bool = True,
                    allow_edge_loops:bool = False,
                    **kwargs):
        """Node graph holoviz panel component

        Parameters
        ----------
        nodes_classes : List[Type[ReactFlowNode]], optional
            List of node classes that are present in the side bar, by default []
        initial_nodes : List[NodeInstance], optional
            List of nodes in the graph at its creation, by default []
        initial_edges : List[EdgeInstance], optional
            List of edges in the graph at its creation, by default []
        sizing_mode : str, optional
            Sizing mod of the Viewable, default at stretch_both to prevent the graph to be of zero size, by default "stretch_both"
        display_side_bar : bool, optional
            Display the side bar to drag and drop new nodes, by default True
        allow_edge_loops : bool, optional
            Allow to have edge loops in the graph (can lead to update infinite loops), by default False
        """
        
        super().__init__(sizing_mode=sizing_mode, **kwargs)

        self.nodes_classes = nodes_classes
        self.node_class_labels = [c.node_class_name for c in self.nodes_classes]

        self.display_side_bar = display_side_bar 
        self.allow_edge_loops = allow_edge_loops 

        # Adding all nodes present in the initial nodes 
        for node in initial_nodes:
            self.add_node(node)

        # Creating the dictionnaries for ReactFlow from the NodeInstance list
        self.initial_nodes += [
                str([
                    {
                        "id":node.name,
                        "type":'panelWidget',
                        "position":{"x":node.x,"y":node.y},
                        "data":{"label":node.node.node_class_name}
                    }
                    for node in initial_nodes
                ])
            ]

        # Creating the dictionnaries for ReactFlow from the EdgeInstance list
        self.initial_edges += [ 
                str([
                    self._edge_to_string(edge)
                    for edge in initial_edges
                ])
            ]
        
        # These two dictionnaries will help understanding the node graph changes
        self.old_nodes = {}
        self.old_edges = {}

        # Monitoring nodes and edges to trigger functions on graph change
        self.param.watch(self.update_nodes, "nodes")
        self.param.watch(self.update_nodes, "edges")

        self.edge_selection_callback = None
        """Function called when an edge is selected, can be set by calling set_on_edge_selection"""
        self.edge_deselection_callback = None
        """Function called when an edge is deselected, can be set by calling set_on_edge_deselection"""

    def _edge_to_string(self, edge:EdgeInstance):
        """Checks the EdgeInstance and prepares the dictionnary understood by reactflow

        Parameters
        ----------
        edge : EdgeInstance
            Edge to add in the initial graph

        Returns
        -------
        Dict[str, Any]
            Edge property

        Raises
        ------
        ValueError
            Source or target node unknown
        ValueError
            Source or target handle not registered in the associated node
        ValueError
            Incompatible handles restrictions
        """
        source_node = [n for n in self.nodes_instances if n.name == edge.source]
        target_node = [n for n in self.nodes_instances if n.name == edge.target]

        if len(source_node) ==0:
            raise ValueError(f"Provided EdgeInstance starts from a node {edge.source} that was not provided in the NodeInstance list.")
        if len(target_node) ==0:
            raise ValueError(f"Provided EdgeInstance ends at a node {edge.target} that was not provided in the NodeInstance list.")
        
        source_node = source_node[0]
        target_node = target_node[0]

        source_port = [p for p in source_node.ports if p.name == edge.source_handle]
        target_port = [p for p in target_node.ports if p.name == edge.target_handle]

        if len(source_port) ==0:
            raise ValueError(f"Provided EdgeInstance starts from a port {edge.source_handle} at node {edge.source} that is not in the ports list.")
        if len(target_port) ==0:
            raise ValueError(f"Provided EdgeInstance ends at a port {edge.target_handle} at node {edge.target} that is not in the ports list.")
        
        source_port = source_port[0]
        target_port = target_port[0]

        edge_dict = {
            "source": edge.source,
            "sourceHandle": edge.source_handle,
            "target": edge.target,
            "targetHandle": edge.target_handle,
            "id": "_".join([edge.source, edge.source_handle, edge.target, edge.target_handle]),
        }

        if source_port.restriction is  None and target_port.restriction is not None:
            raise ValueError("Tried plugging ports that have different restrictions, found:\n" \
            f"Node {edge.source} - Port {edge.source_handle} : No restriction found\n" \
            f"Node {edge.target} - Port {edge.target_handle} : Restriction {target_port.restriction.name}\n")
        
        if source_port.restriction is not None and target_port.restriction is None:
            raise ValueError("Tried plugging ports that have different restrictions, found:\n" \
            f"Node {edge.source} - Port {edge.source_handle} : Restriction {source_port.restriction.name}\n" \
            f"Node {edge.target} - Port {edge.target_handle} : No restriction found\n")

        if source_port.restriction is not None and \
            target_port.restriction is not None and \
            (not source_port.restriction.name == target_port.restriction.name):
            raise ValueError("Tried plugging ports that have different restrictions, found:\n" \
            f"Node {edge.source} - Port {edge.source_handle} : Restriction {source_port.restriction.name}\n" \
            f"Node {edge.target} - Port {edge.target_handle} : Restriction {target_port.restriction.name}\n")

        if source_port.restriction is not None:
            edge_dict["style"] = {"stroke":source_port.restriction.color}

        return edge_dict

    def _handle_msg(self, data:Dict[str, Any]):
        """Handle the message received from the ReactFlow JavaScript.

        Parameters
        ----------
        data : Dict[str, Any]
            Message content
        """
        action = data["action"]

        if action == "NEW_NODE":
            node_id= data["node_id"]
            node_type= data["type"]
            x= data["x"]
            y= data["y"]

            for c in self.nodes_classes:
                if c.node_class_name == node_type:
                    print(f"Creating node of type {node_type}")

                    node = c()
                    node.name = f"{node_id}"
                    node_instance = NodeInstance(f"{node_id}", node, x, y)
                    self.add_node(node_instance)
                    

    def print_state(self, _=None):
        """Printing the list of nodes

        Parameters
        ----------
        _ : Any, optional
            Event triggering the function call, by default None
        """
        print("\n\nPrinting nodes")
        
        for node in self.nodes:
            print(node)

        print("\n\nPrinting edges")
        for edge in self.edges:
            print(edge)

        self.nodes = [e for e in self.nodes]
        self.edges = [e for e in self.edges]
            
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
            len([nc for nc in node_changes if type(nc) in [EdgeCreation, EdgeDeletion]]) > 0:
            self._build_node_tree()

            self.nodes_instances = [node for node in self.nodes_instances if node.name in list(n["id"] for n in self.nodes)]

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

        # Storing the current node and edge state for next call
        self.old_nodes = node_dict
        self.old_edges = edge_dict
         
    def _build_node_tree(self,):
        """Provides to the nodes who is plugged to them for the nodes updates
        """
        print("Building tree")
        for node in self.nodes_instances:
            node.plugged_nodes = {port.name : [] for port in node.ports}

        # Removing edges of the nodes that could have been removed in the event triggering the node tree building
        self.edges = [e for e in self.edges if e["source"] in self.item_names and e["target"] in self.item_names]

        for edge in self.edges:
            source_node = [node for node in self.nodes_instances if node.name == edge["source"]][0]
            target_node = [node for node in self.nodes_instances if node.name == edge["target"]][0]

            source_port_name = edge["sourceHandle"]
            target_port_name = edge["targetHandle"]

            source_node.plugged_nodes[source_port_name].append(target_node)
            target_node.plugged_nodes[target_port_name].append(source_node)

    def add_node(self, node:NodeInstance):
        """Storing the informations of a nodes in the class attributes

        Parameters
        ----------
        node : NodeInstance
            Node to store
        """
        print(f"Adding node {node.name} at ({node.x}, {node.y})")
        node.node.name = node.name
        self.nodes_instances.append(node.node)

        self.items = self.items + [node.node.create()]
        self.item_names = self.item_names + [node.name]
        self.item_ports = self.item_ports + [[
                                                [
                                                    p.direction.value, 
                                                    p.position.value, 
                                                    p.name, 
                                                    p.display_name, 
                                                    p.offset, 
                                                    p.connection_count_limit,
                                                    p.restriction.name if p.restriction is not None else None,  
                                                    p.restriction.color if p.restriction is not None else None,  
                                                ] for p in node.node.ports]]

        self._send_event(ESMEvent, data={
                                            "action":f"NodeCreation",
                                            "node_name":node.name,
                                            "x":node.x,
                                            "y":node.y,
                                            "node_class_name":node.node.node_class_name
                                         })

    def remove_nodes(self, nodes:List[str]):
        """Removes the given nodes from the graph

        Parameters
        ----------
        nodes : List[str]
            List of nodes names to remove
        """
        for node in nodes:
            if not node in self.item_names:
                raise ValueError(f"Node {node} deletion requested, node name unknown.")
            
        self._send_event(ESMEvent, data={
                                            "action":f"NodesRemoval",
                                            "nodes_names":nodes,
                                         })
        
        for node in nodes:
            node_index = self.item_names.index(node)

            self.items.pop(node_index)
            self.item_names.pop(node_index)
            self.item_ports.pop(node_index)

    def remove_edges(self, edges:List[EdgeInstance]):
        """Removes the given edges from the graph

        Parameters
        ----------
        nodes : List[EdgeInstance]
            List of edges to remove
        """
        for edge in edges:
            if not edge in self.get_edges():
                raise ValueError(f"Edge {edge} not in the current edges list.")
            
            
        # self._send_event(ESMEvent, data={
        #                                     "action":f"NodesRemoval",
        #                                     "nodes_names":nodes,
        #                                  })
        
        # for node in nodes:
        #     node_index = self.item_names.index(node)

        #     self.items.pop(node_index)
        #     self.item_names.pop(node_index)
        #     self.item_ports.pop(node_index)

    def clear(self,):
        """Clears the node graph.
        """
        self.remove_edges(list(self.edges))
        self.remove_nodes(list(self.item_names))

    def _check_node_change(self, new_node_dict:Dict[str, Any]) -> List[NodeChange] :
        """Checks if and what changed in the nodes list

        Parameters
        ----------
        new_node_dict : Dict[str, Any]
            Dictionnary containing the nodes parameters for each node name

        Returns
        -------
        List[NodeChange] 
            List of node changes
        """
        node_changes:List[NodeChange] = []
        for node in new_node_dict:
            if not node in self.old_nodes:
                node_changes.append(NodeCreation(node))

        for node in self.old_nodes:
            if node in new_node_dict:
                new = new_node_dict[node]
                old = self.old_nodes[node]

                if old["position"]["x"] != new["position"]["x"] or\
                        old["position"]["y"] != new["position"]["y"]:
                    node_changes.append(NodeMove(node, new["position"]["x"], new["position"]["y"], old["position"]["x"], old["position"]["y"]))
                if "selected" in new:
                    if new["selected"]:
                        if (not "selected" in old) or not old["selected"]:
                            node_changes.append(NodeSelected(node))
                    else:
                        if "selected" in old and old["selected"]:
                            node_changes.append(NodeDeselected(node))

            else:
                node_changes.append(NodeDeletion(node))
        
        return node_changes

    def _check_edge_change(self, new_edge_dict:Dict[str, Any]) -> List[EdgeChange] :
        """Checks if and what changed in the edges list

        Parameters
        ----------
        new_edge_dict : Dict[str, Any]
            Dictionnary containing the edges parameters for each edge name

        Returns
        -------
        List[EdgeChange]
            List of edge changes
        """
        edge_changes:List[NodeChange] = []

        for edge in new_edge_dict:
            if not edge in self.old_edges:
                e = new_edge_dict[edge]
                edge_changes.append(EdgeCreation(e["source"], e["sourceHandle"], e["target"], e["targetHandle"]))

        for edge in self.old_edges:
            if edge in new_edge_dict:
                new = new_edge_dict[edge]
                old = self.old_edges[edge]

                if "selected" in new:
                    if new["selected"]:
                        if (not "selected" in old) or not old["selected"]:
                            edge_changes.append(EdgeSelected(old["source"], old["sourceHandle"], old["target"], old["targetHandle"]))
                    else:
                        if "selected" in old and old["selected"]:
                            edge_changes.append(EdgeDeselected(old["source"], old["sourceHandle"], old["target"], old["targetHandle"]))

            else:
                e = self.old_edges[edge]
                edge_changes.append(EdgeDeletion(e["source"], e["sourceHandle"], e["target"], e["targetHandle"]))
        
        print(edge_changes)
        return edge_changes
    
    def get_nodes(self,) -> List[NodeInstance]:
        """Returns the nodes list

        Returns
        -------
        List[NodeInstance]
            Current nodes list
        """
        return list(self.nodes_instances)
        
    def get_edges(self,) -> List[EdgeInstance]:
        """Returns the nodes list

        Returns
        -------
        List[NodeInstance]
            Current nodes list
        """
        return [EdgeInstance(e["source"], e["sourceHandle"], e["target"], e["targetHandle"]) for e in self.edges]
        
    def set_on_edge_selection(self, callback:Callable):
        """Sets the function called when an edge is selected

        Parameters
        ----------
        callback : Callable
            Function called
        """
        self.edge_selection_callback = callback
        
        
    def set_on_edge_deselection(self, callback:Callable):
        """Sets the function called when an edge is deselected

        Parameters
        ----------
        callback : Callable
            Function called
        """
        self.edge_deselection_callback = callback

if __name__ == "__main__":
    class FloatInputNode(ReactFlowNode):
        node_class_name = "Float Input"
        ports:List[NodePort] = [NodePort(direction=PortDirection.OUTPUT, position=PortPosition.RIGHT, name="output")]

        def __init__(self, ):
            super().__init__()
            self.float_input = pn.widgets.FloatInput(value=0., width=100)
            
            self.float_input.param.watch(self.update, "value")

        def create(self, ):
            return pn.layout.Column(
                                        self.float_input, 
                                        name=self.name, 
                                        align="center"
                                    )
        
        def update(self, _):
            super().update(_)

        def get_node_json_value(self) -> Dict[str, Any]:
            return {"value" : self.float_input.value}

    class ResultNode(ReactFlowNode):
        node_class_name = "Result"
        ports:List[NodePort] = [NodePort(direction=PortDirection.INPUT, position=PortPosition.LEFT, name="input")]

        def __init__(self, ):
            super().__init__()
            self.result_label = pn.pane.Markdown("Result : Undefined")

        def create(self, ):
            return pn.layout.Column(
                                        self.result_label, 
                                        name=self.name, 
                                        align="center"
                                    )
        
        def update(self, _):
            value = 0

            if "input" in self.plugged_nodes :
                if len(self.plugged_nodes["input"]) == 0:
                    self.result_label.object = f"Result : Undefined"
                else:
                    for float_input in self.plugged_nodes["input"]:
                        value += float_input.get_node_json_value()["value"]

                    self.result_label.object = f"Addition result : {round(value, 1)}"
                super().update(_)

        def get_node_json_value(self) -> Dict[str, Any]:
            return {"value" : self.result_label.object}


    def make_reactflow():
        rf1 = ReactFlow(nodes_classes = [FloatInputNode, ResultNode],
                        initial_nodes=[],
                        initial_edges=[])

        return rf1

    rf = make_reactflow()
    pn.Column(rf).show()
