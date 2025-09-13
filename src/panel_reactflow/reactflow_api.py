
from dataclasses import dataclass
from enum import Enum
import panel as pn
from typing import Any, Dict, List, Union

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

@dataclass
class PortRestriction:
    name:str
    """Name of the restriction type"""
    color:str = "#000"
    """HTML color code of the restriction"""

class NodePort:
    def __init__(self, 
                    direction:PortDirection, 
                    position:PortPosition, 
                    name:str, 
                    display_name:bool = False,
                    offset:float = None,
                    connection_count_limit:int = None,
                    restriction:PortRestriction = None):
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
        connection_count_limit : int, optional
            How many edges can be connected to the port. Defaults to None, by default None
        restriction : PortRestriction, optional
            Restriction of what can be plugged to the current port. Defaults to None, by default None
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
        self.connection_count_limit:int = connection_count_limit
        """How many edges can be connected to the port."""
        self.restriction:PortRestriction = restriction
        """Restriction of what can be plugged to the current port."""

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
    
class Node:
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

    def to_reactflow(self, ) -> Dict[str, Union[str, Dict[str, Any]]]:
        """Convert self to reactflow dict

        Returns
        -------
        Dict[str, Union[str, Dict[str, Any]]]
            reactflow readable dictionnary
        """
        return{
                    "id":self.name,
                    "type":'panelWidget',
                    "position":{"x":self.x,"y":self.y},
                    "data":{"label":self.node.node_class_name}
                }
    
class Edge:
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

    def __eq__(self, other:"Edge"):
        if not isinstance(other, Edge):
            return False
        
        return self.source == other.source \
                and self.source_handle == other.source_handle \
                and self.target == other.target \
                and self.target_handle == other.target_handle
    
    def __hash__(self):
        return hash(self.source+self.source_handle+self.target+self.target_handle)
        