


console.log("importing");

import {
    ReactFlow,
    MiniMap,
    Controls,
    Background,
    useNodesState,
    useEdgesState,
    addEdge,
    useStore,
    ReactFlowProvider,
    
} from 'reactflow';


import { useCallback, useEffect, useLayoutEffect, type ChangeEventHandler } from 'react';
import { Handle, Position, useReactFlow, type NodeProps, type Node } from 'reactflow';

const handleStyle = { left: 10 };


function TextUpdaterNode({ id, data }) {
  const { setNodes } = useReactFlow();

  const updateData: ChangeEventHandler<HTMLInputElement> = (evt) => {
    const inputVal = (evt.target as HTMLInputElement).value;

    setNodes((nodes) =>
      nodes.map((node) => {
        if (node.id === id) {
          return {
            ...node,
            data: {
              ...node.data,
              text:inputVal
            }
          };
        }

        return node;
      })
    );
  };

  return (
    <div>
      <div>Node graph</div>
      <div>
        <input
          onChange={updateData}
          value={data.text}
          className="xy-theme__input"
        />
      </div>
      <Handle type="source" position={Position.Bottom} />
    </div>
  );
}

const nodeTypes = {
  textUpdater: TextUpdaterNode,
};

const initialNodes = [
    {
        id: "1",
        position: {"x": 161, "y": -13},
        data: {"text": "Incoming"},
        type:"textUpdater"
    },
    {
        id: "2",
        position: {"x": 180, "y": 65},
        data: {"label": "feature"},
    },
    {
        id: "3",
        position: {"x": 100, "y": 125},
        data: {"label": "to"},
    },
    {
        id: "4",
        position: {"x": 270, "y": 125},
        data: {"label": "parametrize"},
    },
    {
        id: "5",
        position: {"x": 180, "y": 185},
        data: {"label": "plots"},
    }
];
const initialEdges = [{
        "source": "1",
        "target": "2",
        "id": "reactflow__edge-1-2"
    },
    {
        "source": "2",
        "target": "3",
        "id": "reactflow__edge-2-3"
    },
    {
        "source": "3",
        "target": "5",
        "id": "reactflow__edge-3-5"
    },
    {
        "source": "2",
        "target": "4",
        "id": "reactflow__edge-2-4"
    },
    {
        "source": "4",
        "target": "5",
        "id": "reactflow__edge-4-5"
    }];

    
function Flow({model}) {
  // you can access the internal state here
    const reactFlowInstance = useReactFlow();
    const [py_nodes, py_setNodes] = model.useState("nodes");
    const [py_edges, py_setEdges] = model.useState("edges");

    const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
    const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);

    if(nodes != py_nodes){
        py_setNodes(nodes);
    }
    
    if(edges != py_edges){
        py_setEdges(edges);
    }
    
    
    const onConnect = useCallback(
        (params) => {
            setEdges((eds) => addEdge(params, eds));
            model.send_msg('Connected'); 
        },
        [setEdges],
    );

    const onNodesChangeHandler = (changes) => {
        onNodesChange(changes);

        let new_nodes = [];
        changes.forEach(change => {
            if (Object.hasOwn(change, 'item')){
                new_nodes.push(change.item);
                console.log(change.item.data);
            }
        });
        if (new_nodes != []){
            py_setNodes(new_nodes);
            model.send_msg('Node Change'); 
        }
    };

    // model.send_msg('Usual loop'); 

    return <div style={{ width: '100%', height: '100%' }}
            >
                <ReactFlow
                    nodes={nodes}
                    edges={edges}
                    onNodesChange={onNodesChangeHandler}
                    onEdgesChange={onEdgesChange}
                    onConnect={onConnect}
                    nodeTypes={nodeTypes}
                    fitView
                >
                    <Controls />
                    <MiniMap />
                    <Background variant="dots" gap={12} size={1} />
                </ReactFlow>
            </div>
}
 

export function render({ model }) {
    
    return (
        <ReactFlowProvider>
            <Flow model={model} />
        </ReactFlowProvider>
        );
}