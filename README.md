## install
git clone https://github.com/Gamzanet/fastAPI.git --recursive  
cd fastAPI  
docker build . -t gamza-api  


### RUN
```
# .env
_data_location=../../src/data/
uni="UNICHAIN_RPC_URL"
```
write .env  
docker run -d -p 7777:8000 --env-file .env --name "api-ubuntu-server" gamza-api  
docker exec api-ubuntu-server /bin/bash
sh run.sh