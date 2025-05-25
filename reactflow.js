


console.log("importing");

import {
    ReactFlow,
    MiniMap,
    Controls,
    Background,
    useNodesState,
    useEdgesState,
    addEdge,
} from 'reactflow';

import { useCallback } from 'react';
import { Handle, Position, useReactFlow, type NodeProps, type Node } from 'reactflow';

const handleStyle = { left: 10 };
 
function TextNode({ id, data }: NodeProps<Node<{ text: string }>>) {
  const { updateNodeData } = useReactFlow;
 
  return (
    <div>
      <div>node {id}</div>
      <div>
        <input
        //   onChange={(evt) => updateNodeData(id, { text: evt.target.value })}
          value={data.text}
          className="xy-theme__input"
        />
      </div>
      <Handle type="source" position={Position.Bottom} />
    </div>
  );
}


let myPythonCodeString = `
import panel as pn
pn.extension(sizing_mode="stretch_width")

slider = pn.widgets.FloatSlider(start=0, end=10, name='Amplitude')

def callback(new):
    return f'Amplitude is: {new}'

component = pn.Row(slider, pn.bind(callback, slider))
component.servable(target='my_panel_widget');
`;


const nodeTypes = {
  textUpdater: TextNode,
};

const initialNodes = [
    { 
        id: 'node-1',
        type: 'textUpdater',
        position: { x: 0, y: 0 },
        data: { text: '' }, 
    },
    { id: '2', 
        position: { x: 0, y: 100 }, 
    data: { label: '2' } },
];
const initialEdges = [{ id: 'e1-2', source: '1', target: '2' , sourceHandle: 'a'}];

export function render({ model }) {
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
            model.send_msg('updated'); 
        },
        [setEdges],
    );

    model.send_msg('updated'); 

    // nodes[0].data = model.get_child("py_component");

    return (
        <div style={{ width: '100vw', height: '100vh' }}>
            <ReactFlow
                nodes={nodes}
                edges={edges}
                onNodesChange={onNodesChange}
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
    );
}