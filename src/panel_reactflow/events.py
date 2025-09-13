
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

