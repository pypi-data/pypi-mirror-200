import logging


logger = logging.getLogger(__name__)


class NodeError(Exception):
    pass


def node(class_):
    """
    Marks a class as a node. Any class decorated with `@node`
    can be picked up by a Pipeline, serialized, deserialized, etc.

    All nodes MUST follow the contract below.
    This docstring is the source of truth for nodes contract.

    ```python
    def __init__(self, [... nodes init parameters ...]):
    ```
    Mandatory method.

    Nodes should have an `__init__` method where they define:

    - `self.inputs = [<expected_input_edge_name(s)>]`:
        A list with all the edges they can possibly receive input from

    - `self.outputs = [<expected_output_edge_name(s)>]`:
        A list with the edges they might possibly produce as output

    - `self.init_parameters = {<init parameters>}`:
        Any state they wish to be persisted when they are marshalled.
        These values will be given to the `__init__` method of a new instance
        when the pipeline is unmarshalled.

    If nodes want to let users customize their input and output edges (be it
    the edge name, the edge count, etc...) they should provide properly
    named init parameters:

    - `input: str` or `inputs: List[str]` (always with proper defaults)
    - `output: str` or `outputs: List[str]` (always with proper defaults)

    All the rest is going to be interpreted as a regular init parameter that
    has nothing to do with the node edges.

    The `__init__` must be extrememly lightweight, because it's a frequent
    operation during the construction and validation of the pipeline. If a node
    has some heavy state to initialize (models, backends, etc...) refer to the
    `warm_up()` method.

    ```
    def warm_up(self):
    ```
    Optional method.

    This method is called by Pipeline before the graph execution.
    Make sure to avoid double-initializations, because Pipeline will not keep
    track of which nodes it called `warm_up()` on.

    ```
    def run(
        self,
        name: str,
        data: List[Tuple[str, Any]],
        parameters: Dict[str, Dict[str, Any]],
    ):
    ```
    Mandatory method.

    This is the method where the main functionality of the node should be carried out.
    It's called by `Pipeline.run()`, which passes the following parameters to it:

    - `name: str`: the name of the node. Allows the node to find its own parameters in
        the `parameters` dictionary (see below).

    - `data: List[Tuple[str, Any]]`: the input data.
        Pipeline guarantees that the following assert always passes:

        `assert self.inputs == [name for name, value in data]`

        which means that:
        - `data` is of the same length as `self.inputs`.
        - `data` contains one tuple for each string stored in `self.inputs`.
        - no guarantee is given on the values of these tuples: notably, if there was a
            decision node upstream, some values might be `None`.

        For example, if a node declares `self.inputs = ["value", "value"]` (think of a
        `Sum` node), `data` might look like:

        `[("value", 1), ("value", 10)]`

        `[("value", None), ("value", 10)]`

        `[("value", None), ("value", None)]`

        `[("value", 1), ("value", ["something", "unexpected"])]`

        but it will never look like:

        `[("value", 1), ("value", 10), ("value", 100)]`

        `[("value": 15)]`

        `[("value": 15), ("unexpected", 10)]`

    - `parameters: Dict[str, Dict[str, Any]]`: a dictionary of dictionaries with all
        the parameters for all nodes.
        Note that all nodes have access to all parameters for all other nodes: this
        might come handy to nodes like `Agent`s, that want to influence the behavior
        of nodes downstream.
        Nodes can access their own parameters using `name`, but they must **not** assume
        their name is present in the dictionary.
        Therefore, the best way to get the parameters is with
        `my_parameters = parameters.get(name, {})`

    Pipeline expect the output of this function to be a tuple of two dictionaries.
    The first item is a dictionary that represents the output and it should always
    abide to the following format:

    `{output_name: output_value for output_name in <subset of self.expected_output>}`

    Which means that:
    - Nodes are not forced to produce output on all the expected outputs: for example,
        nodes taking a decision, like classifiers, can produce output on a subset of
        the expected output edges and Pipeline will figure out the rest.
    - Nodes must not add any key in the data dictionary that is not present in `self.outputs`.

    The second item of the tuple is the `parameters` dictionary. This allows node to
    propagate downstream any change they might have done to the `parameters` dictionary.
    """
    logger.debug("Registering %s as a node", class_)

    # '__canals_node__' is used to distinguish nodes from regular classes.
    # Its value is set to the desired node name: normally it is the class name, but it can technically be customized.
    class_.__canals_node__ = class_.__name__

    # Check for run()
    if not hasattr(class_, "run"):
        # TODO check the node signature too
        raise NodeError("Nodes must have a 'run()' method. See the docs for more information.")

    return class_
