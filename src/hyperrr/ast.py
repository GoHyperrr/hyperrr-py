from dataclasses import dataclass
from typing import Dict, List, Union


class Node:
    pass


@dataclass
class TextNode(Node):
    text: str


@dataclass
class VariableNode(Node):
    name: str


@dataclass
class PromptCallNode(Node):
    ref: str
    kwargs: Dict[str, Union[str, List[Node]]]


@dataclass
class ExpressionNode(Node):
    expr: str
