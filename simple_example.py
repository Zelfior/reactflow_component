
from typing import Any, Dict, List

import panel as pn

from reactflow import ReactFlow
from reactflow_api import NodePort, PortDirection, PortPosition, ReactFlowNode


class FloatInputNode(ReactFlowNode):
    node_class_name = "Float Input"
    ports:List[NodePort] = [NodePort(direction=PortDirection.OUTPUT, position=PortPosition.RIGHT, name="output")]

    def __init__(self, ):
        super().__init__()
        self.float_input = pn.widgets.FloatInput(value=0., width=100)
        
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

class ResultNode(ReactFlowNode):
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
    rf1 = ReactFlow(nodes_classes = [FloatInputNode, ResultNode],
                    initial_nodes=[],
                    initial_edges=[])

    return rf1

rf = make_reactflow()
pn.Column(rf).show()
