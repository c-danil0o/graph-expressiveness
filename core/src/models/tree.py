from api.src.types.graph import Node, Graph


class TreeNode(Node):
    def __init__(self, node_id: int, data: dict, children: list):
        super().__init__(node_id, data)
        self.children = children


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
