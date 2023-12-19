# # Setup
# from web3 import Web3
#
# from api.src.types.graph import Graph, Node, Edge
#
# alchemy_url = "https://eth-mainnet.g.alchemy.com/v2/b4NTkO8I0PoGbjnrRkR-p0JflJRWY-6v"
# w3 = Web3(Web3.HTTPProvider(alchemy_url))
# latest_block_number = 18806431
#
# _graph = Graph
#
#
# def load_from_blocks(blocks_num: int, graph_name: str, latest_block: int = -1) -> Graph:
#     global latest_block_number, _graph, w3
#     if latest_block != -1:
#         latest_block_number = latest_block
#     start_block_number = latest_block_number - blocks_num
#     print(w3.is_connected())
#     _graph = Graph(graph_name, None, [], [])
#     blocks = [w3.eth.get_block(block, True) for block in range(start_block_number, latest_block_number)]
#     first: bool = False
#     for block in blocks:
#         for transaction in block['transactions']:
#
#             node_from: Node = Node(transaction['from'], {})
#             node_to: Node = Node(transaction['to'], {})
#             transaction_edge = Edge(transaction['transactionIndex'],
#                                     {'blockNumber': transaction['blockNumber'], 'gas': transaction['gas'],
#                                      'gasPrice': transaction['gasPrice']}, source=node_from, destination=node_to,
#                                     directed=True)
#             if not first:
#                 first = True
#                 _graph.set_root(node_from)
#             _graph.add_node(node_from)
#             _graph.add_node(node_to)
#             _graph.add_edge(transaction_edge)
#     return _graph
#
#
# load_from_blocks(2, "Ethereum blockchain")
# print(_graph)
# print(_graph.get_node_count())
