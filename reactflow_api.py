
from enum import Enum
import panel as pn
from typing import Callable, Dict, List

class PortDirection(Enum):
    INPUT=0
    OUTPUT=1

class PortPosition(Enum):
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
    def __init__(self, name:str):
        self.node_name = name

class NodeCreation(NodeChange):
    def __init__(self, name:str):
        super().__init__(name)
    
    def __repr__(self):
        return f"Node created : {self.node_name}"

class NodeDeletion(NodeChange):
    def __init__(self, name:str):
        super().__init__(name)
    
    def __repr__(self):
        return f"Node deleted : {self.node_name}"

class NodeMove(NodeChange):
    def __init__(self, name:str, new_x:float, new_y:float, old_x:float, old_y:float):
        super().__init__(name)
        self.new_x = new_x
        self.new_y = new_y
        self.old_x = old_x
        self.old_y = old_y
    
    def __repr__(self):
        return f"Node {self.node_name} moved from ({self.old_x}, {self.old_y}) to ({self.new_x}, {self.new_y})"

class NodeSelected(NodeChange):
    def __init__(self, name:str):
        super().__init__(name)

    def __repr__(self):
        return f"Node selected : {self.node_name}"

class NodeDeselected(NodeChange):
    def __init__(self, name:str):
        super().__init__(name)
    
    def __repr__(self):
        return f"Node deselected : {self.node_name}"

class EdgeChange:
    def __init__(self, source:str, source_handle:str, target:str, target_handle:str):
        self.source:str = source
        self.source_handle:str = source_handle
        self.target:str = target
        self.target_handle:str = target_handle

class EdgeCreation(EdgeChange):
    def __init__(self, source:str, source_handle:str, target:str, target_handle:str):
        super().__init__(source, source_handle, target, target_handle)
    
    def __repr__(self):
        return f"Edge created : from {self.source} - {self.source_handle} to {self.target} - {self.target_handle}"

class EdgeDeletion(EdgeChange):
    def __init__(self, source:str, source_handle:str, target:str, target_handle:str):
        super().__init__(source, source_handle, target, target_handle)
    
    def __repr__(self):
        return f"Edge deleted : from {self.source} - {self.source_handle} to {self.target} - {self.target_handle}"

class EdgeSelected(EdgeChange):
    def __init__(self, source:str, source_handle:str, target:str, target_handle:str):
        super().__init__(source, source_handle, target, target_handle)
    
    def __repr__(self):
        return f"Edge selected : from {self.source} - {self.source_handle} to {self.target} - {self.target_handle}"

class EdgeDeselected(EdgeChange):
    def __init__(self, source:str, source_handle:str, target:str, target_handle:str):
        super().__init__(source, source_handle, target, target_handle)
    
    def __repr__(self):
        return f"Edge deselected : from {self.source} - {self.source_handle} to {self.target} - {self.target_handle}"


class ReactFlowNode:
    child:pn.viewable.Viewable = None
    node_class_name = ""
    ports:List[NodePort]
    plugged_nodes:Dict[str, List['ReactFlowNode']]
    name:str

    def __init__(self,):
        self.plugged_nodes = {}

    def create(self, ):
        raise NotImplementedError

    def update(self, _):
        print("Updating ", self.name)
        for port in self.ports:
            if port.direction == PortDirection.OUTPUT and port.name in self.plugged_nodes:
                for node in self.plugged_nodes[port.name]:
                    node.update(_)
    
    def get_node_json_value(self,):
        raise NotImplementedError
    
    def on_node_move(self, node_move:NodeMove):
        pass
    
    def on_node_selected(self, ):
        pass
    
    def on_node_deselected(self, ):
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
        self.node = node
        self.x = x
        self.y = y

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
        self.source_handle = source_handle
        self.target = target
        self.target_handle = target_handle

