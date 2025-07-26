
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
                        Path("dnd_flow.css"),
                    ]
    """CSS elements to customize the graph appearance"""
    
    _esm = Path(__file__).parent / "reactflow.js"
    """Javascrip file containing the reactflow graph definition"""

    def __init__(self, 
                    sizing_mode = "stretch_both", 
                    nodes_classes:List[Type[ReactFlowNode]] = [], 
                    initial_nodes:List[NodeInstance] = [],
                    initial_edges:List[EdgeInstance] = [],
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
        """
        
        super().__init__(sizing_mode=sizing_mode, **kwargs)

        self.nodes_classes = nodes_classes
        self.node_class_labels = [c.node_class_name for c in self.nodes_classes]

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
                    {
                        "source": edge.source,
                        "sourceHandle": edge.source_handle,
                        "target": edge.target,
                        "targetHandle": edge.target_handle,
                        "id": "_".join([edge.source, edge.source_handle, edge.target, edge.target_handle]),
                    }
                    for edge in initial_edges
                ])
            ]
        
        # These two dictionnaries will help understanding the node graph changes
        self.old_nodes = {}
        self.old_edges = {}

        # Monitoring nodes and edges to trigger functions on graph change
        self.param.watch(self.update_nodes, "nodes")
        self.param.watch(self.update_nodes, "edges")

    def _handle_msg(self, data:str):
        """Handle the message received from the ReactFlow JavaScript.

        Parameters
        ----------
        data : str
            Message content
        """
        if data.startswith("NEW_NODE"):
            _, node_id, node_type = data.split(":")

            new_item = None
            for c in self.nodes_classes:
                if c.node_class_name == node_type:
                    print(f"Creating node of type {node_type}")

                    node = c()
                    node.name = f"{node_id}"
                    new_item = node.create()
                    
                    self.nodes_instances.append(node)
                    
                    self.items = self.items + [new_item]
                    self.item_names = self.item_names + [node_id]
                    self.item_ports = self.item_ports + [[[p.direction.value, p.position.value, p.name, p.display_name, p.offset] for p in c.ports]]

                    node.update()
                    

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
        
        if len([nc for nc in node_changes if type(nc) in [NodeCreation, NodeDeletion]]) > 0:
            self.build_node_tree()

            self.nodes_instances = [node for node in self.nodes_instances if node.name in list(n["id"] for n in self.nodes)]

        for node_change in node_changes:
            if isinstance(node_changes, NodeCreation):
                self.nodes_instances[self.item_names.index(node_change)].update(None)
            elif isinstance(node_changes, NodeMove):
                self.nodes_instances[self.item_names.index(node_change)].on_node_move(node_change)
            elif isinstance(node_changes, NodeSelected):
                self.nodes_instances[self.item_names.index(node_change)].on_node_selected()
            elif isinstance(node_changes, NodeDeselected):
                self.nodes_instances[self.item_names.index(node_change)].on_node_deselected()

        for edge_change in edge_changes:
            if isinstance(edge_change, EdgeCreation):
                self.build_node_tree()
                self.nodes_instances[self.item_names.index(edge_change.target)].update(None)
            elif isinstance(edge_change, EdgeDeletion):
                self.build_node_tree()
                self.nodes_instances[self.item_names.index(edge_change.target)].update(None)

        # Storing the current node and edge state for next call
        self.old_nodes = node_dict
        self.old_edges = edge_dict
         
    def build_node_tree(self,):
        """Provides to the nodes who is plugged to them for the nodes updates
        """
        for node in self.nodes_instances:
            node.plugged_nodes = {port.name : [] for port in node.ports}

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
        node.node.name = node.name
        self.nodes_instances.append(node.node)

        self.items = self.items + [node.node.create()]
        self.item_names = self.item_names + [node.node.name]
        self.item_ports = self.item_ports + [[[p.direction.value, p.position.value, p.name, p.display_name, p.offset] for p in node.node.ports]]

        self._send_event(ESMEvent, data=f"NodeCreation@{node.name}@{node.x}@{node.y}@{node.node.node_class_name}")

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
        
        return edge_changes
        

if __name__ == "__main__":
    class FloatInputNode(ReactFlowNode):
        node_class_name = "Float Input"
        ports:List[NodePort] = [NodePort(direction=PortDirection.OUTPUT, position=PortPosition.BOTTOM, name="output")]

        def __init__(self, ):
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

        def get_node_json_value(self):
            return {"value" : self.float_input.value}

    class ResultNode(ReactFlowNode):
        node_class_name = "Result"
        ports:List[NodePort] = [NodePort(direction=PortDirection.INPUT, position=PortPosition.TOP, name="input")]

        def __init__(self, ):
            self.result_label = pn.pane.Markdown("Result : Undefined")

        def create(self, ):
            return pn.layout.Column(
                                        self.result_label, 
                                        name=self.name, 
                                        align="center"
                                    )
        
        def update(self, _):
            value = 0

            if len(self.plugged_nodes["input"]) == 0:
                self.result_label.object = f"Result : Undefined"
            else:
                for float_input in self.plugged_nodes["input"]:
                    value += float_input.get_node_json_value()["value"]

                self.result_label.object = f"Addition result : {round(value, 1)}"
            super().update(_)

        def get_node_json_value(self):
            return {"value" : self.result_label.object}


    def make_reactflow():
        rf1 = ReactFlow(nodes_classes = [FloatInputNode, ResultNode])

        return rf1

    make_reactflow().show()