
import panel as pn

from panel_reactflow.workflow import Workflow
from panel_reactflow.api import Node, Edge
from panel_reactflow.nodes import *

array_node = ArrayInputNode()
array_node.array_input.value = np.array([1, 2, 3, 4, 5])

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
    initial_nodes=[
        Node("Input array", array_node, 0., 0.),
        Node("Button", ButtonNode(), 0., 100.),
        Node("CheckBox", CheckBoxNode(), 0., 200.),
        Node("ColorPicker", ColorPickerNode(), 0., 300.),
        Node("DatePicker", DatePickerNode(), 0., 400.),
        Node("DateRangePicker", DateRangePickerNode(), 0., 500.),
        Node("FileInput", FileInputNode(), 0., 600.),

        Node("FloatInput", FloatInputNode(), 250., 0.),
        Node("IntInput", IntInputNode(), 250., 100.),
        Node("Select", SelectNode(), 250., 200.),
        Node("MultiChoice", MultiChoiceNode(), 250., 300.),
        Node("TextInput", TextInputNode(), 250., 400.),
        Node("PrintInput", PrintInputNode(), 250., 500.),
    ],
    initial_edges=[
        Edge("Input array", "Output", "Select", "Options"),
        Edge("Input array", "Output", "MultiChoice", "Options"),
        Edge("Input array", "Output", "PrintInput", "Input")
    ]
).show()
