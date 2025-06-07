
from pathlib import Path
from typing import Any
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

class ReactFlow(ReactComponent):

    edges = param.List()
    nodes = param.List()

    button = Child()

    def __init__(self, sizing_mode = "stretch_both", **kwargs):
        super().__init__(sizing_mode=sizing_mode, **kwargs)

    _importmap = {
        "imports": {
            "reactflow": "https://esm.sh/reactflow@11.11.4",
            "react-select": "https://esm.sh/react-select@5.10.1",    
        }
    }
    
    _stylesheets = [
                        "https://unpkg.com/reactflow@11.11.4/dist/style.css",
                        make_css("textUpdater"),
                        make_css("dropBox"),
                        make_css("panelWidget"),
                        make_css("dndnode"),
                        make_css("input"),
                        Path("dnd_flow.css")
                    ]

    _esm = Path(__file__).parent / "reactflow.js"

    def update_node_value(self, node_name:str, parameter_name:str, parameter_value:Any):
         self._send_event(ESMEvent, data=f"{node_name}@{parameter_name}@{parameter_value}")

    def _handle_msg(self, data):
        print("Received message :", data, )

    def print_nodes(self, _):
        print("\n\nPrinting nodes")
        
        for node in self.nodes:
            print(node)

        print("\n\nPrinting edges")
        for edge in self.edges:
            print(edge)
         

if __name__ == "__main__":

    bt = pn.widgets.Button(name="pn.widgets.Button")
    bt.on_click(lambda event:print("Clicked"))
    col = pn.layout.Column(pn.pane.Markdown("pn.layout.Column example"), bt, pn.widgets.Select(options=["option 1", "option 2"], width=150))
    rf1 = ReactFlow(button=col)
    rf2 = ReactFlow(button=col)
    rf3 = ReactFlow(button=col)

    for rf in [rf1, rf2, rf3]:
         rf.param.watch(rf.print_nodes, "nodes")

    rf1.show()
    # pn.Row(pn.Column(rf1, rf2), rf3).show()