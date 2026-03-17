from dataclasses import dataclass
from typing import Dict, List


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
    kwargs: Dict[str, str]


@dataclass
class Template:
    schema: dict
    nodes: List[Node]
