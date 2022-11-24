from typing import Any, TypeAlias


Node: TypeAlias = dict[str, Any]
class TreeStore:
    def __init__(self, nodes: list[Node]) -> None:
        self.items: list[Node] = nodes
        # local copy to change for future functions
        self._items: list[Node] = nodes

        # see `_unpack_list_to_dict`
        self._unpacked_items: dict[int, Node] = self._unpack_list_to_dict()
        self._bfs()

    def getAll(self) -> list[Node]:
        return self.items

    def getItem(self, id: int) -> Node | str:
        item: Node | None = self._unpacked_items.get(id)
        if item:
            output = dict.copy(item)
            output.pop("children")
            return output
        else:
            return "Item doesn't exist. Try again."

    def getChildren(self, id: int) -> list[Node | None] | str:
        children: list[int | None] = self._unpacked_items[id]["children"]
        if not children:
            return []
        else:
            output: list[Node | None] = []
            for child_index in children:
                item: Node | str = self.getItem(child_index)
                if isinstance(item, str):
                    return item
                else:
                    child: Node = dict.copy(item)
                    output.append(child)
            return output

    def getAllParents(self, id: int) -> list[Node | None] | str:
        parents: list[Node | None] = []

        def _dfs(start_id) -> list[Node | None] | str:
            start: Node | str = self.getItem(start_id)
            if isinstance(start, str):
                return start
            else:
                if start["parent"] == "root":
                    return parents
                # reminder: `start` can be 'Item doesn't exist. Try again.'
                parents.append(self.getItem(start["parent"]))
                return _dfs(start["parent"])

        output: list[Node | None] | str = _dfs(id)
        return output

    def _bfs(self) -> None:
        """Breadth-first search.
        
        Needed to fill the `children` value of unpacked nodes.
        We use this for O(1) access to node's children as tasked.
        """
        node_dict = self._unpacked_items
        for index, node in node_dict.items():
            if node["parent"] != "root":
                node_dict[node["parent"]]["children"].append(index)

    def _unpack_list_to_dict(self) -> dict:
        """Unpacks list of Nodes to dictionary of separate Nodes.

        We store the unpacked dict in memory to speed up access to
        children by id (as is tasked). Because the time complexity of looking
        up all the Nodes in the list is O(N) + O(1), the main idea is to store
        all the individual ids, so we can get O(1) access speed while
        sacrificing O(N) memory. We also set `children` key for future 
        (see `_bfs()`).
        
        This method is optimal as long as we have enough memory, minimal
        number of hash collisions and frequent access to the Node list by id.
        The final output is shown below, dict's key is Node's id.
        """
        # items_dict = {
        #     1: {"id": 1, "parent": "root", "children": []},
        #     2: {"id": 2, "parent": 1, "type": "test", "children": []},
        #     3: {"id": 3, "parent": 1, "type": "test", "children": []},
        #     4: {"id": 4, "parent": 2, "type": "test", "children": []},
        #     5: {"id": 5, "parent": 2, "type": "test", "children": []},
        #     6: {"id": 6, "parent": 2, "type": "test", "children": []},
        #     7: {"id": 7, "parent": 4, "type": None, "children": []},
        #     8: {"id": 8, "parent": 4, "type": None, "children": []},
        # }
        if not self.items:
            return {}
        else:
            items_dict: dict[int, Node] = {}
            for item in self._items:
                item.update({"children": []})
                items_dict.update({item["id"]: item})
            return items_dict
