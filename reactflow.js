
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

    const [node_class_labels, setNodeClassLabels] = useModel().useState("node_class_labels");

    console.log(node_class_labels);

    return (
        <aside>
            <div className="description">
                {/* You can drag these nodes to the pane on the right. */}
            </div>
            <div className="nodes-container">
                {node_class_labels.map((label, index) => (
                    <div
                        key={index}
                        className={`dndnode`}
                        onDragStart={(event) => onDragStart(event, label)}
                        draggable
                    >
                        {label} Node
                    </div>
                ))}
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
const positions = [Position.Top, Position.Bottom, Position.Right, Position.Left];

function PanelWidgetNode({ id, data }) {
    const { setNodes } = useReactFlow();
    const model = useModel(); // Access the model using the custom hook at the top level

    let children = model.get_child("items");
    let [ports_list, setPortsList] = model.useState("item_ports");

    let child;
    let ports;

    const self_num = parseInt(id.replace('dndnode_', ''), 10);

    for (let index = 0; index < children.length; index++) {
        if (self_num == index){
            child = children[index];
            ports = ports_list[index];
            break;
        }
    }

    return (
        <div>
            <div>
                {child}
            </div>
            {ports && ports.map((handle, index) => {
                const [typeValue, positionValue, name] = handle;
                const type = typeValue === 0 ? 'target' : 'source';
                const position = positions[positionValue];

                return (
                <Handle
                    key={index} // Make sure to use a unique key for each element in the list
                    type={type}
                    position={position}
                    id={name}
                />
                );
            })}
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
];

const initialEdges = [
];



/**
 * 
 *  Displayed component definition
 * 
 * 
 */

const getNodeTypes = (onMyTrigger) => ({
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

            const position = screenToFlowPosition({
                x: event.clientX,
                y: event.clientY,
            });
            const newNode = {
                id: getId(),
                type:'panelWidget',
                position,
                data: { label: `${type} node` },
            };
            
            model.send_msg("NEW_NODE:"+newNode.id+":"+type.toString());

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
