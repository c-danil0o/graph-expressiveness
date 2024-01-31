import random
from itertools import filterfalse

from api.src.services.source_plugin import SourcePlugin

# Setup
from web3 import Web3

from api.src.types.graph import Graph, Node, Edge

alchemy_url = "https://eth-mainnet.g.alchemy.com/v2/b4NTkO8I0PoGbjnrRkR-p0JflJRWY-6v"
w3 = Web3(Web3.HTTPProvider(alchemy_url))
latest_block_number = 18806431

_graph = Graph


def load_from_blocks(blocks_num: int, graph_name: str, latest_block: int = -1) -> Graph:
    global latest_block_number, _graph, w3
    if latest_block != -1:
        latest_block_number = latest_block
    start_block_number = latest_block_number - blocks_num
    print(w3.is_connected())
    _graph = Graph(graph_name, None, [], [])
    blocks = [w3.eth.get_block(block, True) for block in range(start_block_number, latest_block_number)]
    root: Node = Node(0, {'connected': 1})
    _graph.add_node(root)
    _graph.set_root(root)
    for block in blocks:
        for transaction in block['transactions']:
            transaction_node: Node = Node(int.from_bytes(transaction['hash'], byteorder='big'),
                                          {'from': transaction['from'], 'to': transaction['to'],
                                           'blockNumber': transaction['blockNumber'],
                                           'gas': transaction['gas'],
                                           'gasPrice': transaction['gasPrice'],
                                           'connected': 0})
            _graph.add_node(transaction_node)
    for node in _graph.nodes:
        for node2 in _graph.nodes:
            if node != root and node2 != root and node.data['from'] == node2.data['to'] and node != node2:
                node.data['connected'] = 1
                node2.data['connected'] = 1
                new_edge: Edge = Edge(node.data['from'], {}, node, node2, True)
                #      root_edge = Edge(1, {}, root, node, True)
                _graph.add_edge(new_edge)
            #   _graph.add_edge(root_edge)
    _graph.nodes = list(filterfalse(lambda x: not x.data['connected'], _graph.nodes))
    visited: list[Node] = []
    for node in _graph.nodes:
        if node != root and node not in visited:
            dfs_undirected(_graph, visited, node)
            root_edge = Edge(1, {}, root, visited[-1], True)
            _graph.add_edge(root_edge)
    return _graph


def get_neighbours_undirected(graph: Graph, node: Node):
    neighbours = []
    for edge in graph.edges:
        if node == edge.source:
            neighbours.append(edge.destination)
        if node == edge.destination:
            neighbours.append(edge.source)
    return neighbours


def dfs_undirected(graph: Graph, visited: list[Node], node: Node):  # function for dfs
    if node not in visited:
        visited.append(node)
        for neighbour in get_neighbours_undirected(graph, node):
            dfs_undirected(graph, visited, neighbour)


class DataSource(SourcePlugin):
    def load(self, config: dict):
        return load_from_blocks(config['blocks_num'], config['graph_name'], config['latest_block'])

    def identifier(self):
        return "graph-explorer-ethereum-datasource"

    def name(self):
        return "ethereum_datasource"
