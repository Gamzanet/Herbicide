## install
git clone https://github.com/Gamzanet/Herbicide.git --recursive  
cd Herbicide  
docker build . -t herbicide-api  


### RUN
```
# .env
_data_location=../../src/data/
uni="UNICHAIN_RPC_URL"
```
write .env  
docker run -d -p 7777:8000 --env-file .env --name "api-ubuntu-server" herbicide-api  
docker exec api-ubuntu-server /bin/bash
sh run.sh
