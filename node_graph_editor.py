
import functools
from typing import List, Dict, Any
import panel as pn

from reactflow_api import EdgeSelected, EdgeDeselected, NodeInstance, ReactFlowNode, PortDirection, PortPosition, NodePort
from reactflow import ReactFlow

class NodeClass(ReactFlowNode):
    node_class_name = "Result"
    ports:List[NodePort] = [NodePort(direction=PortDirection.INPUT, position=PortPosition.LEFT, name="input"),
                            NodePort(direction=PortDirection.OUTPUT, position=PortPosition.RIGHT, name="input")]
    
    def __init__(self, node_editor:"NodesEditor"):
        self.name = ""
        self.node_editor:NodesEditor = node_editor

    def create(self, ) -> pn.viewable.Viewable:
        """Function called by the Reactflow class to instanciate the content of the node
        """
        return pn.pane.Markdown(f"Node {self.name}")

    def update(self, _):
        """Update the node content based on the input ports.

        Parameters
        ----------
        _ : Any
            Event requesting the update
        """
        pass
    
    def get_node_json_value(self,) -> Dict[str, Any]:
        """ Returns a dictionnary describing the node content, this dictionnary can be obtain by other nodes in their update call.
        
        Returns
        ----------
        Dict[str, Any]
            Node properties
        """
        return {}
    
    def on_node_selected(self, ):
        """Function triggered when a node is selected
        """
        print(f"Node selected : {self.name}")
        self.node_editor.selected_nodes.append(self.name)
        self.node_editor.update_information()
    
    def on_node_deselected(self, ):
        """Function triggered when a node is deselected
        """
        self.node_editor.selected_nodes.remove(self.name)
        self.node_editor.update_information()

class NodesEditor:
    def __init__(self):
        
        class ClassWithNodeEditor(NodeClass):
            __init__ = functools.partialmethod(NodeClass.__init__, node_editor = self)

        self.rf = ReactFlow(nodes_classes = [ClassWithNodeEditor])
        self.rf.set_on_edge_deselection(self.on_edge_deselection)
        self.rf.set_on_edge_selection(self.on_edge_selection)

        self.current_node_index = 0

        def add_new_node(event):
            print("Adding node", f"node_{self.current_node_index}")
            self.rf.add_node(NodeInstance(f"node_{self.current_node_index}", ClassWithNodeEditor(), 0., 0.))
            self.current_node_index += 1
        
        def remove_selected_nodes(event):
            print(f"Removing nodes: {self.selected_nodes}")
        
        self.add_node_button = pn.widgets.Button(name="Add node")
        self.remove_node_button = pn.widgets.Button(name="Remove node")

        self.add_node_button.on_click(add_new_node)
        self.remove_node_button.on_click(remove_selected_nodes)

        self.selected_nodes = []
        self.selected_edges = []

        self.information_pane = pn.pane.Markdown("Selected nodes : \n\nSelected edges : \n\n")

        self.layout = pn.Row(self.rf, pn.Column(self.information_pane, pn.layout.Divider(), self.add_node_button, self.remove_node_button, width = 250))

    def update_information(self,):
        self.information_pane.object = "Selected nodes :\n" + "\n".join([f"- {e}" for e in self.selected_nodes]) +"\n\n"+\
                                         "Selected edges :\n" + "\n".join([f"- {e}" for e in self.selected_edges])+"\n\n"

    def on_edge_selection(self, es:EdgeSelected):
        self.selected_edges.append((es.source, es.target))
        self.update_information()

    def on_edge_deselection(self, es:EdgeDeselected):
        self.selected_edges.remove((es.source, es.target))
        self.update_information()


ne = NodesEditor()
ne.layout.show()