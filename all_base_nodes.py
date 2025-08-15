
import panel as pn

from reactflow import ReactFlow
from nodes import *


pn.Column(ReactFlow(nodes_classes = [ArrayInputNode, 
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
                                        PrintInputNode],
                    initial_nodes=[],
                    initial_edges=[])).show()
