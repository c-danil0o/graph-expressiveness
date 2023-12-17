# Setup
from web3 import Web3

alchemy_url = "https://eth-mainnet.g.alchemy.com/v2/b4NTkO8I0PoGbjnrRkR-p0JflJRWY-6v"
w3 = Web3(Web3.HTTPProvider(alchemy_url))

# Print if web3 is successfully connected
print(w3.is_connected())

# Get the latest block number
latest_block = w3.eth.get_block("latest")

ending_blocknumber = 18721960
starting_blocknumber = ending_blocknumber - 3

for x in range(starting_blocknumber, ending_blocknumber):
    block = w3.eth.get_block(x, True)
    for transaction in block['transactions']:
        print('transaction')
        print(transaction['to'])
        print(transaction['from'], end='\n')

