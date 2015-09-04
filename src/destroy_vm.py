import settings
import main_mini
import libvirt
import os
import sys
settings.init()

def destroy(vm):
    try:
        vmid=vm["vmid"]
	j=0
	#print vmid
	#print settings.created_vms
	for i in settings.created_vms:
	    if i[0]==int(vmid):
	        break
	    j=j+1
	vm_name=str(i[1])
	pmid=i[3]
	username=settings.machine_list[pmid][0]
	ip=settings.machine_list[pmid][1]
	#print vm_name,pmid,username,ip
	connect=libvirt.open("remote+ssh://"+username+"@"+ip+"/")
	request=connect.lookupByName(vm_name)
	if request.isActive():
	    request.destroy()
	request.undefine()
	del settings.created_vms[j]
	#print settings.created_vms[j]
	return {"status":1}
    except:
        return {"status":0}


