from pymongo import MongoClient

client = MongoClient('localhost',27017)

dbname = client.vm_management
collection = dbname['vmdetails']

def getVmDetails():
    vmdetails= []
    vmdata = collection.find()
    for record in vmdata:
        vmdetails.append(record)
    return vmdetails

def getSpecificVmDetails(vm_name):
    data = {}
    vmdata = collection.find({'vm_name':vm_name})
    for i in vmdata:
        data.update(i)
    return data

def updateVmDetails(vmdata):
    data = []
    vm_name = vmdata['vm_name']
    client_name = vmdata['client_name']
    status = vmdata['status']
    update = collection.update({'vm_name':vm_name},{"$set":{'client_name':client_name,'status':status}})
    getvm = collection.find({'vm_name':vm_name})
    for i in getvm:
        data.append(i)
    return data
