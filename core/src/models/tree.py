import json

from api.src.types.graph import Node, Graph


class TreeNode(Node):
    def __init__(self, node_id: int, data: dict, children: list):
        super().__init__(node_id, data)
        self.children: list[TreeNode] = children


class Tree(object):
    def __init__(self, root: Node, graph: Graph):
        self.root = TreeNode(root.node_id, root.data, [])
        visited: list[Node] = [root]
        self.dfs_traverse(self.root, root, graph, visited)

    def dfs_traverse(self, tree_node: TreeNode, node: Node, graph: Graph, visited: list[Node]):
        for neighbour in graph.get_neighbours_undirected(node):
            if neighbour not in visited:
                visited.append(neighbour)
                new_node = TreeNode(neighbour.node_id, neighbour.data, [])
                tree_node.children.append(new_node)
                self.dfs_traverse(new_node, neighbour, graph, visited)

    def get_json(self):
        tree = {"name": self.root.node_id, "data": self.root.data, "children": []}
        self.dfs_dict(tree, self.root)
        return tree
       #  with open("graph_explorer/app/static/tree.json", "w") as output:
       # ## with open("tree.json", "w") as output:
       #      json.dump(tree, output)

    def dfs_dict(self, tree: dict, node: TreeNode):
        for child in node.children:
            dict_node = {"name": child.node_id, "data": child.data, "children": []}
            tree["children"].append(dict_node)
            self.dfs_dict(dict_node, child)
