from typing import Optional, Any, Dict, List, Union, Tuple

from pathlib import Path
import logging
from copy import deepcopy
from collections import OrderedDict

import networkx as nx
from networkx.drawing.nx_agraph import to_agraph


logger = logging.getLogger(__name__)


PYGRAPHVIZ_IMPORTED = False
try:
    import pygraphviz  # pylint: disable=unused-import

    PYGRAPHVIZ_IMPORTED = True
except ImportError:
    logger.info(
        "Could not import `pygraphviz`. Please install via: \n"
        "pip install pygraphviz\n"
        "(You might need to run this first: apt install libgraphviz-dev graphviz )"
    )


class PipelineError(Exception):
    pass


class PipelineRuntimeError(Exception):
    pass


class PipelineConnectError(PipelineError):
    pass


class PipelineValidationError(PipelineError):
    pass


class PipelineMaxLoops(PipelineError):
    pass


def locate_pipeline_input_nodes(graph) -> List[str]:
    """
    Collect the nodes with no input edges: they receive directly the pipeline inputs.
    """
    return [node for node in graph.nodes if not graph.in_edges(node) or graph.nodes[node]["input_node"]]


def locate_pipeline_output_nodes(graph) -> List[str]:
    """
    Collect the nodes with no output edges: these define the output of the pipeline.
    """
    return [node for node in graph.nodes if not graph.out_edges(node) or graph.nodes[node]["output_node"]]


class Pipeline:
    """
    Nodes orchestration engine.

    Builds a graph of nodes and orchestrates their execution according to the execution graph.
    """

    def __init__(
        self,
        metadata: Optional[Dict[str, Any]] = None,
        max_loops_allowed: int = 100,
    ):
        """
        Creates the Pipeline.

        :param metadata: arbitrary dictionary to store metadata about this pipeline. Make sure
            all the values contained in this dictionary can be serialized and deserialized if you wish to save this
            pipeline to file with `save_pipelines()/load_pipelines()`.
        :param max_loops_allowed: how many times the pipeline can run the same node before throwing an exception.
        """
        self.metadata = metadata or {}
        self.max_loops_allowed = max_loops_allowed
        self.graph = nx.DiGraph()

    def __eq__(self, other) -> bool:
        """
        Equal pipelines share all nodes and metadata instances.
        """
        if not isinstance(other, type(self)):
            return False
        return (
            self.metadata == other.metadata
            and self.max_loops_allowed == other.max_loops_allowed
            and self.graph == other.graph
        )

    def add_node(
        self,
        name: str,
        instance: Any,
        parameters: Optional[Dict[str, Any]] = None,
        input_node: bool = False,
        output_node: bool = False,
    ) -> None:
        """
        Create a node for the given node. Nodes are not connected to anything by default:
        use `Pipeline.connect()` to connect nodes together.

        Node names must be unique, but node instances can be reused if needed.

        :param name: the name of the node.
        :param instance: the node instance.
        :param parameters: default parameters to pass to this node's instance only then this
            specific node is executed. These parameters are NOT shared across nodes that use
            the same instance.
        :param input_node: whether this node should receive the input data given to
            `Pipeline.run()` directly, regardless of its location in the Pipeline.
        :param output_node: whether the output of this node should be returned as output,
            regardless of its location in the Pipeline.
        :returns: None
        """
        # Node names are unique
        if name in self.graph.nodes:
            raise ValueError(f"Node named '{name}' already exists: choose another name.")

        # Node instances must be nodes
        if not hasattr(instance, "__canals_node__"):
            raise PipelineValidationError(
                f"'{type(instance)}' doesn't seem to be a node. Is this class decorated with @node?"
            )

        # Params must be a dict
        if parameters and not isinstance(parameters, dict):
            raise ValueError("'parameters' must be a dictionary.")

        # Add node to the graph, disconnected
        logger.debug("Adding node '%s' (%s)", name, instance)
        self.graph.add_node(
            name,
            instance=instance,
            visits=0,
            parameters=parameters,
            input_node=input_node,
            output_node=output_node,
        )

    def connect(self, connect_from: str, connect_to: str) -> None:
        """
        Connect nodes together. All nodes to connect must exist in the pipeline.
        If connecting to an node that has several output edges, specify its name with 'node_name.edge_name'.

        :param connect_from: the node that deliver the values. This can be either a single node name or
            can be in the format `node_name.edge_name` if the node has multiple outputs.
        :param connect_to: the node that receives the values. This is always just the node name.
        :returns: None
        """
        upstream_node_name = connect_from
        downstream_node_name = connect_to

        # Find out the name of the edge
        edge_name = None
        # Edges may be named explicitly by passing 'node_name.edge_name' to connect().
        # Specify the edge name for the upstream node only.
        if "." in upstream_node_name:
            upstream_node_name, edge_name = upstream_node_name.split(".", maxsplit=1)
            upstream_node = self.graph.nodes[upstream_node_name]["instance"]
        else:
            # If the edge had no explicit name and the upstream node has multiple outputs, raise an exception
            upstream_node = self.graph.nodes[upstream_node_name]["instance"]
            if len(upstream_node.outputs) != 1:
                raise PipelineConnectError(
                    f"Please specify which output of '{upstream_node_name}' "
                    f"'{downstream_node_name}' should connect to. Node '{upstream_node_name}' has the following "
                    f"outputs: {upstream_node.outputs}"
                )
            edge_name = upstream_node.outputs[0]

        # Remove edge name from downstream_node name (it's needed only when the node is upstream)
        downstream_node_name = downstream_node_name.split(".", maxsplit=2)[0]
        downstream_node = self.graph.nodes[downstream_node_name]["instance"]

        # All nodes names must be in the pipeline already
        if upstream_node_name not in self.graph.nodes:
            raise PipelineConnectError(f"'{upstream_node_name}' is not present in the pipeline.")
        if downstream_node_name not in self.graph.nodes:
            raise PipelineConnectError(f"'{downstream_node_name}' is not present in the pipeline.")

        # Check if the edge with that name already exists between those two nodes
        if any(
            edge[1] == downstream_node_name and edge[2]["label"] == edge_name
            for edge in self.graph.edges.data(nbunch=upstream_node_name)
        ):
            logger.info(
                "An edge called '%s' connecting node '%s' and node '%s' already exists: skipping.",
                edge_name,
                upstream_node_name,
                downstream_node_name,
            )
            return

        # Find all empty slots in the upstream and downstream nodes
        free_downstream_inputs = deepcopy(downstream_node.inputs)
        for _, __, data in self.graph.in_edges(downstream_node_name, data=True):
            position = free_downstream_inputs.index(data["label"])
            free_downstream_inputs.pop(position)

        free_upstream_outputs = deepcopy(upstream_node.outputs)
        for _, __, data in self.graph.out_edges(upstream_node_name, data=True):
            position = free_upstream_outputs.index(data["label"])
            free_upstream_outputs.pop(position)

        # Make sure the edge is connecting one free input to one free output
        if edge_name not in free_downstream_inputs or edge_name not in free_upstream_outputs:
            inputs_string = "\n".join(
                [
                    " - " + edge[2]["label"] + f" (taken by {edge[0]})"
                    for edge in self.graph.in_edges(downstream_node_name, data=True)
                ]
                + [f" - {free_in_edge} (free)" for free_in_edge in free_downstream_inputs]
            )
            outputs_string = "\n".join(
                [
                    " - " + edge[2]["label"] + f" (taken by {edge[1]})"
                    for edge in self.graph.out_edges(upstream_node_name, data=True)
                ]
                + [f" - {free_out_edge} (free)" for free_out_edge in free_upstream_outputs]
            )
            raise PipelineConnectError(
                f"Cannot connect '{upstream_node_name}' with '{downstream_node_name}' "
                f"with an edge named '{edge_name}': "
                f"their declared inputs and outputs do not match.\n"
                f"Upstream node '{upstream_node_name}' declared these outputs:\n{outputs_string}\n"
                f"Downstream node '{downstream_node_name}' declared these inputs:\n{inputs_string}\n"
            )
        # Create the edge
        logger.debug(
            "Connecting node '%s' to node '%s' along edge '%s'",
            upstream_node_name,
            downstream_node_name,
            edge_name,
        )
        self.graph.add_edge(upstream_node_name, downstream_node_name, label=edge_name)

    def get_node(self, name: str) -> Dict[str, Any]:
        """
        Returns all the data associated with a node.

        :param name: the name of the node
        :returns: a dictionary containing all data that was given to `add_node()` (except for `name`)
        """
        candidates = [node for node in self.graph.nodes if node == name]
        if not candidates:
            raise ValueError(f"Node named {name} not found.")
        return self.graph.nodes[candidates[0]]

    def draw(self, path: Path) -> None:
        """
        Draws the pipeline. Requires `pygraphviz`.
        Run `pip install canals[draw]` to install missing dependencies.

        :param path: where to save the drawing.
        """
        if not PYGRAPHVIZ_IMPORTED:
            raise ImportError(
                "Could not import `pygraphviz`. Please install via: \n"
                "pip install pygraphviz\n"
                "(You might need to run this first: apt install libgraphviz-dev graphviz )"
            )
        graph = deepcopy(self.graph)

        input_nodes = locate_pipeline_input_nodes(graph)
        output_nodes = locate_pipeline_output_nodes(graph)

        # Draw the input
        graph.add_node("input", shape="plain")
        for node in input_nodes:
            for edge in graph.nodes[node]["instance"].inputs:
                graph.add_edge("input", node, label=edge)

        # Draw the output
        graph.add_node("output", shape="plain")
        for node in output_nodes:
            for edge in graph.nodes[node]["instance"].outputs:
                graph.add_edge(node, "output", label=edge)

        graphviz = to_agraph(graph)
        graphviz.layout("dot")
        graphviz.draw(path)
        logger.debug("Pipeline diagram saved at %s", path)

    def warm_up(self):
        """
        Make sure all nodes are warm.

        It's the node's responsibility to make sure this method can be called at every `Pipeline.run()`
        without re-initializing everything.
        """
        for node in self.graph.nodes:
            if hasattr(self.graph.nodes[node]["instance"], "warm_up"):
                self.graph.nodes[node]["instance"].warm_up()

    def run(
        self,
        data: Union[Dict[str, Any], List[Tuple[str, Any]]],
        parameters: Optional[Dict[str, Dict[str, Any]]] = None,
        debug: bool = False,
    ) -> Dict[str, Any]:
        """
        Runs the pipeline.

        :param data: the inputs to give to the input nodes of the Pipeline.
        :param parameters: a dictionary with all the parameters of all the nodes, namespaced by node.
        :param debug: whether to collect and return debug information.
        :returns: a dictionary with the outputs of the output nodes of the Pipeline.
        """
        parameters = self._validate_parameters(parameters=parameters)
        self.warm_up()
        self._validate_pipeline()

        # **** The Pipeline.run() algorithm ****
        #
        # Nodes are run as soon as an input for them appears in the inputs buffer.
        # When there's more than a node at once  in the buffer (which means some
        # branches are running in parallel or that there are loops) they are selected to
        # run in FIFO order by the `inputs_buffer` OrderedDict.
        #
        # Inputs are labeled with the name of the node they're aimed for:
        #
        #   ````
        #   inputs_buffer[target_node] = [(input_edge, input_value), ...]
        #   ```
        #
        # Nodes should wait until all the necessary input data has arrived before running.
        # If they're popped from the input_buffer before they're ready, they're put back in.
        # If the pipeline has branches of different lengths, it's possible that a node has to
        # wait a bit and let other nodes pass before receiving all the input data it needs.
        #
        # Data access:
        # - Name of the node       # self.graph.nodes  (List[str])
        # - Node instance          # self.graph.nodes[node]["instance"]
        # - Input nodes            # [e[0] for e in self.graph.in_edges(node)]
        # - Output nodes           # [e[1] for e in self.graph.out_edges(node)]
        # - Output edges           # [e[2]["label"] for e in self.graph.out_edges(node, data=True)]
        logger.info("Pipeline execution started.")
        inputs_buffer: OrderedDict = OrderedDict()

        for node_name in locate_pipeline_input_nodes(self.graph):
            # NOTE: We allow users to pass dictionaries just for convenience.
            # The real input format is List[Tuple[str, Any]], to allow several input edges to have the same name.
            if isinstance(data, dict):
                data = list(data.items())
            inputs_buffer[node_name] = {"data": data, "parameters": parameters}

        # *** PIPELINE EXECUTION LOOP ***
        # We select the nodes to run by checking which keys are set in the
        # inputs buffer. If the key exists, the node might be ready to run.
        pipeline_results: Dict[str, List[Dict[str, Any]]] = {}
        while inputs_buffer:
            logger.debug("> Current node queue: %s", inputs_buffer.keys())

            node_name, node_inputs = inputs_buffer.popitem(last=False)  # FIFO

            # Check if we looped over this node too many times
            self._check_max_loops(node_name)

            ready_to_run, inputs_buffer = self._ready_to_run(
                node_name=node_name, node_inputs=node_inputs, inputs_buffer=inputs_buffer
            )
            if not ready_to_run:
                continue

            # **** RUN THE NODE ****
            # It is our turn! The node is ready to run and all inputs are ready
            #
            # Let's raise the visits count
            self.graph.nodes[node_name]["visits"] += 1

            # Check for default parameters and add them to the parameter's dictionary
            # Default parameters are the one passed with the `pipeline.add_node()` method
            # and have lower priority with respect to parameters passed through `pipeline.run()`
            # or the modifications made by other nodes along the pipeline.
            if self.graph.nodes[node_name]["parameters"]:
                node_inputs["parameters"][node_name] = {
                    **(self.graph.nodes[node_name]["parameters"] or {}),
                    **parameters.get(node_name, {}),
                }

            # Get the node
            node_node = self.graph.nodes[node_name]["instance"]

            # Call the node
            try:
                logger.info(
                    "* Running %s (visits: %s)",
                    node_name,
                    self.graph.nodes[node_name]["visits"],
                )
                logger.debug("   '%s' inputs: %s", node_name, node_inputs)
                node_results: Tuple[Dict[str, Any], Dict[str, Dict[str, Any]]]
                node_results = node_node.run(
                    name=node_name, data=node_inputs["data"], parameters=node_inputs["parameters"]
                )
                logger.debug("   '%s' outputs: %s\n", node_name, node_results)
            except Exception as e:
                raise PipelineRuntimeError(
                    f"{node_name} raised '{e.__class__.__name__}: {e}' \ninputs={node_inputs['data']}\nparameters={node_inputs.get('parameters', None)}\n\n"
                    "See the stacktrace above for more information."
                ) from e

            # **** PROCESS THE OUTPUT ****
            # The node run successfully. Let's store or distribute the output it produced, if it's valid.
            #
            # Type-check the output
            if (
                len(node_results) != 2
                or not isinstance(node_results[0], dict)
                or not isinstance(node_results[1], dict)
                or not all(isinstance(params, dict) for params in node_results[1].values())
            ):
                logger.debug("Node output is malformed!\n%s", node_results)
                raise PipelineRuntimeError(
                    f"The node '{node_name}' did not return proper output. Check out the '@node' docstring."
                )

            # Process the output of the node
            if not self.graph.out_edges(node_name):
                # If there are no output edges, the output of this node is the output of the pipeline:
                # store it in pipeline_results.
                if not node_name in pipeline_results.keys():
                    pipeline_results[node_name] = []
                # We use append() to account for the case in which a node outputs several times
                # (for example, it can happen if there's a loop upstream). The list gets unwrapped before
                # returning it if there's only one output.
                pipeline_results[node_name].append(node_results[0])
            else:
                inputs_buffer = self._route_output(
                    node_results=node_results, node_name=node_name, inputs_buffer=inputs_buffer
                )

        logger.info("Pipeline executed successfully.")

        # Simplify output for single edge, single output pipelines
        pipeline_results = self._unwrap_results(pipeline_results)
        return pipeline_results

    def _validate_parameters(self, parameters: Optional[Dict[str, Dict[str, Any]]]) -> Dict[str, Dict[str, Any]]:
        """
        Validate the input parameters.
        """
        if not parameters:
            return {}

        if any(node not in self.graph.nodes for node in parameters.keys()):
            logging.warning(
                "You passed parameters for one or more node(s) that do not exist in the pipeline: %s",
                [node for node in parameters.keys() if node not in self.graph.nodes],
            )
        return parameters

    def _validate_pipeline(self):
        """
        Make sure the pipeline has at least one input node and one output node.
        """
        if not locate_pipeline_input_nodes(self.graph):
            raise ValueError("This pipeline has no input nodes!")

        if not locate_pipeline_output_nodes(self.graph):
            raise ValueError("This pipeline has no output nodes!")

    def _check_max_loops(self, node_name: str):
        """
        Verify whether this node run too many times.
        """
        if self.graph.nodes[node_name]["visits"] > self.max_loops_allowed:
            raise PipelineMaxLoops(f"Maximum loops count ({self.max_loops_allowed}) exceeded for node '{node_name}'.")

    def _ready_to_run(
        self, node_name: str, node_inputs: Dict[str, Any], inputs_buffer: OrderedDict
    ) -> Tuple[bool, OrderedDict]:
        """
        Verify whether a node is ready to run.

        Returns true if the node should run, false otherwise, and the updated inputs buffer.
        """
        # List all the inputs the current node should be waiting for.
        inputs_received = [i[0] for i in node_inputs["data"]]

        # We should be wait on all edges except for the downstream ones, to support loops.
        # This downstream check is enabled only for nodes taking more than one input
        # (the "entrance" of the loop).
        is_merge_node = len(self.graph.in_edges(node_name)) != 1
        data_to_wait_for = [
            (e[0], e[2]["label"])  # the node and the edge label
            for e in self.graph.in_edges(node_name, data=True)  # for all input edges
            # if there's a path in the graph leading back from the current node to the
            # input node, in case of multiple input nodes.
            if not is_merge_node or not nx.has_path(self.graph, node_name, e[0])
        ]

        if not data_to_wait_for:
            # This is an input node, so it's ready to run.
            logger.debug("'%s' is an input node and it's ready to run.")
            return (True, inputs_buffer)

        # Do we have all the inputs we expect?
        nodes_to_wait_for, inputs_to_wait_for = zip(*data_to_wait_for)
        if sorted(inputs_to_wait_for) == sorted(inputs_received):
            return (True, inputs_buffer)

        # This node is missing some inputs.
        #
        # Did all the upstream nodes run?
        if not all(self.graph.nodes[node_to_wait_for]["visits"] > 0 for node_to_wait_for in nodes_to_wait_for):
            # Some node upstream didn't run yet, so we should wait for them.
            logger.debug(
                "Putting '%s' back in the queue, some inputs are missing "
                "(inputs to wait for: %s, inputs_received: %s)",
                node_name,
                inputs_to_wait_for,
                inputs_received,
            )
            # Put back the node in the inputs buffer at the back...
            inputs_buffer[node_name] = node_inputs
            # ... and do not run this node (yet)
            return (False, inputs_buffer)

        # All upstream nodes run, so it **must** be our turn.
        #
        # Are we missing ALL inputs or just a few?
        if not inputs_received:
            # ALL upstream nodes have been skipped.
            #
            # Let's skip this node and add all downstream nodes to the queue.
            self.graph.nodes[node_name]["visits"] += 1
            logger.debug(
                "Skipping '%s', all input nodes were skipped and no inputs were received "
                "(skipped nodes: %s, inputs: %s)",
                node_name,
                nodes_to_wait_for,
                inputs_to_wait_for,
            )
            # Put all downstream nodes in the inputs buffer...
            downstream_nodes = [e[1] for e in self.graph.out_edges(node_name)]
            for downstream_node in downstream_nodes:
                if not downstream_node in inputs_buffer:
                    inputs_buffer[downstream_node] = {
                        "data": [],
                        "parameters": {},
                    }
            # ... and never run this node
            return (False, inputs_buffer)

        # If all nodes upstream have run and we received SOME input,
        # this is a merge node that was waiting on a node that has been skipped, so it's ready to run.
        # Let's pass None on the missing edges and go ahead.
        #
        # Example:
        #
        # --------------- value ----+
        #                           |
        #        +---X--- even ---+ |
        #        |                | |
        # -- parity_check         sum --
        #        |                 |
        #        +------ odd ------+
        #
        # If 'parity_check' produces output only on 'odd', 'sum' should run
        # with 'value' and 'odd' only, because 'even' will never arrive.
        #
        inputs_to_wait_for = list(inputs_to_wait_for)
        for input_expected in inputs_to_wait_for:
            if input_expected in inputs_received:
                inputs_to_wait_for.pop(inputs_to_wait_for.index(input_expected))
        logger.debug(
            "Some nodes upstream of '%s' were skipped, so some inputs will be None (missing inputs: %s)",
            node_name,
            inputs_to_wait_for,
        )
        for missing_input in inputs_to_wait_for:
            node_inputs["data"].append((missing_input, None))

        return (True, inputs_buffer)

    def _route_output(
        self,
        node_name: str,
        node_results: Tuple[Dict[str, Any], Dict[str, Dict[str, Any]]],
        inputs_buffer: OrderedDict,
    ) -> OrderedDict:
        """
        Distrubute the outputs of the node into the input buffer of downstream nodes.

        Returns the updated inputs buffer.
        """
        # This is not a terminal node: find out where the output goes, to which nodes and along which edge
        is_decision_node_for_loop = (
            any(nx.has_path(self.graph, edge[1], node_name) for edge in self.graph.out_edges(node_name))
            and len(self.graph.out_edges(node_name)) > 1
        )
        for edge_data in self.graph.out_edges(node_name, data=True):
            edge = edge_data[2]["label"]
            target_node = edge_data[1]

            # If this is a decision node and a loop is involved, we add to the input buffer only the nodes
            # that received their expected output and we leave the others out of the queue.
            if is_decision_node_for_loop and not edge in node_results[0].keys():
                if nx.has_path(self.graph, target_node, node_name):
                    # In case we're choosing to leave a loop, do not put the loop's node in the buffer.
                    logger.debug(
                        "Not adding '%s' to the inputs buffer: we're leaving the loop.",
                        target_node,
                    )
                else:
                    # In case we're choosing to stay in a loop, do not put the external node in the buffer.
                    logger.debug(
                        "Not adding '%s' to the inputs buffer: we're staying in the loop.",
                        target_node,
                    )
            else:
                # In all other cases, populate the inputs buffer for all downstream nodes, setting None to any
                # edge that did not receive input.
                if not target_node in inputs_buffer:
                    inputs_buffer[target_node] = {
                        "data": []
                    }  # Create the buffer for the downstream node if it's not there yet
                if edge in node_results[0].keys():
                    inputs_buffer[target_node]["data"].append((edge, node_results[0][edge]))
                inputs_buffer[target_node]["parameters"] = node_results[1]

        return inputs_buffer

    def _unwrap_results(self, pipeline_results):
        """
        Simplifies the output of simple Pipelines:

        - if the resuklt contains output of a single node, unwraps the dictionary to return the list only
        - if the resulting list is only composed of one dictionary, returns the internal dictionary only.

        So the output of `Pipeline.run()` might look like:

        - Multi-node output: `{node: [{key: value, ... }, ... ], ... }`
        - Single-node, repeated output: `[{key: value, ... }, ... ]`
        - Single-node, single output: `{key: value, ... }`
        """
        if len(pipeline_results.keys()) == 1:
            pipeline_results = pipeline_results[list(pipeline_results.keys())[0]]  # type: ignore

            if len(pipeline_results) == 1:
                pipeline_results = pipeline_results[0]  # type: ignore

        return pipeline_results
