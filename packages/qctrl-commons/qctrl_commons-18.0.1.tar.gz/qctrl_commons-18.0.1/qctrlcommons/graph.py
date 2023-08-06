# Copyright 2023 Q-CTRL. All rights reserved.
#
# Licensed under the Q-CTRL Terms of service (the "License"). Unauthorized
# copying or use of this file, via any medium, is strictly prohibited.
# Proprietary and confidential. You may not use this file except in compliance
# with the License. You may obtain a copy of the License at
#
#    https://q-ctrl.com/terms
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS. See the
# License for the specific language.
"""Module for custom Graph."""
import logging
from typing import (
    Callable,
    Dict,
)

from qctrlcommons.node.registry import NODE_REGISTRY

LOGGER = logging.getLogger(__name__)


class Graph:
    """
    Utility class for representing and building a Q-CTRL data flow graph.

    You can call methods to add nodes to the graph, and use the `operations` attribute to get a
    dictionary representation of the graph.

    Parameters
    ----------
    operations : dict[str, str], optional
        The initial dictionary of operations for the graph. You can can omit this parameter if this
        is a new graph (which is expected to be true in almost all cases).
    """

    def __init__(self, operations: Dict[str, str] = None):
        self.operations = operations or {}

    def __getattr__(self, attr):
        # We override getattr to stop pylint from complaining about missing attributes for methods
        # that are added dynamically.
        raise AttributeError(f"'Graph' object has no attribute '{attr}'.")


def _extend_method(cls, func: Callable):
    """
    Extends the specified class by adding methods as attributes.

    Parameters
    ----------
    cls : class
        The class to which the function should be added.
    func : Callable
        Function to be added to the class as a method.
    """
    func_name = func.__name__
    if hasattr(cls, func_name):
        LOGGER.debug("existing attr %s on namespace: %s", func_name, cls)
    else:
        LOGGER.debug("adding attr %s to namespace: %s", func_name, cls)
        setattr(cls, func_name, func)


# set nodes to Graph
for node_cls in NODE_REGISTRY.as_list():
    node = node_cls.create_graph_method()
    _extend_method(Graph, node)
