from typing import Any, TypeAlias
import pytest
from main import TreeStore


Node: TypeAlias = dict[str, Any]
items: list[Node] = [
    {"id": 1, "parent": "root"},
    {"id": 2, "parent": 1, "type": "test"},
    {"id": 3, "parent": 1, "type": "test"},
    {"id": 4, "parent": 2, "type": "test"},
    {"id": 5, "parent": 2, "type": "test"},
    {"id": 6, "parent": 2, "type": "test"},
    {"id": 7, "parent": 4, "type": None},
    {"id": 8, "parent": 4, "type": None}
]


@pytest.mark.parametrize(
    "input, output",
    [(items, items)]
)
def test_getAll(input: list[Node], output: list[Node]) -> None:
    ts: TreeStore = TreeStore(input)
    assert ts.getAll() == output

@pytest.mark.parametrize(
    "id, output",
    [
        (1, {"id": 1, "parent": "root"}),
        (2, {"id": 2, "parent": 1, "type": "test"}),
        (3, {"id": 3, "parent": 1, "type": "test"}),
        (4, {"id": 4, "parent": 2, "type": "test"}),
        (5, {"id": 5, "parent": 2, "type": "test"}),
        (6, {"id": 6, "parent": 2, "type": "test"}),
        (7, {"id": 7, "parent": 4, "type": None}),
        (8, {"id": 8, "parent": 4, "type": None}),
    ]
)
def test_getItem(id: int, output: Node) -> None:
    ts: TreeStore = TreeStore(items)
    assert ts.getItem(id) == output

@pytest.mark.parametrize(
    "id, output",
    [
        (1, [{"id": 2, "parent": 1, "type": "test"}, {"id": 3, "parent": 1, "type": "test"}]),
        (2, [{"id": 4, "parent": 2, "type": "test"}, {"id": 5, "parent": 2, "type": "test"}, {"id": 6, "parent": 2, "type": "test"}]),
        (3, []),
        (4, [{"id": 7,"parent": 4,"type": None}, {"id": 8,"parent": 4,"type": None}]),
        (5, []),
        (6, []),
        (7, []),
        (8, []),
    ]
)
def test_getChildren(id, output) -> None:
    ts: TreeStore = TreeStore(items)
    assert ts.getChildren(id) == output

@pytest.mark.parametrize(
    "id, output",
    [
        (1, []),
        (2, [{"id": 1, "parent": "root"}]),
        (3, [{"id": 1, "parent": "root"}]),
        (4, [{"id": 2, "parent": 1, "type": "test"}, {"id": 1, "parent": "root"}]),
        (5, [{"id": 2, "parent": 1, "type": "test"}, {"id": 1, "parent": "root"}]),
        (6, [{"id": 2, "parent": 1, "type": "test"}, {"id": 1, "parent": "root"}]),
        (7, [{"id": 4,"parent": 2,"type": "test"}, {"id": 2,"parent": 1,"type": "test"}, {"id": 1,"parent": "root"}]),
        (8, [{"id": 4,"parent": 2,"type": "test"}, {"id": 2,"parent": 1,"type": "test"}, {"id": 1,"parent": "root"}]),
    ]
)
def test_getAllParents(id, output) -> None:
    ts: TreeStore = TreeStore(items)
    assert ts.getAllParents(id) == output
