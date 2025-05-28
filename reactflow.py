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


class ReactFlow(ReactComponent):

    edges = param.List()
    nodes = param.List()

    def __init__(self, sizing_mode = "stretch_both", **kwargs):
        super().__init__(sizing_mode=sizing_mode, **kwargs)

    _importmap = {
        "imports": {
            "reactflow": "https://esm.sh/reactflow@11.11.4",
            # "prop-types":"https://unpkg.com/prop-types@15.6/prop-types.js",
            # "usehooks-ts":"https://unpkg.com/usehooks-ts@3.1.1/dist/index.js",
            # "lodash.debounce":"https://unpkg.com/lodash.debounce@4.0.8/index.js"
        }
    }
    
    _stylesheets = [
                    #   Path(f"{filename}") for filename in glob.glob("*.css")
                      Path(__file__).parent / Path(f"main.css"),
                      Path(__file__).parent / Path(f"init.css"),
                      Path(__file__).parent / Path(f"style.css"),
                      Path(__file__).parent / Path(f"node-resizer.css"),
                    ]

    _esm = Path(__file__).parent / "reactflow.js"

    def _handle_msg(self, data):
        if False:
            print(self.edges)
            print(self.nodes)
            print()

    # def _handle_click(self, event):
    #     self.value = event.data

if __name__ == "__main__":
    rf1 = ReactFlow()
    rf2 = ReactFlow()
    rf3 = ReactFlow()
    pn.Row(pn.Column(rf1, rf2), rf3).show()