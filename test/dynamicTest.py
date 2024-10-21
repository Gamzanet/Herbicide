import requests
import json
import time

payload2 = json.dumps({
	"currency0": "0x6aD83000194DFCf9a0869091B2Ea7D121033163E",
	"currency1": "0xe61398b1Cb0FBED8268808A983Ad71ECFE2e1Ee9",
	"fee": 0,
	"tickSpacing": 60,
	"hooks": "0x7e06d9b96178ab9e3d0d27f84f29476e42057ff0",
	"data": {"cocoa" : "1234", "qwer":"3333"}
})# unichain for-loop hook
payload3 =json.dumps({
	"data":{
		"PoolKey":{
			"currency0": "0x0197481B0F5237eF312a78528e79667D8b33Dcff",
			"currency1": "0xA56569Bd93dc4b9afCc871e251017dB0543920d4",
		    "fee": 0,
		    "tickSpacing": 60,
		    "hooks": "0xDefb3B8B58375e500d67cc31b91c51166cf8CaC0"
		}
	}
}) ## only by poolmanager err 

payload1 = json.dumps({
  "data": {
    "Poolkey": {
		"currency0": "0x6aD83000194DFCf9a0869091B2Ea7D121033163E",
		"currency1": "0xe61398b1Cb0FBED8268808A983Ad71ECFE2e1Ee9",
		"fee": 0,
		"tickSpacing": 60,
		"hooks": "0x693153d5d512f343ff89CDdBBf18019c226241D0"
    },
    "mode" : 2
  }
})# not implement hook
payload_1 = json.dumps({
  "data": {
    "Poolkey": {
		"currency0": "0x6aD83000194DFCf9a0869091B2Ea7D121033163E",
		"currency1": "0xe61398b1Cb0FBED8268808A983Ad71ECFE2e1Ee9",
		"fee": 0,
		"tickSpacing": 60,
		"hooks": "0xdab6453c40422F80467f5a426656aB3650cc3Ff0"
    },
    "mode" : 2
  }
})# oog hook

payload_2 = json.dumps({
  "data": {
    "Poolkey": {
		"currency0": "0x6aD83000194DFCf9a0869091B2Ea7D121033163E",
		"currency1": "0xe61398b1Cb0FBED8268808A983Ad71ECFE2e1Ee9",
		"fee": 0,
		"tickSpacing": 60,
		"hooks": "0x7e06d9b96178ab9e3d0d27f84f29476e42057ff0",
    },
    "mode" : 2
  }
})# storage oob hook
# 
payload_3 = json.dumps({
  "data": {
    "Poolkey": {
		"currency0": "0x6aD83000194DFCf9a0869091B2Ea7D121033163E",
		"currency1": "0xe61398b1Cb0FBED8268808A983Ad71ECFE2e1Ee9",
		"fee": 0,
		"tickSpacing": 60,
		"hooks": "0x346b5B6a99a695cdc4820958B846Ab599c693FF0"
    },
    "mode" : 2
  }
}) ## oog
payload_4 = json.dumps({
  "data": {
    "Poolkey": {
		"currency0": "0x6aD83000194DFCf9a0869091B2Ea7D121033163E",
		"currency1": "0xe61398b1Cb0FBED8268808A983Ad71ECFE2e1Ee9",
		"fee": 0,
		"tickSpacing": 60,
		"hooks": "0x693153d5d512f343ff89CDdBBf18019c226241D0"
    },
    "mode" : 2
  }
}) ## oog
payload_4 = json.dumps({
  "data": {
    "Poolkey": {
		"currency0": "0x6aD83000194DFCf9a0869091B2Ea7D121033163E",
		"currency1": "0xe61398b1Cb0FBED8268808A983Ad71ECFE2e1Ee9",
		"fee": 0,
		"tickSpacing": 60,
		"hooks": "0x3c712B5E5B4a7ee97E4e3F2330bFb435050a4800"
    },
    "mode" : 2
  }
}) ## kenny's oog
url = "http://localhost:8000/api/tasks"
headers = {
    'Content-Type': 'application/json'
}

res = requests.post(url, headers = headers, data = payload_4)
print(res.text)
#time.sleep(2)
res = requests.post(url, headers = headers, data = payload_3)
print(res.text)
#res = requests.post(url, headers = headers, data = payload3)
#print(res.text)

