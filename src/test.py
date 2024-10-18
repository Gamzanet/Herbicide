import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
#../engine/gamza-dynamic/test/inputPoolkey/utils/getOffchainPrice.py
engine_path = os.path.join(current_dir, '..', 'engine', 'gamza-dynamic', 'test','inputPoolkey', 'utils')
sys.path.append(engine_path)
print(engine_path)
import getOffchainPrice

rpc_url = "https://unichain-sepolia.g.alchemy.com/v2/LVjDyU_Hfup9CLkn7lAl6LYu8cCw4HJm" 
#sys.argv[1]
token0_address = "0x7066eE42efEF618B2Eb32BeAd83BD2eb1CB88562"
token1_address = "0x31d0220469e10c4E71834a79b1f276d740d3768F"
token0_symbol = getOffchainPrice.get_token_symbol_from_rpc(rpc_url, token0_address).strip()
token1_symbol = getOffchainPrice.get_token_symbol_from_rpc(rpc_url, token1_address).strip()
	
getOffchainPrice.fetch_token_price(token0_symbol, token1_symbol)
