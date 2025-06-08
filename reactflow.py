
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, NamedTuple, Type
import panel as pn

from panel.custom import Child, Children, ReactComponent, ESMEvent
import param
# reactflow site : https://reactflow.dev/learn
# reactflow github :https://github.com/xyflow/xyflow/tree/main/packages/react
# reactflow custom component : https://reactflow.dev/learn/customization/custom-nodes
# tutorials : https://reactflow.dev/examples/

# confetti example : https://panel.holoviz.org/reference/custom_components/ReactComponent.html#dependency-imports

# /* esm.sh - reactflow@11.11.4 */
# import "/@reactflow/background@11.3.14/es2022/background.mjs";
# import "/@reactflow/controls@11.2.14/es2022/controls.mjs";
# import "/@reactflow/core@11.11.4/es2022/core.mjs";
# import "/@reactflow/minimap@11.7.14/es2022/minimap.mjs";
# import "/@reactflow/node-resizer@2.2.14/es2022/node-resizer.mjs";
# import "/@reactflow/node-toolbar@1.3.14/es2022/node-toolbar.mjs";
# export * from "/reactflow@11.11.4/es2022/reactflow.mjs";
# export { default } from "/reactflow@11.11.4/es2022/reactflow.mjs";

def make_css(node_name):
    return """.react-flow__node-{node_name} {
  padding: 10px;
  border-radius: 3px;
  min-width: 150px;
  font-size: 12px;
  color: #222;
  text-align: center;
  border-width: 1px;
  border-style: solid;
  border-color: #1a192b;
  background-color: white;
}

}

.react-flow__node-{node_name}.selectable:hover {
      box-shadow: 0 1px 4px 1px rgba(0, 0, 0, 0.08);
}
.react-flow__node-{node_name}.selectable.selected,
    .react-flow__node-{node_name}.selectable:focus,
    .react-flow__node-{node_name}.selectable:focus-visible {
      box-shadow: 0 0 0 0.5px #1a192b;
}
    """.replace("{node_name}", node_name)
"""Basic node display that is added to the default style.css"""

class PortDirection(Enum):
    INPUT=0
    OUTPUT=1

class PortPosition(Enum):
    TOP=0
    BOTTOM=1
    RIGHT=2
    LEFT=3

class NodePort(NamedTuple):
    direction:PortDirection
    position:PortPosition
    name:str

class ReactFlowNode:
    child:pn.viewable.Viewable = None
    node_class_name = ""
    ports:List[NodePort]
    plugged_nodes:Dict[str, List['ReactFlowNode']]

    def create(name:str):
        raise NotImplementedError

    def update(name:str):
        raise NotImplementedError

class ReactFlow(ReactComponent):

    edges = param.List()
    nodes = param.List()
    item_ports = param.List()

    items = Children()

    nodes_classes: List[Type[ReactFlowNode]] = []
    nodes_instances: List[ReactFlowNode] = []

    node_class_labels = param.List()

    _importmap = {
        "imports": {
            "reactflow": "https://esm.sh/reactflow@11.11.4",
            "react-select": "https://esm.sh/react-select@5.10.1",    
        }
    }
    
    _stylesheets = [
                        "https://unpkg.com/reactflow@11.11.4/dist/style.css",
                        make_css("dndnode"),
                        make_css("input"),
                        make_css("panelWidget"),
                        Path("dnd_flow.css"),
                    ]

    _esm = Path(__file__).parent / "reactflow.js"


    def __init__(self, sizing_mode = "stretch_both", nodes_classes:List[Type[ReactFlowNode]] = [], **kwargs):
        super().__init__(sizing_mode=sizing_mode, **kwargs)

        self.nodes_classes = nodes_classes
        self.node_class_labels = [c.node_class_name for c in self.nodes_classes]

        # self.param.watch(self.update_nodes, "nodes")
        # self.param.watch(self.update_nodes, "edges")

    def update_node_value(self, node_name:str, parameter_name:str, parameter_value:Any):
         self._send_event(ESMEvent, data=f"{node_name}@{parameter_name}@{parameter_value}")

    def _handle_msg(self, data:str):
        if data.startswith("NEW_NODE"):
            _, node_id, node_type = data.split(":")

            new_item = None
            for c in self.nodes_classes:
                if c.node_class_name == node_type:
                    print(f"Creating node of type {node_type}")

                    node = c()
                    new_item = node.create(f"{node_id}")
                    
                    self.nodes_instances.append(node)
                    
                    self.items += [new_item]
                    self.item_ports = self.item_ports + [[[p.direction.value, p.position.value, p.name] for p in c.ports]]

        print("Received message :", data, )

    def print_nodes(self, _):
        print("\n\nPrinting nodes")
        
        for node in self.nodes:
            print(node)

        print("\n\nPrinting edges")
        for edge in self.edges:
            print(edge)
            
    # def update_nodes(self, _):
    #     print("Updating nodes")
    #     self.get_node_tree()
         
    # def get_node_tree(self,):
        
    #     for node in self.nodes_instances:
    #         node.plugged_nodes = {port.name : [] for port in node.ports}

    #     for edge in self.edges:
    #         source_node = [node for node in self.nodes if node['id'] == edge["source"]][0]
    #         target_node = [node for node in self.nodes if node['id'] == edge["target"]][0]
            
    #         print(source_node, target_node)
# {'source': 'dndnode_1', 'sourceHandle': 'input', 'target': 'dndnode_0', 'targetHandle': 'output', 'id': 'reactflow__edge-dndnode_1input-dndnode_0output'}
        

if __name__ == "__main__":
    class FloatInputNode(ReactFlowNode):
        child:pn.viewable.Viewable = None
        node_class_name = "Float Input"
        ports:List[NodePort] = [NodePort(direction=PortDirection.OUTPUT, position=PortPosition.BOTTOM, name="output")]

        def __init__(self,):
            self.mkdown = pn.pane.Markdown("Drag & drop example")
            self.float_input = pn.widgets.FloatInput(value=0., width=100)

        def create(self, name:str):
            return pn.layout.Column(
                                        self.mkdown, 
                                        self.float_input, 
                                        name=name, 
                                        align="center"
                                    )

    class ResultNode(ReactFlowNode):
        child:pn.viewable.Viewable = None
        node_class_name = "Result"
        ports:List[NodePort] = [NodePort(direction=PortDirection.INPUT, position=PortPosition.TOP, name="input")]

        def __init__(self,):
            self.result_label = pn.pane.Markdown("Result : Undefined")

        def create(self, name:str):
            return pn.layout.Column(
                                        self.result_label, 
                                        name=name, 
                                        align="center"
                                    )



    def make_reactflow():
        rf1 = ReactFlow(nodes_classes = [FloatInputNode, ResultNode])
        rf1.param.watch(rf1.print_nodes, "nodes")

        return rf1

    make_reactflow().show()
    # pn.Row(pn.Column(rf1, rf2), rf3).show()