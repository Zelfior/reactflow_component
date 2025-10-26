
from typing import Any, Dict, List

import panel as pn

from panel_reactflow.workflow import Workflow, WorkflowNode
from panel_reactflow.api import Edge, Node, NodePort, PortDirection, PortPosition

class FloatInputNode(WorkflowNode):
    node_class_name = "Float Input"
    ports:List[NodePort] = [NodePort(direction=PortDirection.OUTPUT, position=PortPosition.RIGHT, name="output")]

    def __init__(self, value: float = 0.):
        super().__init__()
        self.float_input = pn.widgets.FloatInput(value=value, width=100)
        
        self.float_input.param.watch(self.update, "value")

    def create(self, ):
        return pn.layout.Column(
                                    self.float_input, 
                                    name=self.name, 
                                    align="center"
                                )
    
    def update(self, _):
        self.update_outputs()

    def get_node_json_value(self) -> Dict[str, Any]:
        return {"value" : self.float_input.value}

class ResultNode(WorkflowNode):
    node_class_name = "Result"
    ports:List[NodePort] = [NodePort(direction=PortDirection.INPUT, position=PortPosition.LEFT, name="input")]

    def __init__(self, ):
        super().__init__()
        self.result_label = pn.pane.Markdown("Result : Undefined")

    def create(self, ):
        return pn.layout.Column(
                                    self.result_label, 
                                    name=self.name, 
                                    align="center"
                                )
    
    def update(self, _):
        value = 0

        if "input" in self.plugged_nodes :
            if len(self.plugged_nodes["input"]) == 0:
                self.result_label.object = f"Result : Undefined"
            else:
                for float_input in self.plugged_nodes["input"]:
                    value += float_input.get_node_json_value()["value"]

                self.result_label.object = f"Addition result : {round(value, 1)}"
            self.update_outputs()

    def get_node_json_value(self) -> Dict[str, Any]:
        return {"value" : self.result_label.object}


def make_reactflow():
    node_1 = FloatInputNode(4.5)
    node_2 = ResultNode()
    node_3 = FloatInputNode(2)

    rf1 = Workflow(nodes_classes = [FloatInputNode, ResultNode],
                    initial_nodes=[Node("Node_1", node_1, 0, 0),
                        Node("Node_3", node_3, 0, 100),
                        Node("Node_2", node_2, 200, 0),],
                    initial_edges=[Edge("Node_1", "output", "Node_2", "input"),
                                   Edge("Node_3", "output", "Node_2", "input")])

    return rf1

make_reactflow().show()
