import redis
import json
r = redis.Redis(host='localhost', port=6379, db=0)
all_keys = r.keys('*')

for key in all_keys:
	print(key.decode('utf-8'))
	res = r.get(key)
	tmp = json.loads(res)
	try:
		print(tmp)
		if(tmp["hooks"] == "0x15F3F147eB0278b46363529083751363Be248c00"):
			print("find!")
	except:
		print("no")
