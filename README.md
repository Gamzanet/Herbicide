## install
git clone https://github.com/Gamzanet/fastAPI.git --recursive  
cd fastAPI  
docker build . -t gamza-api  
docker run   


### RUN
```
# .env
_data_location=../../src/data/
uni="UNICHAIN_RPC_URL"
```
docker run -d -p 7777:8000 --env-file .env --name "api-ubuntu-server" gamza-api  
