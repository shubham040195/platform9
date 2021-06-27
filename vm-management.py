from flask import Flask
from flask_restful import Resource, Api
from flask import request
import json
from bson import json_util
import vmdb
from paramiko import SSHClient
app = Flask(__name__)
api = Api(app)



def vMockCleanup(host,vIp,vUser):
    port = 22
    password = 'abcd'
    ssh = SSHClient()
    ssh.load_system_host_keys()
    ssh.connect(host,port,username,password)
    stdin, stdout, stderr = ssh.exec_command('rm -rf /tmp')
    return True


class VmDetails(Resource):
    # To get the all available VMs and its respective details
    def get(self):
        vm_data = vmdb.getVmDetails()
        return json.loads(json_util.dumps(vm_data))

    # To checkout the VM for client and its VMs details.

    def put(self):
        vm_details = {}

        vm_name = request.args.get('vm_name')

        client_name = request.args.get('client_name')
        vm_data = vmdb.getVmDetails()
        for vm in vm_data:
            if vm['vm_name'] == vm_name and vm['status']=='available':
                vm.update({'client_name':client_name,'vm_name':vm_name,'status':'InUse'})
                dbupdate = vmdb.updateVmDetails(vm)
                vm_details.update({'data':json.loads(dbupdate)})
            elif vm['status'] == 'InUse' and vm['vm_name']==vm_name:
                vm_details.update({'data':'Requested VM is not available. Please try again after sometime.'})

        return vm_details

    # To checkin the VMs and adding VM back to pool

    def delete(self):
        vm_details = {}
        vm_name = request.args.get('vm_name')
        vm_data = vmdb.getSpecificVmDetails(vm_name)
        vIp = vm_data['ipv4']
        vUser = vm_data['username']
        # function to cleanup the VM data after client checkin for now it will be hardcoded for test vm
#        vm_cleanup = vMockCleanup(vm_name,vIp,vUser)
        vm_cleanup = True # Assuming VM is cleanup successfully.
        if vm_cleanup == True:
            vm_details.update({'client_name':None,'vm_name':vm_name,'status':'available'})
            dbupdate = vmdb.updateVmDetails(vm_details)
            return json.dumps({'data': 'Virtual Machine is free to use '+vm_name+''})

api.add_resource(VmDetails,'/vmdetails')

if __name__ == '__main__':
    app.run(debug=True)
