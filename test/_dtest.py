import requests
import json
import time

_payload_1 = json.dumps({
  "data": {
    "Poolkey": {
		"currency0": "0x6aD83000194DFCf9a0869091B2Ea7D121033163E",
		"currency1": "0xe61398b1Cb0FBED8268808A983Ad71ECFE2e1Ee9",
		"fee": 0,
		"tickSpacing": 60,
		"hooks": "0xd7b5397f95fA038e78dae2FD5956f11805bd8aC0"
    },
    "mode" : 2
  }#
})# 30 days hook
_payload_2 = json.dumps({
  "data": {
    "Poolkey": {
		"currency0": "0x6aD83000194DFCf9a0869091B2Ea7D121033163E",
		"currency1": "0xe61398b1Cb0FBED8268808A983Ad71ECFE2e1Ee9",
		"fee": 0,
		"tickSpacing": 60,
		"hooks": "0xF20Ac4669fc2bbAC775B46875E22Ba851bF64AC0"
    },
    "mode" : 2
  }#
})# 304 days hook
_payload_3 = json.dumps({
  "data": {
    "Poolkey": {
      "currency0": "0x6aD83000194DFCf9a0869091B2Ea7D121033163E",
      "currency1": "0xe61398b1Cb0FBED8268808A983Ad71ECFE2e1Ee9",
      "fee": 0,
      "tickSpacing": 60,
      "hooks": "0xEB0E9255aaB63951464f8adF268f676575E92000"
    },
    "mode" : 2
  }#
})# init err hook
# 

_payload_4 = json.dumps({
  "data": {
    "Poolkey": {
      "currency0": "0x0197481B0F5237eF312a78528e79667D8b33Dcff",
      "currency1": "0xA56569Bd93dc4b9afCc871e251017dB0543920d4",
      "fee": 3000,
      "hooks": "0x1ab60164141C802C0Fc359f99268953E59ec6880",
      "tickSpacing": 60
    },
    "mode" : 2
  }#
})# beforeaddliquidity err

print("")
url = "http://localhost:8000/api/tasks"
headers = {
    'Content-Type': 'application/json'
}
print("30 days fail")
res = requests.post(url, headers = headers, data = _payload_1)
print(res.text)
time.sleep(1)

print("1 year fail")
res = requests.post(url, headers = headers, data = _payload_2)
print(res.text)
time.sleep(1)

print("init err")
res = requests.post(url, headers = headers, data = _payload_3)
print(res.text)
time.sleep(1)

print("beforeaddliquidity err")
res = requests.post(url, headers = headers, data = _payload_4)
print(res.text)

