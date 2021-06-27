# platform9
VM management code

# step to setup environment
apt-get install python
apt-get install pip
pip install flask
pip install paramiko
pip install pymongo

# step to setup mognodb database

wget -qO - https://www.mongodb.org/static/pgp/server-4.4.asc | sudo apt-key add -
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/4.4 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.4.list
sudo apt-get update
sudo apt-get install -y mongodb-org
sudo systemctl start mongod

# Login to database and create VM data

mongo
use vm_management
db.createCollection("vmdetails")
db.vmdetails.insert({'vm_name':'windows','ipv4':'192.168.0.1','ram':'16GB','cpu':'4c','status':'available','client_name':null,'username':'windows'})

# API calls to Get all VM details

curl http://localhost:5000/vmdetails

# APi call to check in vm
curl -X PUT 'http://localhost:5000/vmdetails?vm_name='ubuntu'&client_name='intel''

# Api call to checkout vm
curl -X DELETE 'http://localhost:5000/vmdetails?vm_name='ubuntu'&client_name='intel''

# Run python server using below coomand

python3 file_name.py
