
from enum import Enum
import panel as pn
from typing import Callable, Dict, List

class PortDirection(Enum):
    """Whether the port is an input or output. The update function will spread through output ports."""
    INPUT=0
    OUTPUT=1

class PortPosition(Enum):
    """Position of the port around the node."""
    TOP=0
    BOTTOM=1
    RIGHT=2
    LEFT=3

class NodePort:
    def __init__(self, 
                    direction:PortDirection, 
                    position:PortPosition, 
                    name:str, 
                    display_name:bool = False,
                    offset:float = None):
        """Node port class constructor : stores the information for each port of a node.

        Parameters
        ----------
        direction : PortDirection
            Whether the port represents an input or an output
        position : PortPosition
            Location of the port around the node : BOTTOM, TOP, LEFT or RIGHT
        name : str
            Port name
        display_name : bool, optional
            Display the port name on the node (only available for LEFT and RIGHT ports). Defaults to False., by default False
        offset : float, optional
            Port position offset to the top/left based on the position. If None, the port will be centered to the edge. Defaults to None, by default None
        """        
        assert not (display_name and position in [PortPosition.TOP, PortPosition.BOTTOM]), "Node port name can only be displayed if located on left or right."
        assert not (display_name and offset is None), "Node port name can only be displayed if the port offset is provided."

        self.direction:PortDirection = direction
        """Whether the port represents an input or an output"""
        self.position:PortPosition = position
        """Location of the port around the node : BOTTOM, TOP, LEFT or RIGHT"""
        self.name:str = name
        """Port name"""
        self.display_name:bool = display_name
        """Display the port name on the node (only available for LEFT and RIGHT ports)"""
        self.offset:float = offset
        """Port position offset to the top/left based on the position. If None, the port will be centered to the edge."""



class NodeChange:
    """Class defining any node change occuring in the graph."""
    def __init__(self, name:str):
        self.node_name = name

class NodeCreation(NodeChange):
    """Class defining a node creation."""
    def __init__(self, name:str):
        """Class defining a node creation.

        Parameters
        ----------
        name : str
            Created node name
        """
        super().__init__(name)
    
    def __repr__(self):
        return f"Node created : {self.node_name}"

class NodeDeletion(NodeChange):
    """Class defining a node deletion."""
    def __init__(self, name:str):
        """Class defining a node deletion.

        Parameters
        ----------
        name : str
            Deleted node name
        """
        super().__init__(name)
    
    def __repr__(self):
        return f"Node deleted : {self.node_name}"

class NodeMove(NodeChange):
    """Class defining a node movement."""
    def __init__(self, name:str, new_x:float, new_y:float, old_x:float, old_y:float):
        """Description of a node movement.

        Parameters
        ----------
        name : str
            Moved node name
        new_x : float
            New X coordinate in the graph
        new_y : float
            Nez Y coordinate in the graph
        old_x : float
            Old X coordinate in the graph
        old_y : float
            Old Y coordinate in the graph
        """
        super().__init__(name)
        self.new_x = new_x
        """New X coordinate in the graph"""
        self.new_y = new_y
        """Nez Y coordinate in the graph"""
        self.old_x = old_x
        """Old X coordinate in the graph"""
        self.old_y = old_y
        """Old Y coordinate in the graph"""
    
    def __repr__(self):
        return f"Node {self.node_name} moved from ({self.old_x}, {self.old_y}) to ({self.new_x}, {self.new_y})"

class NodeSelected(NodeChange):
    """Class defining a node selection."""
    def __init__(self, name:str):
        """Class defining a node selection.

        Parameters
        ----------
        name : str
            Selected node name
        """
        super().__init__(name)

    def __repr__(self):
        return f"Node selected : {self.node_name}"

class NodeDeselected(NodeChange):
    """Class defining a node deselection."""
    def __init__(self, name:str):
        """Class defining a node deselection.

        Parameters
        ----------
        name : str
            Deselected node name
        """
        super().__init__(name)
    
    def __repr__(self):
        return f"Node deselected : {self.node_name}"

class EdgeChange:
    """Class defining any edge change occuring in the graph."""
    def __init__(self, source:str, source_handle:str, target:str, target_handle:str):
        """Class defining any edge change occuring in the graph.

        Parameters
        ----------
        source : str
            Source node name
        source_handle : str
            Source port name
        target : str
            Target node name
        target_handle : str
            Target port name
        """
        self.source = source
        """Node name from which the edge starts"""
        self.source_handle = source_handle
        """Plugged port name in the source node"""
        self.target = target
        """Node name in which the edge ends"""
        self.target_handle = target_handle
        """Plugged port name in the target node"""

class EdgeCreation(EdgeChange):
    """Class defining a edge creation."""
    def __init__(self, source:str, source_handle:str, target:str, target_handle:str):
        """Class defining a edge creation.

        Parameters
        ----------
        source : str
            Source node name
        source_handle : str
            Source port name
        target : str
            Target node name
        target_handle : str
            Target port name
        """
        super().__init__(source, source_handle, target, target_handle)
    
    def __repr__(self):
        return f"Edge created : from {self.source} - {self.source_handle} to {self.target} - {self.target_handle}"

class EdgeDeletion(EdgeChange):
    """Class defining a edge deletion."""
    def __init__(self, source:str, source_handle:str, target:str, target_handle:str):
        """Class defining a edge deletion.

        Parameters
        ----------
        source : str
            Source node name
        source_handle : str
            Source port name
        target : str
            Target node name
        target_handle : str
            Target port name
        """
        super().__init__(source, source_handle, target, target_handle)
    
    def __repr__(self):
        return f"Edge deleted : from {self.source} - {self.source_handle} to {self.target} - {self.target_handle}"

class EdgeSelected(EdgeChange):
    """Class defining a edge selection."""
    def __init__(self, source:str, source_handle:str, target:str, target_handle:str):
        """Class defining a edge selection.

        Parameters
        ----------
        source : str
            Source node name
        source_handle : str
            Source port name
        target : str
            Target node name
        target_handle : str
            Target port name
        """
        super().__init__(source, source_handle, target, target_handle)
    
    def __repr__(self):
        return f"Edge selected : from {self.source} - {self.source_handle} to {self.target} - {self.target_handle}"

class EdgeDeselected(EdgeChange):
    """Class defining a edge deselection."""
    def __init__(self, source:str, source_handle:str, target:str, target_handle:str):
        """Class defining a edge deselection.

        Parameters
        ----------
        source : str
            Source node name
        source_handle : str
            Source port name
        target : str
            Target node name
        target_handle : str
            Target port name
        """
        super().__init__(source, source_handle, target, target_handle)
    
    def __repr__(self):
        return f"Edge deselected : from {self.source} - {self.source_handle} to {self.target} - {self.target_handle}"


class ReactFlowNode:
    node_class_name = ""
    """Node class name, as it will appear in the reactflow side bar."""
    ports:List[NodePort]
    """List of node ports"""
    plugged_nodes:Dict[str, List['ReactFlowNode']]
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
        for port in self.ports:
            if port.direction == PortDirection.OUTPUT and port.name in self.plugged_nodes:
                for node in self.plugged_nodes[port.name]:
                    node.update(_)
    
    def get_node_json_value(self,):
        """ Returns a dictionnary describing the node content, this dictionnary can be obtain by other nodes in their update call.
        
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

class NodeInstance:
    def __init__(self, 
                    name:str, 
                    node:ReactFlowNode, 
                    x:float, 
                    y:float,):
        """Node that is created when opening the app

        Parameters
        ----------
        name : str
            Node name
        node_type : ReactFlowNode
            Class of the node
        x : float
            Horizontal position in graph
        y : float
            Vertical position in graph
        """
        self.name = name
        """Node name"""
        self.node = node
        """Already instanciated node"""
        self.x = x
        """Node X coordinate in the graph"""
        self.y = y
        """Node Y coordinate in the graph"""

class EdgeInstance:
    def __init__(self, 
                    source:str, 
                    source_handle:str, 
                    target:str, 
                    target_handle:str,):
        """Edge that is created when opening the app

        Parameters
        ----------
        source : str
            Source node name
        source_handle : str
            Source port name
        target : str
            Target node name
        target_handle : str
            Target port name
        """
        self.source = source
        """Node name from which the edge starts"""
        self.source_handle = source_handle
        """Plugged port name in the source node"""
        self.target = target
        """Node name in which the edge ends"""
        self.target_handle = target_handle
        """Plugged port name in the target node"""

