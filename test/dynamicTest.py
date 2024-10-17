import requests
import json

payload1 = json.dumps({
	"currency0": "0x6f0cD9aC99c852bDBA06F72db93078cbA80A32F5",
	"currency1": "0x8dB7EFd30A632eD236eAbde82286551f843D5487",
	"fee": "0",
	"tickSpacing": "60",
	"hooks": "0x0fb2c35d2151b1009702acf2c2921c14a4ff41d0"
})# not implement hook
payload2 = json.dumps({
	"currency0": "0x6f0cD9aC99c852bDBA06F72db93078cbA80A32F5",
	"currency1": "0x8dB7EFd30A632eD236eAbde82286551f843D5487",
	"fee": "0",
	"tickSpacing": "60",
	"hooks": "0x7dFCe7A9Cc9E6Cfa35a3aBf0079988b58dD15040"
})# all implement hook
url = "http://localhost:8000/api/tasks"
headers = {
    'Content-Type': 'application/json'
}
res = requests.post(url, headers = headers, data = payload2)
print(res.text)

