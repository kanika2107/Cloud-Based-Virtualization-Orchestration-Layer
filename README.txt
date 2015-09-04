			MINI PROJECT CLOUD COMPUTING
Problem Definition – Build a fabric that can coordinate the provisioning of 
compute resources by negotiating with a set of Hypervisors running across 
physical servers in the datacenter. 
 
Expected Outcome – 
 
1. Resource Discovery: 
 
2. Resource Allocation 
Decide what resources to allocate to fulfil the request. It should be loosely coupled in the 
sense that mechanism and implementation should be separate. What this means is it should be 
a possible to change the “Algorithm” for allocation with minimal code changes or still better with 
change in configuration only. 
 
3. A REST API Server ( that can be consumed by a variety of clients to deal with the 
		virtual infrastructure). 

Expected API:  
VM APIs: 
■ VM_Creation: 
	● Argument: name, instance_type. 
	● Return: vmid(+ if successfully created, 0 if failed) 
	{ 
		vmid:38201 
	}	 
	● URL: http://server/vm/create?name=test_vm&instance_type=type&image_id=id 


VM_Query 
	● Argument: vmid 
	● Return: instance_type, name, id, pmid (0 if invalid vmid or 
		otherwise) 
	{ 
		"vmid":38201, 
		"name":"test_vm", 
		"instance_type":3, 
		"pmid": 2 
	} 
● URL: http://server/vm/query?vmid=vmid 

VM_Destroy 
	● Argument: vmid 
	● Return: 1 for success and 0 for failure. 
	{	 
		“status”:1 
	} 
	● URL: http://server/vm/destroy?vmid=vmid 

VM_Type 
	● Argument: NA 
	● Return: tid, cpu, ram, disk 
	{	 
		"types": [ 
		{ 
			"tid": 1, 
			"cpu": 1, 
			"ram": 512, 
			"disk": 1 
		}, 
		{ 
		"tid": 2, 
		"cpu": 2, 
		"ram": 1024, 
		"disk": 2 
		}, 
		{ 
		"tid": 3, 
		"cpu": 4, 
		"ram": 2048, 
		"disk": 3         } 
		] 
	} 
	● URL: http://server/vm/types 

Resource Service APIs: 

■ List_PMs 
	● Argument: NA 
	● Return: pmids 
	{ 
		“pmids”: [1,2,3] 
	} 
	● URL: http://server/pm/list 

■ List_VMs 
	● Argument: pmid 
	● Return: vmids (0 if invalid) 
	{ 
		“vmids”: [38201, 38203, 38205] 
	} 
	● URL:http://server/pm/listvms?pmid=id 

■ PM_Query 
	● Argument: pmid 
	● Return: pmid, capacity, free, no. of VMs running(0 if invalid pmid 
		or otherwise) 
	{ 
		“pmid”: 1, 
		“capacity”:{ 
			“cpu”: 4, 
			“ram”: 4096, 
			“disk”: 160 
		}, 
		“free”:{ 
			“cpu”: 2, 
			“ram”: 2048, 
			“disk”: 157 
		}, 
		“vms”: 1 
	}	 
	● URL: http://server/pm/query?pmid=id 
 
Image Service APIs: 

■ List_Images 
	● Argument: NA 
	● Return: id, name 
	{ 
	“images”:[ 
	{ 
		“id”: 100, 
			“name”: “Ubuntu­12.04­amd64” 
	}, 
	{ 
		“id”:101, 
		“name”: “Fedora­17­x86_64” 
	} 
	] 
	} 
	URL: http://server/image/list 
 
For all the other Restful calls return 0(that is the call is invalid) 


	Syntax: 
	 
	./script pm_file image_file flavor_file 
	 
	pm_file => Contains a list of IP addresses separated by new­line. These addresses the Physical 
	machines to be used for hosting VMs. A unique ID is to be assigned by you. 
	image_file => Contains a list of Images(full path) to be used for spawning VMs. The name of the 
	image is to be extracted from the path itself. A unique ID is to be assigned by you. 
	flavor_file => contains a dictionary of flavors which can be evaluated. 

TECHNOLOGY STACK USED
1)FLASK
2)PYTHON
3)LIBVIRT
4)KVM
5)VIRTUAL MACHINE MANAGER-HYPERVISOR

SHEDULING POLICY USED
FIFO(first in first out)

Location and names of my files
pm_file ---> /src/pm_file
image_file ----> /src/image_file
flavor_file ----> /src/vm_types


Name of source files:

main_mini.py:
1)Handles all the function API calls except VM_CREATE and VM_DESTROY

create.py
1)Handles VM_CREATE

destroy_vm.py
1)Handles VM_DESTROY

settings.py
1)Handles all the global variables used in the entire project

linux.img:
taken from http://wiki.qemu.org/Testing

