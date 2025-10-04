
import functools
from typing import List, Dict, Any
import panel as pn
import panel_material_ui as pmui

from panel_reactflow.api import Edge, Node, PortDirection, PortPosition, NodePort, ReactFlowNode
from panel_reactflow.events import EdgeSelected, EdgeDeselected, NodeSelected, NodeDeselected
from panel_reactflow.reactflow import ReactFlowGraph

class NodeClass(ReactFlowNode):
    node_class_name = "Result"
    ports:List[NodePort] = [NodePort(direction=PortDirection.INPUT, position=PortPosition.LEFT, name="input"),
                            NodePort(direction=PortDirection.OUTPUT, position=PortPosition.RIGHT, name="output")]
    
    def __init__(self, node_editor:"NodesEditor"):
        self.name = ""
        self.node_editor:NodesEditor = node_editor

    def create(self, ) -> pn.viewable.Viewable:
        """Function called by the Reactflow class to instanciate the content of the node
        """
        return pn.pane.Markdown(f"Node {self.name}")

class NodesEditor:
    def __init__(self):
        
        class ClassWithNodeEditor(NodeClass):
            __init__ = functools.partialmethod(NodeClass.__init__, node_editor = self)

        self.rf = ReactFlowGraph(nodes_classes = [ClassWithNodeEditor])
        self.rf.on_event(EdgeDeselected, self.on_edge_deselection)
        self.rf.on_event(EdgeSelected, self.on_edge_selection)
        self.rf.on_event(NodeDeselected, self.on_node_deselection)
        self.rf.on_event(NodeSelected, self.on_node_selection)

        self.current_node_index = 0

        def add_new_node(event):
            print("Adding node", f"node_{self.current_node_index}")
            self.rf.add_node(Node(f"node_{self.current_node_index}", ClassWithNodeEditor(), 0., 0.))
            self.current_node_index += 1
        
        def remove_selected_nodes(event):
            print(f"Removing nodes: {self.selected_nodes}")
            self.rf.remove_nodes(self.selected_nodes)
            self.selected_nodes.clear()
            self.update_information()
        
        def clear(event):
            print("Clearing nodes")
            self.rf.clear()
            self.selected_edges.clear()
            self.selected_nodes.clear()
            self.update_information()
            self.current_node_index = 0
        
        def remove_selected_edges(event):
            print(f"Removing edges: {self.selected_edges}")
            self.rf.remove_edges([Edge(*e) for e in self.selected_edges])
            self.selected_edges.clear()
            self.update_information()
        
        def add_new_edge(event):
            if len(self.selected_nodes) > 1:
                print(f"Adding edge from ({self.selected_nodes[0]}, output) to ({self.selected_nodes[1]}, input).")
                self.rf.add_edges([Edge(self.selected_nodes[0], "output", self.selected_nodes[1], "input")])
                self.current_node_index += 1
            else:
                print("Select two nodes to add an edge")
        
        self.add_node_button = pmui.Button(name="Add node")
        self.remove_node_button = pmui.Button(name="Remove selected nodes")
        
        self.add_edge_button = pmui.Button(name="Add edge between nodes")
        self.remove_edge_button = pmui.Button(name="Remove selected edges")
        
        self.clear_button = pmui.Button(name="Clear graph")

        self.add_node_button.on_click(add_new_node)
        self.remove_node_button.on_click(remove_selected_nodes)
        self.clear_button.on_click(clear)

        self.add_edge_button.on_click(add_new_edge)
        self.remove_edge_button.on_click(remove_selected_edges)

        self.selected_nodes = []
        self.selected_edges = []

        self.information_pane = pn.pane.Markdown("Selected nodes : \n\nSelected edges : \n\n")

        self.layout = pn.Row(self.rf, pn.Column(self.information_pane, 
                                                
                                                pn.layout.Divider(), 
                                                
                                                self.add_node_button, self.remove_node_button, 
                                                
                                                pn.layout.Divider(), 
                                                
                                                self.add_edge_button, self.remove_edge_button, 

                                                pn.layout.Divider(), 
                                                
                                                self.clear_button, 

                                                width = 250))

    def update_information(self,):
        self.information_pane.object = "Selected nodes :\n" + "\n".join([f"- {e}" for e in self.selected_nodes]) +"\n\n"+\
                                         "Selected edges :\n" + "\n".join([f"- {e}" for e in self.selected_edges])+"\n\n"

    def on_node_selection(self, es:NodeSelected):
        print("Selected edge")
        self.selected_nodes.append(es.node_name)
        self.update_information()

    def on_node_deselection(self, es:NodeDeselected):
        print("Selected edge")
        if es.node_name in self.selected_nodes:
            self.selected_nodes.remove(es.node_name)
        self.update_information()

    def on_edge_selection(self, es:EdgeSelected):
        print("Selected edge")
        self.selected_edges.append((es.source, es.source_handle, es.target, es.target_handle))
        self.update_information()

    def on_edge_deselection(self, es:EdgeDeselected):
        self.selected_edges.remove((es.source, es.source_handle, es.target, es.target_handle))
        self.update_information()


ne = NodesEditor()

pmui.Page(main=[ne.layout]).show()