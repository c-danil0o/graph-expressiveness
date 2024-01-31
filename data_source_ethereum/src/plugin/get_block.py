# Setup
from itertools import filterfalse

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
    first: bool = False
    for block in blocks:
        for transaction in block['transactions']:
            print(transaction)
            transaction_node: Node = Node(str(transaction['hash']),
                                          {'from': transaction['from'], 'to': transaction['to'],
                                           'blockNumber': transaction['blockNumber'],
                                           'gas': transaction['gas'],
                                           'gasPrice': transaction['gasPrice'],
                                           'hash': transaction['hash'],
                                           'connected': False})
            _graph.add_node(transaction_node)
    for node in _graph.nodes:
        for node2 in _graph.nodes:
            if node.data['from'] == node2.data['to']:
                node.data['connected'] = True
                node2.data['connected'] = True
                new_edge: Edge = Edge(node.data['from'], {}, node.data['from'], node2.data['to'], True)
                _graph.add_edge(new_edge)
    _graph.nodes = list(filterfalse(lambda x: not x.data['connected'], _graph.nodes))
    return _graph


load_from_blocks(10, "Ethereum blockchain")
print(_graph)
print(_graph.get_node_count())
