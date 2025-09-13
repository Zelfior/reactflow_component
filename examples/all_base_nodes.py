
import panel as pn

from panel_reactflow.workflow import Workflow
from panel_reactflow.nodes import *


Workflow(nodes_classes = [
    ArrayInputNode, 
    ButtonNode, 
    CheckBoxNode, 
    ColorPickerNode, 
    DatePickerNode,
    DateRangePickerNode,
    FileInputNode,
    FloatInputNode,
    IntInputNode,
    SelectNode,
    MultiChoiceNode,
    TextInputNode, 
    PrintInputNode
],
    initial_nodes=[],
    initial_edges=[]
).show()
