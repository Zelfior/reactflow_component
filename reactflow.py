import glob
import os
from pathlib import Path
import panel as pn

from panel.custom import ReactComponent
import param
# npm install @xyflow/react

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

text_node_css = """.react-flow__node-textUpdater {
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
.react-flow__node-textUpdater.selectable:hover {
      box-shadow: 0 1px 4px 1px rgba(0, 0, 0, 0.08);
}
.react-flow__node-textUpdater.selectable.selected,
    .react-flow__node-textUpdater.selectable:focus,
    .react-flow__node-textUpdater.selectable:focus-visible {
      box-shadow: 0 0 0 0.5px #1a192b;
}
    """
"""Basic node display that is added to the default style.css"""

class ReactFlow(ReactComponent):

    edges = param.List()
    nodes = param.List()

    def __init__(self, sizing_mode = "stretch_both", **kwargs):
        super().__init__(sizing_mode=sizing_mode, **kwargs)

    _importmap = {
        "imports": {
            "reactflow": "https://esm.sh/reactflow@11.11.4",
        }
    }
    
    _stylesheets = [
                        "https://unpkg.com/reactflow@11.11.4/dist/style.css",
                        text_node_css
                    ]

    _esm = Path(__file__).parent / "reactflow.js"

    def _handle_msg(self, data):
        # if False:
            # print(self.edges)
            print(data, self.nodes)
            # print()

    # def _handle_click(self, event):
    #     self.value = event.data

if __name__ == "__main__":
    rf1 = ReactFlow()
    rf2 = ReactFlow()
    rf3 = ReactFlow()
    pn.Row(pn.Column(rf1, rf2), rf3).show()