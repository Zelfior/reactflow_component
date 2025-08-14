
import {
    ReactFlow,
    MiniMap,
    Controls,
    Background,
    useNodesState,
    useEdgesState,
    addEdge,
    ReactFlowProvider,
    useUpdateNodeInternals,
    getOutgoers,
    useReactFlow,
    Handle,
    Position,
    useEdges,
} from 'reactflow';
import { useRef, useCallback, createContext, useContext, useState, useMemo, forwardRef, HTMLAttributes, memo, useEffect } from 'react';

// import {
//     useNodeConnections ,
// } from 'reactflow';

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
 *  Restrictive handle
 * 
 * 
 */
function countConnectedEdges(edges, currentPort) {
    // Initialize a counter for the number of connected edges
    let count = 0;

    // Iterate over each edge in the edges array
    edges.forEach(edge => {
        // Check if the edge's source and sourceHandle match the current port's id and type
        if (edge.targetHandle === currentPort.id && edge.target == currentPort.node_name) {
            count++;
        }
    });

    // Return the count of connected edges
    return count;
}
const CustomRestrictiveHandle = (props) => {
    let edges = useEdges();

    return (
        <Handle
            {...props}
            isConnectable={countConnectedEdges(edges, props) < props.connectionCount}
        />
    );
};

/**
 * 
 *  Components definition
 * 
 * 
 */
const positions = [Position.Top, Position.Bottom, Position.Right, Position.Left];
function renderPortsNames(ports) {
    const maxOffset =
        ports && ports.length > 0
            ? Math.max(
                ...ports.map(([, , , display_name, offset]) =>
                    display_name && offset !== undefined ? offset : 0
                )
            ) + 20 // estimated height
            : 0;

    return (
        <div
            style={{
                position: 'relative',
                top: '-20px',
                minHeight: `${maxOffset}px`,
                width: 'max-content',
            }}
        >
            {/* Invisible block to preserve width */}
            <div style={{ visibility: 'hidden', position: 'relative' }}>
                {ports &&
                    ports.map(([, , name, display_name]) =>
                        display_name ? <div key={name}>{name}</div> : null
                    )}
            </div>

            {/* Absolutely positioned spans */}
            {ports &&
                ports.map((handle, index) => {
                    const [, , name, display_name, offset] = handle;

                    if (!display_name) return null;

                    const spanStyle =
                        offset !== undefined
                            ? {
                                position: 'absolute',
                                top: `${offset}px`,
                                left: 0,
                                whiteSpace: 'nowrap',
                            }
                            : {
                                position: 'absolute',
                                top: `${maxOffset * 0.5}px`,
                                left: 0,
                                whiteSpace: 'nowrap'
                            };

                    return (
                        <span key={name} style={spanStyle}>
                            {name}
                        </span>
                    );
                })}
        </div>
    );
}

function renderHandles(ports, origin, id) {
    return ports && ports.map((handle, index) => {
        let [typeValue,
            positionValue,
            name,
            display_name,
            offset,
            connectionCount,
            restiction_name,
            restriction_color] = handle;
        const type = typeValue === 0 ? 'target' : 'source';
        const position = positions[positionValue];

        if (connectionCount == undefined)
            connectionCount = 10000;

        let style = {
            background: restriction_color !== undefined ? restriction_color : '#000'
        };

        if (offset != undefined) {
            style[[origin]] = offset;
        }

        if (typeof (restiction_name) === "undefined") {
            restiction_name = "default";
        }

        let handleProperties = {
            key: index,
            type: type,
            position: position,
            id: name,
            title: name,
            node_name: id,
            style: style,
            connectionCount: connectionCount,
            restiction_name: restiction_name
        };

        return <CustomRestrictiveHandle {...handleProperties} />
    });
}

function PanelWidgetNode({ id, data }) {
    const model = useModel(); // Access the model using the custom hook at the top level
    const updateNodeInternals = useUpdateNodeInternals();

    let children = model.get_child("items");
    let [children_name,] = model.useState("item_names");
    let [ports_list,] = model.useState("item_ports");

    let child;
    let ports;

    for (let index = 0; index < children.length; index++) {
        if (id == children_name[index]) {
            child = children[index];
            ports = ports_list[index];
            break;
        }
    };

    updateNodeInternals(id);

    const leftPorts = ports && ports.filter(handle => positions[handle[1]] === Position.Left);
    const rightPorts = ports && ports.filter(handle => positions[handle[1]] === Position.Right);
    const topPorts = ports && ports.filter(handle => positions[handle[1]] === Position.Top);
    const bottomPorts = ports && ports.filter(handle => positions[handle[1]] === Position.Bottom);

    const gridContainerStyle = {
        display: 'grid',
        gridTemplateColumns: 'min-content auto min-content',
        gap: '0px',
    };

    const gridItemStyle = {
        // border: '1px solid black', // Uncomment for debug
        minWidth: "fit-content"
    };

    return (
        <div style={gridContainerStyle}>

            <div style={gridItemStyle}>
                {/* Display of the left ports, and if applicable, of the list of names */}

                {/* HTML element with all port names, one after the other */}
                {renderPortsNames(leftPorts)}

                {/* Display of Handle components */}
                {renderHandles(leftPorts, "top", id)}
            </div>

            <div style={gridItemStyle}>
                {/* Display of the top/bottom ports and actual panel element (child) */}

                {renderHandles((topPorts || []).concat(bottomPorts || []), "left", id)}
                {child}
            </div>

            <div style={gridItemStyle}>
                {/* Display of the left ports, and if applicable, of the list of names */}

                {/* HTML element with all port names, one after the other */}
                {renderPortsNames(rightPorts)}

                {/* Display of Handle components */}
                {renderHandles(rightPorts, "top", id)}
            </div>
        </div>
    );
}


/**
 * 
 *  Displayed component definition
 * 
 * 
 */

const getNodeTypes = (onMyTrigger) => ({
    panelWidget: PanelWidgetNode,
});

function getPortDict(node_name, port_name, node_list, port_list) {
    let ports = port_list[node_list.indexOf(node_name)];
    let foundPort;

    ports.forEach(port => {
        if (port[2] == port_name) {
            foundPort = port;
        }
    });

    return foundPort;
}

let id = 0;
const getId = () => `dndnode_${id++}`;

const DnDFlow = () => {
    const model = useModel();
    const reactFlowWrapper = useRef(null);

    const [py_nodes, py_setNodes] = model.useState('nodes');
    const [py_edges, py_setEdges] = model.useState('edges');

    const [py_initial_nodes,] = model.useState('initial_nodes');
    const parsed_initial_nodes = JSON.parse(py_initial_nodes.toString()
        .replace(/(['"])?([a-zA-Z0-9_]+)(['"])?:/g, '"$2":')  // fix keys
        .replace(/'/g, '"') // convert single to double quotes);
    );

    const [py_initial_edges,] = model.useState('initial_edges');
    const parsed_initial_edges = JSON.parse(py_initial_edges.toString()
        .replace(/(['"])?([a-zA-Z0-9_]+)(['"])?:/g, '"$2":')  // fix keys
        .replace(/'/g, '"') // convert single to double quotes);
    );

    const [allowEdgeLoops,] = model.useState("allow_edge_loops");
    const [displaySidebar,] = model.useState("display_side_bar");

    const [nodes, setNodes, onNodesChange] = useNodesState(parsed_initial_nodes);
    const [edges, setEdges, onEdgesChange] = useEdgesState(parsed_initial_edges);

    const { screenToFlowPosition, getNodes, getEdges } = useReactFlow();
    const [type] = useDnD();


    if (nodes !== py_nodes) {
        py_setNodes(nodes);
    }

    if (edges !== py_edges) {
        py_setEdges(edges);
    }

    let [item_names,] = model.useState("item_names");
    let [ports_list,] = model.useState("item_ports");

    const onConnect = useCallback(
        (params) => {
            let sourcePort = getPortDict(params["source"], params["sourceHandle"], item_names, ports_list);
            let targetPort = getPortDict(params["target"], params["targetHandle"], item_names, ports_list);

            // Checking if the restriction name is the same
            if (sourcePort[6] == targetPort[6]) {
                params["style"] = { stroke: targetPort[7] };
                setEdges((eds) => addEdge(params, eds));
            }
        },
        [setEdges, addEdge, edges, item_names, ports_list]
    );

    const onEdgesChangeHandler = useCallback(
        (changes) => {
            onEdgesChange(changes);

            let new_edge = [];
            changes.forEach((change) => {
                if (Object.hasOwn(change, 'item')) {
                    new_edge.push(change.item);
                }
            });

            if (new_edge.length !== 0) {
                py_setEdges(new_edge);
            }
        }, [py_setEdges]
    );

    const onNodesChangeHandler = useCallback(
        (changes) => {
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
            }
        }, [py_setNodes]
    );

    const onMyTrigger = useCallback((new_nodes) => {
        console.log("New nodes my trigger", new_nodes);
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
                type: 'panelWidget',
                position,
                data: { label: `${type} node` },
            };

            model.send_msg({
                action: "NEW_NODE",
                node_id: newNode.id,
                type: type.toString(),
                x: newNode.position.x,
                y: newNode.position.y,
            });

            setNodes((nds) => nds.concat(newNode));
        },
        [screenToFlowPosition, type, setNodes]
    );

    const onDragStart = (event, nodeType) => {
        setType(nodeType);
        event.dataTransfer.setData('text/plain', nodeType);
        event.dataTransfer.effectAllowed = 'move';
    };

    const nodeTypes = useMemo(() => getNodeTypes(onMyTrigger), [onMyTrigger]);

    // Functions to create nodes and edges from python
    function receiveMessage(msg, setNodes, setEdges) {
        let action = msg["action"];

        if (action == "NodeCreation") {
            const node_id = msg["node_name"];
            const x = msg["x"];
            const y = msg["y"];
            const node_class_name = msg["node_class_name"];

            const newNode = {
                id: node_id,
                type: 'panelWidget',
                position: { x, y },
                data: { label: node_class_name },
            };

            setNodes((nds) => nds.concat(newNode));
        }
        else if (action == "NodesRemoval") {
            const nodes_list = msg["nodes_names"];

            setNodes((nds) => {
                return nds.filter((node) => !nodes_list.includes(node.id));
            });
        }
        else if (action == "EdgesCreation") {
            const edges = msg["edges"];

            setEdges((edg) => edg.concat(edges));
        }
        else if (action == "EdgesRemoval") {
            const edges_list = msg["edges"];

            setEdges((eds) => {
                return eds.filter((edge) => {
                    return !edges_list.some((e) =>
                        edge.source === e.source &&
                        edge.sourceHandle === e.sourceHandle &&
                        edge.target === e.target &&
                        edge.targetHandle === e.targetHandle
                    );
                });
            });
        }
    }
    // Receive message from panel
    useEffect(() => {
        model.on('msg:custom', (msg) => {
            receiveMessage(msg, setNodes, setEdges);
        });
    }, [setNodes, setEdges]); // Missing dependencies!

    const isValidConnection = useCallback(
        (connection) => {
            if (allowEdgeLoops)
                return true;
            // we are using getNodes and getEdges helpers here
            // to make sure we create isValidConnection function only once
            const nodes = getNodes();
            const edges = getEdges();
            const target = nodes.find((node) => node.id === connection.target);
            const hasCycle = (node, visited = new Set()) => {
                if (visited.has(node.id)) return false;

                visited.add(node.id);

                for (const outgoer of getOutgoers(node, nodes, edges)) {
                    if (outgoer.id === connection.source) return true;
                    if (hasCycle(outgoer, visited)) return true;
                }
            };

            if (target.id === connection.source) return false;
            return !hasCycle(target);
        },
        [getNodes, getEdges],
    );


    return (
        <div className="dndflow" style={{ display: 'flex', width: '100%', height: '100%' }}>
            <div className="reactflow-wrapper" ref={reactFlowWrapper}>
                <ReactFlow
                    nodes={nodes}
                    edges={edges}
                    onNodesChange={onNodesChangeHandler}
                    onEdgesChange={onEdgesChangeHandler}
                    onConnect={onConnect}
                    nodeTypes={nodeTypes}
                    onDrop={onDrop}
                    onDragStart={onDragStart}
                    onDragOver={onDragOver}
                    isValidConnection={isValidConnection}
                    fitView
                >
                    <Controls />
                    <MiniMap />
                    <Background variant="dots" gap={12} size={1} />
                </ReactFlow>
            </div>
            {displaySidebar && <Sidebar />}
        </div>
    );
};

export function render({ model }) {
    return (
        <ReactFlowProvider>
            <ModelProvider model={model}>
                <DnDProvider>
                    <DnDFlow />
                </DnDProvider>
            </ModelProvider>
        </ReactFlowProvider>
    );
};
