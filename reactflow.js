
import {
    ReactFlow,
    MiniMap,
    Controls,
    Background,
    useNodesState,
    useEdgesState,
    addEdge,
    ReactFlowProvider,
} from 'reactflow';

import { useRef, useCallback, createContext, useContext, useState, useMemo } from 'react';
import { Handle, Position, useReactFlow } from 'reactflow';

// Create a context for the model
const ModelContext = createContext(null);

// Custom hook to use the model context
export const useModel = () => useContext(ModelContext);

// Provider component
export const ModelProvider = ({ model, children }) => {
    return (
        <ModelContext.Provider value={model}>
            {children}
        </ModelContext.Provider>
    );
};

/**
 * 
 *  Drag and drop feature
 * 
 * 
 */
const DnDContext = createContext([null, (_) => { }]);

export const DnDProvider = ({ children }) => {
    const [type, setType] = useState(null);

    return (
        <DnDContext.Provider value={[type, setType]}>
            {children}
        </DnDContext.Provider>
    );
};

export const useDnD = () => {
    return useContext(DnDContext);
};

function Sidebar() {
    const [_, setType] = useDnD();

    const onDragStart = (event, nodeType) => {
        setType(nodeType);
        event.dataTransfer.effectAllowed = 'move';
    };

    return (
        <aside>
            <div className="description">
                {/* You can drag these nodes to the pane on the right. */}
            </div>
            <div className="nodes-container">
                <div
                    className="dndnode input"
                    onDragStart={(event) => onDragStart(event, 'textUpdater')}
                    draggable
                >
                    Input Node
                </div>
                <div
                    className="dndnode"
                    onDragStart={(event) => onDragStart(event, 'dropBox')}
                    draggable
                >
                    Default Node
                </div>
                <div
                    className="dndnode output"
                    onDragStart={(event) => onDragStart(event, 'panelWidget')}
                    draggable
                >
                    Output Node
                </div>
            </div>
        </aside>
    );
}














/**
 * 
 *  Components definition
 * 
 * 
 */
function DropBox({ id, data }) {
    const { setNodes } = useReactFlow();

    const updateData = (evt) => {
        const inputVal = evt.target.value;

        setNodes((nodes) =>
            nodes.map((node) => {
                if (node.id === id) {
                    return {
                        ...node,
                        data: {
                            ...node.data,
                            value: inputVal,
                        },
                    };
                }
                return node;
            })
        );
    };

    return (
        <div style={{ border: '1px solid #ddd', padding: '10px', borderRadius: '5px' }}>
            <Handle type="target" position={Position.Top} />
            <select onChange={updateData}>
                <option value="light">light</option>
                <option value="dark">dark</option>
                <option value="system">system</option>
            </select>
            <Handle type="source" position={Position.Bottom} />
        </div>
    );
}

function TextUpdaterNode({ id, data, //onMyTrigger 
}) {
    const { setNodes } = useReactFlow();
    // const model = useModel(); // Access the model using the custom hook at the top level

    const updateData = (evt) => {
        const inputVal = evt.target.value;

        setNodes((nodes) =>
            nodes.map((node) => {
                if (node.id === id) {
                    return {
                        ...node,
                        data: {
                            ...node.data,
                            value: inputVal,
                        },
                    };
                }
                return node;
            })
        );

        // onMyTrigger(new_nodes);
    };

    return (
        <div>
            <div>Node graph</div>
            <div>
                <input
                    onChange={updateData}
                    value={data.value}
                    className="xy-theme__input"
                />
            </div>
            <Handle type="source" position={Position.Bottom} />
        </div>
    );
}

function PanelWidgetNode({ id, data }) {
    const { setNodes } = useReactFlow();
    const model = useModel(); // Access the model using the custom hook at the top level

    return (
        <div>
            <div>Panel widget</div>
            <div>
                {model.get_child("button")}
            </div>
            <Handle type="source" position={Position.Bottom} />
        </div>
    );
}

/**
 * 
 *  Initial state definition
 * 
 * 
 */
const initialNodes = [
    {
        id: '1',
        position: { x: 161, y: -13 },
        data: { value: 'Incoming' },
        type: 'textUpdater',
    },
    {
        id: '2',
        position: { x: 180, y: 65 },
        data: { value: 'feature' },
        type: 'dropBox',
    },
    {
        id: '3',
        position: { x: 100, y: 125 },
        data: { label: 'panelWidget' },
        type: 'panelWidget',
    },
    {
        id: '4',
        position: { x: 270, y: 125 },
        data: { label: 'parametrize' },
    },
    {
        id: '5',
        position: { x: 180, y: 185 },
        data: { label: 'plots' },
    },
];

const initialEdges = [
    {
        source: '1',
        target: '2',
        id: 'reactflow__edge-1-2',
    },
    {
        source: '2',
        target: '3',
        id: 'reactflow__edge-2-3',
    },
    {
        source: '3',
        target: '5',
        id: 'reactflow__edge-3-5',
    },
    {
        source: '2',
        target: '4',
        id: 'reactflow__edge-2-4',
    },
    {
        source: '4',
        target: '5',
        id: 'reactflow__edge-4-5',
    },
];



/**
 * 
 *  Displayed component definition
 * 
 * 
 */

const getNodeTypes = (onMyTrigger) => ({
  textUpdater: TextUpdaterNode,// (props) => <TextUpdaterNode {...props} onMyTrigger={onMyTrigger} />,
  dropBox: DropBox,
  panelWidget: PanelWidgetNode,
});

let id = 0;
const getId = () => `dndnode_${id++}`;

const DnDFlow = () => {
    const model = useModel();
    const reactFlowWrapper = useRef(null);
    // const reactFlowInstance = useReactFlow();
    const [py_nodes, py_setNodes] = model.useState('nodes');
    const [py_edges, py_setEdges] = model.useState('edges');
    const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
    const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);
    const { screenToFlowPosition } = useReactFlow();
    const [type] = useDnD();
    if (nodes !== py_nodes) {
        py_setNodes(nodes);
    }

    if (edges !== py_edges) {
        py_setEdges(edges);
    }

    const onConnect = useCallback(
        (params) => {
            setEdges((eds) => addEdge(params, eds));
            model.send_msg('Connected');
        },
        [setEdges]
    );

    const onNodesChangeHandler = (changes) => {
        onNodesChange(changes);

        let new_nodes = [];
        changes.forEach((change) => {
            if (Object.hasOwn(change, 'item')) {
                new_nodes.push(change.item);
                console.log(change.item.data);
            }
        });
        if (new_nodes.length !== 0) {
            py_setNodes(new_nodes);
            model.send_msg('Node Change');
            // model.nodes = new_nodes;
        }
    };

    const onMyTrigger = useCallback((new_nodes) => {
        console.log("New nodes my trigger", new_nodes);

        // py_setNodes(new_nodes);
        // model.send_msg('Node Change from my trigger');
    }, [model]);


    const onDragOver = useCallback((event) => {
        event.preventDefault();
        event.dataTransfer.dropEffect = 'move';
    }, []);

    const onDrop = useCallback(
        (event) => {
            event.preventDefault();

            // check if the dropped element is valid
            if (!type) {
                return;
            }

            // project was renamed to screenToFlowPosition
            // and you don't need to subtract the reactFlowBounds.left/top anymore
            // details: https://reactflow.dev/whats-new/2023-11-10
            const position = screenToFlowPosition({
                x: event.clientX,
                y: event.clientY,
            });
            const newNode = {
                id: getId(),
                type,
                position,
                data: { label: `${type} node` },
            };

            setNodes((nds) => nds.concat(newNode));
        },
        [screenToFlowPosition, type]
    );

    const onDragStart = (event, nodeType) => {
        setType(nodeType);
        event.dataTransfer.setData('text/plain', nodeType);
        event.dataTransfer.effectAllowed = 'move';
    };

    const nodeTypes = useMemo(() => getNodeTypes(onMyTrigger), [onMyTrigger]);
    return (
        <div className="dndflow" style={{ display: 'flex', width: '100%', height: '100%' }}>
            <div className="reactflow-wrapper" ref={reactFlowWrapper}>
                <ReactFlow
                    nodes={nodes}
                    edges={edges}
                onNodesChange={onNodesChangeHandler}
                    onEdgesChange={onEdgesChange}
                    onConnect={onConnect}
                nodeTypes={nodeTypes}
                    onDrop={onDrop}
                    onDragStart={onDragStart}
                    onDragOver={onDragOver}
                    fitView
                >
                    <Controls />
                    <MiniMap />
                    <Background variant="dots" gap={12} size={1} />
                </ReactFlow>
            </div>
            <Sidebar />
        </div>
    );
};

export function render({ model }) {
    return (<ReactFlowProvider>
                <ModelProvider model={model}>
        <DnDProvider>
            <DnDFlow />
        </DnDProvider>
                    </ModelProvider>
    </ReactFlowProvider>);
};
